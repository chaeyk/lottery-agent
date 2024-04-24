from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from random import randint
from os import getenv
import traceback

class DhLottery:
  driver: WebDriver
  dryrun: bool

  def __init__(self, driver: WebDriver):
    self.driver = driver
    self.dryrun = getenv('LTA_DRYRUN') == '1'

  def login(self, userid: str, password: str):
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

  def getBalance(self) -> str:
    self.driver.get('https://dhlottery.co.kr')

    money = self.driver.find_element(By.XPATH, '//li[@class="money"]/a/strong')
    return money.text

  def _get_popup_layer_message(self):
    try:
      layer_message = self.driver.find_element(By.XPATH, '//div[@id="popupLayerAlert"]/div/div/span[@class="layer-message"]')
      WebDriverWait(self.driver, 10).until(EC.visibility_of(layer_message))
      return layer_message.text
    except Exception as e:
      print('팝업 내용 못읽음:', e)
      traceback.print_exc()
      return ''

  # 로또 6/45
  def buyLo40(self, count: int, dryrun: bool) -> str:
    try:
      self.driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')

      iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
      self.driver.switch_to.frame(iframe)

      # 자동 번호 선택
      try:
        self.driver.execute_script('selectWayTab(1)')
      except:
        # 로또는 판매시간이 아니면 팝업이 뜬다.
        message = self._get_popup_layer_message()
        if message:
          raise Exception(message)
        raise

      # 수량 선택
      count_dropdown = Select(self.driver.find_element(By.ID, 'amoundApply'))
      count_dropdown.select_by_value(str(count))

      # 수량 확인 버튼
      select_num_button = self.driver.find_element(By.ID, 'btnSelectNum')
      select_num_button.click()

      if not dryrun:
        # 구매 버튼 누름
        buy_button = self.driver.find_element(By.NAME, 'btnBuy')
        buy_button.click()

        # 구매 확인 누름
        self.driver.execute_script('closepopupLayerConfirm(true)')

        # 구매 결과 확인
        report_row = self.driver.find_element(By.ID, 'reportRow')
        WebDriverWait(self.driver, 10)\
          .until(lambda driver: len(report_row.find_elements(By.XPATH, './li')) > 0)

        report_count = len(report_row.find_elements(By.XPATH, './li'))
        if count != report_count:
          raise Exception(f'로또 구매 실패 {count - report_count}건 있음')

      return f'로또 구매완료: {count}매'
    except Exception as e:
      print('로또 구매실패:', e)
      traceback.print_exc()
      return f'로또 구매실패: {e}'

  # 연금복권 720+
  def buyLp72(self, count: int, dryrun: bool) -> str:
    try:
      self.driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LP72')

      iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
      self.driver.switch_to.frame(iframe)

      for i in range(count):
        # 랜덤으로 조 선택
        jo = randint(1, 5)
        jo_button = self.driver.find_element(By.XPATH, f'//span[@class="notranslate lotto720_box jogroup num{jo}"]')
        jo_button.click()

        # 자동 번호 선택
        auto_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_auto_number')
        auto_button.click()

        # 구매 등록
        confirm_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_confirm_number')
        confirm_button.click()

      # 구매 버튼
      buy1_button = self.driver.find_element(By.CLASS_NAME, 'lotto720_btn_pay')
      buy1_button.click()

      Alert(self.driver).accept()

      if not dryrun:
        # 구매 버튼이 하나 더 있음
        buy2_button = self.driver.find_element(By.XPATH, '//div[@id="lotto720_popup_confirm"]/div/div[@class="lotto720_popup_bottom_wrapper btn_area"]/a')
        WebDriverWait(self.driver, 10).until(EC.visibility_of(buy2_button))
        buy2_button.click()

        # 구매 결과

        sale_span = self.driver.find_element(By.CLASS_NAME, 'saleCnt')
        WebDriverWait(self.driver, 10).until(EC.visibility_of(sale_span))
        sale_count = int(sale_span.text)
        if sale_count != count:
          raise Exception(f'연금복권 구매 실패 {count - sale_count}건 있음')

      return f'연금복권 구매완료: {count}매'
    except Exception as e:
      print('연금복권 구매실패:', e)
      traceback.print_exc()
      return f'연금복권 구매실패: {e}'
