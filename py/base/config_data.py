"""配置管理模块

Desc:
    这个版本先实现配置表加载功能

"""

import os
from base.const import server_const
from base.logger import SysLogger
import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from base.singleton import Singleton

@dataclass
class ConfigNode:
    data: dict

class ConfigData(metaclass=Singleton):

    def __init__(self, root_dir = os.path.abspath(server_const.config_root_dir)):
        """

        Args:
            @root_dir: 指定配置根目录,必须是绝对路径

        """

        self.config_root_dir = root_dir    # 配置目录
        self.loaded_config_map = dict()  # 已加载配置

    def get_conf(self, config_name) -> dict:
        if self.config_root_dir is None:
            SysLogger.error('config_data not inited')
            return None

        if config_name in self.loaded_config_map:
            return self.loaded_config_map[config_name].data
        else:
            config_str = self.load_config_from_disk(config_name)
            if config_str is None:
                SysLogger.error(f'load config fail {config_name}')
                return None

            try:
                config_node = ConfigNode(data = json.loads(config_str))   # 这样写方便后续加数据
            except JSONDecodeError as e:
                SysLogger.error(f'json load config string fail {config_name} {config_str}')
                return None
            self.loaded_config_map[config_name] = config_node
            return config_node.data

    def load_config_from_disk(self, config_name) -> str:
        full_dir = os.path.join(self.config_root_dir, f'{config_name}.json')
        if not os.path.exists(full_dir):
            SysLogger.error(f'{full_dir} not exists')
            return None

        with open(full_dir, 'r', encoding='utf8') as fd:
            config_str = fd.read()

        return config_str

if __name__ == '__main__':
    SysLogger.start('log/config.log')
    ConfigData()
    config = ConfigData().get_conf('a')
    config = ConfigData().get_conf('a')
    print(config)
    SysLogger.close()