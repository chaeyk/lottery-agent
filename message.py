import requests

class Message:
  message: str
  image: bytes | None
  bottoken: str
  chatid: str

  def __init__(self, bottoken: str, chatid: str, message: str = ''):
    self.message = message
    self.image = None
    self.bottoken = bottoken
    self.chatid = chatid

  def add(self, message: str):
    self.message = f'{self.message}\n{message}'

  def add_image(self, image: bytes):
    self.image = image

  def send(self):
    if self.message:
      self.send_message()
    if self.image:
      self.send_image()

  def send_message(self):
    print(self.message)

    if not self.bottoken or not self.chatid:
      return

    url = f'https://api.telegram.org/bot{self.bottoken}/sendMessage'
    payload = {
      'chat_id': self.chatid,
      'text': self.message,
    }

    requests.post(url, json=payload)

  def send_image(self):
    if not self.bottoken or not self.chatid:
      return

    url = f'https://api.telegram.org/bot{self.bottoken}/sendPhoto'
    files = {
      'photo': self.image,
    }
    data = {
      'chat_id': self.chatid,
    }
    requests.post(url, files=files, data=data)
