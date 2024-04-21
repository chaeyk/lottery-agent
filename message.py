import requests

class Message:
  message: str
  bottoken: str
  chatid: str

  def __init__(self, bottoken: str, chatid: str, m: str = ''):
    self.message = m
    self.bottoken = bottoken
    self.chatid = chatid

  def add(self, m: str):
    self.message = f'{self.message}\n{m}'

  def send(self):
    print(self.message)

    if not self.bottoken or not self.chatid:
      return

    url = f'https://api.telegram.org/bot{self.bottoken}/sendMessage'
    payload = {
      'chat_id': self.chatid,
      'text': self.message,
    }

    r = requests.post(url, json=payload)
    print(r.json())
