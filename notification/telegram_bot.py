import requests

import config


class TelegramBot(object):

    def __init__(self):
        self.token = config.config.telegram.get("token", '')
        self.chat_id = config.config.telegram.get("chat_id", '')

    def sendText(self, text):
        if self.token:
            url = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={content}".format(
                token=self.token,
                chat_id=self.chat_id,
                content=text
            )
            result = requests.get(url)
            print(result)
