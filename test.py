from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

class interpark:
    id = 'johoon4687'
    pw = 'Hhtad9134@'
    goodsCode = '23006740'
    wantDate = '20230926'
    wantTime = '1' # 가능한 시간들 중 몇 번째인지

    def __init__(self):
        self.driver = webdriver.Chrome()
        # 사이즈조절
        self.driver.set_window_size(1400, 1000)  # (가로, 세로)
        self.driver.get('https://ticket.interpark.com/Gate/TPLogin.asp') # 페이지 이동
        # 로그인 후에 페이지가 로딩될 때까지 대기
    def login(self):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
        userId = self.driver.find_element(By.ID, 'userId')
        userId.send_keys(self.id) # 로그인 할 계정 id
        userPwd = self.driver.find_element(By.ID, 'userPwd')
        userPwd.send_keys(self.pw) # 로그인 할 계정의 패스워드
        userPwd.send_keys(Keys.ENTER)
        # 로그인 후에 페이지가 로딩될 때까지 대기
        time.sleep(1)
        self.driver.get('http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + self.goodsCode)

    # 태그가 없으면 에러발생
    def check_exists_by_element(self, by, name):
        try:
            self.driver.find_element(by, name)
        except NoSuchElementException:
            return False
        return True
    
    def close_ticketing_info(self):
        # 예매안내가 팝업이 뜨면 닫기. ( ticketingInfo_check : True, False )
        time.sleep(1)
        ticketingInfo_check = self.check_exists_by_element(By.XPATH, "//*[@id='popup-prdGuide']/div/div[3]/button")
        if ticketingInfo_check:
            self.driver.find_element(By.XPATH, "//*[@id='popup-prdGuide']/div/div[3]/button").click()

    def click_reservation_button(self):
        # 예매하기 버튼 클릭
        self.driver.find_element(By.XPATH, "//*[@id='productSide']/div/div[2]/a[1]").click()

        # 예매하기 눌러서 새창이 뜨면 포커스를 새창으로 변경
        print("count is ", self.driver.window_handles.count)
        time.sleep(10)
        # TODO
        # time sleep for typing string refactoring

        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get_window_position(self.driver.window_handles[1])
        # self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
        # chapchaText = self.driver.find_element(By.ID, 'txtCaptcha')
        # chapchaText.send_keys('ABCDEF')

    def select_date_time(self):
        # 날짜 아이프레임
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

        # 날짜 체크
        reserveDate = self.driver.find_element(By.XPATH, "//*[@id='PlayDate']")
        dateSelect = Select(reserveDate)
        dateSelect.select_by_value(self.wantDate)

        # 시간 체크
        reserveTime = self.driver.find_element(By.XPATH, "//*[@id='PlaySeq']")
        timeSelect = Select(reserveTime)
        timeSelect.select_by_index(self.wantTime)
        selected_option = timeSelect.first_selected_option
        selected_value = selected_option.get_attribute('value')
        timeSelect.select_by_value(selected_value)
        print(" selected time is ", selected_value)
        # for option in timeSelectOptions:
        #     print(" option: ", option.get_attribute('value'))

    def seat_title_checking1(level, block, seat):
        return "[title*='" + level + "석'][title*='" + block + "구역 " + str(seat) + "열']"

    def seat_title_checking2(level, block, seat):
        return "[title*='" + level + "석'][title*='" + block + "구역" + str(seat) + "열']"

    def seat_title_checking3(level,  block, seat):
        return "[title*='" + level + "석'][title*='" + block + "블럭" + str(seat) + "열']"

    def seat_title_checking4(level, block, seat):
        return "[title*='" + level + "석'][title*='-" + str(seat) + "열']"

    def seat_title_checking5(level, block, seat):
        return "[title*='" + level + "석'][title*='-" + chr(64 + seat) + "열']"

    def select_seat(self):
        # 좌석 선택 iframe
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//*[@id='ifrmSeatDetail']"))

        # 활성화 되어 있는 좌석의 class 속성 stySeat
        seat_check = self.driver.find_element(By.CSS_SELECTOR, "img.stySeat")
        seat_title = seat_check.get_attribute('title')
        b = seat_title.split('-')

        # 좌석 선택하는 태그의 title 속성의 포멧  
        # [VIP석] 1층-A구역18열-11
        # [VIP석] 1층-B구역 11열-1
        # [VIP석] 1층-D열-99
        # [VIP석] 1층-11열-11
        # [VIP석] 1층-A블럭8열-10

        if '구역' in b[1]:
            if b[1][b[1].find('역') + 1] == ' ':
                zone_seat_return = self.seat_title_checking1
            else:
                zone_seat_return = self.seat_title_checking2
        elif '블럭' in b[1]:
            zone_seat_return = self.seat_title_checking3
        else:
            c = re.compile('[0-9]')
            if c.match(b[1]):
                zone_seat_return = self.seat_title_checking4
            else:
                zone_seat_return = self.seat_title_checking5

        # 좌석 선택
        w_check = False
        seat = 0
        cnt = 0
        while seat < 20:
            seat = seat + 1
            # zon_seat_return의 매개변수 설명
            # level : VIP, R, A  등 좌석의 등급
            # block : A, B, C 등 좌석의 구역을 설정
            # seat : 숫자 또는 영어. 열을 지정
            seat_string = zone_seat_return(level, block, seat)	
            imgs = driver.find_elements(By.CSS_SELECTOR, "img.stySeat" + seat_string)

            for i in imgs:
                i.click()
                cnt = cnt + 1
                if cnt == int(people_):
                    w_check = True
                    break

            if w_check:
                break
        
        


stuff = interpark()
stuff.login()
stuff.close_ticketing_info()    
stuff.click_reservation_button()
stuff.select_date_time()
stuff.select_seat()

# # 예매하기 버튼 클릭
# driver.find_element(By.XPATH, "//div[@class='tk_dt_btn_TArea']/a").click()

# # 예매하기 눌러서 새창이 뜨면 포커스를 새창으로 변경
# driver.switch_to.window(driver.window_handles[1])
# driver.get_window_position(driver.window_handles[1])
