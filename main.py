from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser
from dhlottery import DhLottery
from message import Message
from os import getenv
from time import sleep

from dotenv import load_dotenv
load_dotenv(override=True)

def get_args():
  headless = getenv('LTA_HEADLESS', '1') == '1'
  dryrun = getenv('LTA_DRYRUN', '0') == '1'
  lo40_count = int(getenv('LTA_LO40_COUNT', '1'))
  lp72_count = int(getenv('LTA_LP72_COUNT', '1'))

  parser = ArgumentParser(description='Lottery Agent')
  parser.add_argument('command', choices=['buy', 'check'])
  parser.add_argument('--headless', dest='headless', action='store_true', default=headless, help='enable headless mode. [LTA_HEADLESS=1]')
  parser.add_argument('--no-headless', dest='headless', action='store_false', default=headless, help='disable headless mode. [LTA_HEADLESS=0]')
  parser.add_argument('--dryrun', dest='dryrun', action='store_true', default=dryrun, help='run only up to the point of purchase. [LTA_DRYRUN=1]')
  parser.add_argument('--no-dryrun', dest='dryrun', action='store_false', default=dryrun, help='run to the end. [LTA_DRYRUN=0]')
  parser.add_argument('--lo40', dest='lo40_count', metavar='n', type=int, default=lo40_count, help='lotto 6/45 purchase quantity. [LTA_LO40_COUNT=n]')
  parser.add_argument('--lp72', dest='lp72_count', metavar='n', type=int, default=lp72_count, help='annuity lottery 720+ purchase quantity. [LTA_LP72_COUNT=n]')
  args = parser.parse_args()

  print()
  print('Options')
  print('-------------------------------------')
  print(f'headless = {args.headless}')
  print(f'dryrun = {args.dryrun}')
  print(f'lo40 = {args.lo40_count}')
  print(f'lp72 = {args.lp72_count}')
  print('-------------------------------------')
  print()

  return args

def main(message: Message):
  userid = getenv('DHL_USERID')
  if not userid:
    raise Exception('should set DHL_USERID variable.')
  password = getenv('DHL_PASSWORD')
  if not password:
    raise Exception('should set DHL_PASSWORD variable.')

  args = get_args()
  return

  chrome_options = Options()
  if args.headless:
    chrome_options.add_argument('--headless')
  chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking']) # 팝업 차단
  chrome_options.set_capability('unhandledPromptBehavior', 'accept') # alert 통과

  driver = webdriver.Chrome(options=chrome_options)
  driver.implicitly_wait(10)
  driver.execute_cdp_cmd( # navigator.platform 이 Win64를 리턴해야 모바일 페이지가 뜨지 않는다.
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': "Object.defineProperty(navigator, 'platform', {get: () => 'Win64'})"}
  )

  dhlottery = DhLottery(driver)
  dhlottery.login(userid, password)

  if args.command == 'buy':
    message.add('동행 복권 구매 결과입니다.\n')

    message.add(f'실행전 잔고: {dhlottery.getBalance()}')

    if args.lo40_count > 0:
      message.add(dhlottery.buyLo40(args.lo40_count, args.dryrun))
    if args.lp72_count > 0:
      message.add(dhlottery.buyLp72(args.lp72_count, args.dryrun))
    
    # headless를 안 쓰는 건 개발할 때 화면을 보기 위해서다.
    # 잔고를 조회하면 화면이 넘어가버려서 디버깅하기 어려워진다.
    if args.headless:
      message.add(f'실행후 잔고: {dhlottery.getBalance()}')
  elif args.command == 'check':
    message.add(f'잔고: {dhlottery.getBalance()}')
  else:
    raise Exception(f'not implemented command: {args.command}')

  message.send()

  if not args.headless:
    sleep(3600)

  driver.quit()

message = Message()
try:
  main(message)
except Exception as e:
  message.send(f'\n에러 발생: {e}')
  raise
