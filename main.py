from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhlottery import DhLottery
from os import getenv
from time import sleep

from dotenv import load_dotenv
load_dotenv(override=True)

def send_message(m: str):
  print(m)

def main():
  userid = getenv('DHL_USERID')
  password = getenv('DHL_PASSWORD')

  headless = getenv('LTA_HEADLESS') == '1'
  lo40_count = int(getenv('LTA_LO40_COUNT') or '1')
  lp72_count = int(getenv('LTA_LP72_COUNT') or '1')
  dryrun = getenv('LTA_DRYRUN') == '1'

  chrome_options = Options()
  if headless:
    chrome_options.add_argument('--headless')
  chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking']) # 팝업 차단
  chrome_options.set_capability('unhandledPromptBehavior', 'accept') # alert 통과

  driver = webdriver.Chrome(options=chrome_options)
  driver.implicitly_wait(10)
  driver.execute_cdp_cmd( # navigator.platform 이 Win64를 리턴해야 모바일 페이지가 뜨지 않는다.
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': "Object.defineProperty(navigator, 'platform', {get: () => 'Win64'})"}
  )

  message = '동행 복권 구매 결과입니다.\n'
  def add_message(s: str):
    nonlocal message
    message = f'{message}\n{s}'

  dhlottery = DhLottery(driver)
  dhlottery.login(userid, password)
  add_message(f'실행전 잔고: {dhlottery.getBalance()}')
  if lo40_count > 0:
    add_message(dhlottery.buyLo40(lo40_count, dryrun))
  if lp72_count > 0:
    add_message(dhlottery.buyLp72(lp72_count, dryrun))
  
  if headless:
    add_message(f'실행후 잔고: {dhlottery.getBalance()}')

  send_message(message)

  if not headless:
    sleep(3600)

  driver.quit()

try:
  main()
except Exception as e:
  print(e)
  raise
