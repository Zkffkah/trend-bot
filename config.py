import json


class Config:

    def __init__(self):

        self.telegram = {}
        self.discord = {}

    def loads(self, config_file=None):
        configures = {}
        if config_file:
            try:
                with open(config_file) as f:
                    data = f.read()
                    configures = json.loads(data)
            except Exception as e:
                print(e)
                exit(0)
            if not configures:
                print("config json file error!")
                exit(0)
        self.update(configures)

    def update(self, update_fields):
        self.telegram = update_fields.get("telegram", {})
        self.discord = update_fields.get("discord", {})
        # 将配置文件中的数据按照dict格式解析并设置成config的属性
        for k, v in update_fields.items():
            setattr(self, k, v)


config = Config()
