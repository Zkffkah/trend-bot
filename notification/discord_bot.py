import json

import requests

from config import config


class DiscordBot(object):

    def __init__(self):
        self.secrect = config.discord.get("secrect", '')
        self.webhook_url = config.discord.get("webhook_url", None)

    def send_text(self, text):
        if self.webhook_url:
            payload = {
                "content": text
            }
            headers = {
                'Content-Type': 'application/json',
            }
            result = requests.post(
                self.webhook_url,
                data=json.dumps(payload), headers=headers)
            print(result)
