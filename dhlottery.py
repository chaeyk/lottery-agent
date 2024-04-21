from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from os import getenv

class DhLottery:
  driver: WebDriver

  def __init__(self, driver: WebDriver):
    self.driver = driver

  def login(self):
    userid = getenv('DHL_USERID')
    password = getenv('DHL_PASSWORD')

    # 로그인 화면
    self.driver.get('https://dhlottery.co.kr/user.do?method=login&returnUrl=')

    userid_field = self.driver.find_element(By.ID, 'userId')
    userid_field.send_keys(userid)

    password_field = self.driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)

    login_button = self.driver.find_element(By.XPATH, '//div[@class="form"]/a')
    login_button.click()

    # 로그인 성공하면 메인 화면으로 이동됨
    # 메인 화면에 본인 이름 떠 있는지 확인
    name = self.driver.find_element(By.XPATH, '//form[@name="frmLogin"]/div/ul/li/span/strong')
    if not name.text.endswith('님'):
      raise Exception(f'로그인 실패: {name.text}')

  def buyLp72(self, count: int):
    self.driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LP72')

    iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
    self.driver.switch_to.frame(iframe)

    for i in range(count):
      jo = randint(1, 5)
      jo_button = self.driver.find_element(By.XPATH, f'//span[@class="notranslate lotto720_box jogroup num{jo}"]')
      jo_button.click()

      auto_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_auto_number')
      auto_button.click()

      confirm_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_confirm_number')
      confirm_button.click()

    buy1_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_pay')
    buy1_button.click()

    buy2_button = self.driver.find_element(By.XPATH, '//div[@id="lotto720_popup_confirm"]/div/div[@class="lotto720_popup_bottom_wrapper btn_area"]/a')
    WebDriverWait(self.driver, 10).until(EC.visibility_of(buy2_button))
    buy2_button.click()

    # 구매 결과

    sale_span = self.driver.find_element(By.CLASS_NAME, 'saleCnt')
    WebDriverWait(self.driver, 10).until(EC.visibility_of(sale_span))
    if sale_span.text != str(count):
      raise Exception('구매 실패건 있음')

    print(f'연금복권 구매완료: {count}매')
