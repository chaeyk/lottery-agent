from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhlottery import DhLottery
from os import getenv
from time import sleep

from dotenv import load_dotenv
load_dotenv()

headless = getenv('LTA_HEADLESS') == '1'

chrome_options = Options()
if headless:
  chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
chrome_options.set_capability('unhandledPromptBehavior', 'accept')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.execute_cdp_cmd(
  'Page.addScriptToEvaluateOnNewDocument',
  {'source': "Object.defineProperty(navigator, 'platform', {get: () => 'Win64'})"}
)

dhlottery = DhLottery(driver)
dhlottery.login()
dhlottery.buyLp72(2)

if not headless:
  sleep(3600)

driver.quit()
