from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class interpark:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # 사이즈조절
        self.driver.set_window_size(1400, 1000)  # (가로, 세로)
        self.driver.get('https://ticket.interpark.com/Gate/TPLogin.asp') # 페이지 이동
    def login(self):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
        userId = self.driver.find_element(By.ID, 'userId')
        userId.send_keys('johoon4687') # 로그인 할 계정 id
        userPwd = self.driver.find_element(By.ID, 'userPwd')
        userPwd.send_keys('Hhtad9134@') # 로그인 할 계정의 패스워드
        userPwd.send_keys(Keys.ENTER)
        self.driver.get('http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + '23006740')

    def check_exists_by_element(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def close_ticketing_info(self):
        ticketingInfo_check = self.check_exists_by_element(By.XPATH, "//*[@id="popup-prdGuide"]/div/div[3]/button")
        if ticketingInfo_check:
            self.driver.find_element(By.XPATH, "//*[@id="popup-prdGuide"]/div/div[3]/button").click()


stuff = interpark()
stuff.login()
stuff.close_ticketing_info()

# 예매하기 버튼 클릭
driver.find_element(By.XPATH, "//div[@class='tk_dt_btn_TArea']/a").click()

# 예매하기 눌러서 새창이 뜨면 포커스를 새창으로 변경
driver.switch_to.window(driver.window_handles[1])
driver.get_window_position(driver.window_handles[1])
