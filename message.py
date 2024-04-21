class Message:
  message: str

  def __init__(self, m: str = ''):
    self.message = m

  def add(self, m: str):
    self.message = f'{self.message}\n{m}'

  def send(self):
    print(self.message)
