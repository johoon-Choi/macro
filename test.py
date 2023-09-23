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

    def lets_reserve(self):
        # 날짜 아이프레임
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

        # 월 체크
        reserveDate = self.driver.find_element(By.XPATH, "//*[@id='PlayDate']")
        select = Select(reserveDate)
        select.select_by_value(self.wantDate)

stuff = interpark()
stuff.login()
stuff.close_ticketing_info()    
stuff.click_reservation_button()
stuff.lets_reserve()

# # 예매하기 버튼 클릭
# driver.find_element(By.XPATH, "//div[@class='tk_dt_btn_TArea']/a").click()

# # 예매하기 눌러서 새창이 뜨면 포커스를 새창으로 변경
# driver.switch_to.window(driver.window_handles[1])
# driver.get_window_position(driver.window_handles[1])
