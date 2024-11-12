import os
from server.bean.base_model import BaseModel
from server.dao.data_base_manager import db_config


class GptModel(BaseModel):
    def __init__(self, version=None, name=None, path=None):
        self.version = version
        self.name = name
        self.path = path

    def equals(self, version, name):
        return self.version == version and self.name == name

    @staticmethod
    def create_dir():
        os.makedirs(GptModel.get_base_v1_dir(), exist_ok=True)
        os.makedirs(GptModel.get_base_v2_dir(), exist_ok=True)

    @staticmethod
    def get_base_v1_dir():
        return f'{db_config.get_role_model_dir()}/GPT_weights'

    @staticmethod
    def get_base_v2_dir():
        return f'{db_config.get_role_model_dir()}/GPT_weights_v2'
