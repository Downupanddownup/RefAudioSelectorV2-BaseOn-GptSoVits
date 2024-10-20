import configparser
import os
import server.util.util as util


class ParamReadWriteManager:
    def __init__(self):
       pass


class ConfigManager:
    def __init__(self):
        self.config_path = 'server/config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='utf-8')

    def get_log(self, key):
        return self.config.get('Log',key)

    def get_other(self, key):
        return self.config.get('Other', key)

    def print(self):
        # 打印所有配置
        for section in self.config.sections():
            print('[{}]'.format(section))
            for key in self.config[section]:
                print('{} = {}'.format(key, self.config[section][key]))
            print()


_config = ConfigManager()
_param_read_write_manager = ParamReadWriteManager()


def get_config():
    return _config


def get_rw_param():
    return _param_read_write_manager


if __name__ == '__main__':
    print(_config.print())
