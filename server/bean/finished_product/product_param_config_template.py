import shutil
import json
import os
import uuid
from io import BytesIO

from jinja2 import Template

from server.dao.data_base_manager import db_config
from server.util.util import delete_directory, zip_directory, read_zip_to_memory, write_text_to_file, \
    copy_file_to_dest_file
import server.common.config_params as params

config_template = """
{
    "version": "{{ version }}",
    "gpt_path": "{{ gpt_sovits_version }}/{{ gpt_model_name }}",
    "sovits_path": "{{ gpt_sovits_version }}/{{ vits_model_name }}",
    "introduction": "RAS-V2导出的基于GPT-Sovits的微调模型",
    "product_list": [
        {%- for audio in product_list %}
        {
            "name": "{{ audio.name }}",
            "default_selected": {{ 'true' if loop.first else 'false' }},
            "category": "{{ audio.category }}",
            "audio_path": "refer_audio/{{ audio.content }}.{{ audio.get_audio_extension() }}",
            "content": "{{ audio.content }}",
            "language": "{{ audio.language }}",
            "top_k": {{ audio.top_k }},
            "top_p": {{ audio.top_p }},
            "temperature": {{ audio.temperature }},
            "text_delimiter": "{{ audio.text_delimiter }}",
            "speed": {{ audio.speed }},
            "inp_refs": [
                {%- for sound in audio.sound_fusion_list %}
                {
                     "role_name": "{{ sound.role_name }}",
                     "category": "{{ sound.category }}",
                     "audio_path": "inp_refs/{{ sound.content }}.{{ sound.get_audio_extension() }}",
                     "content": "{{ sound.content }}",
                     "language": "{{ sound.language }}"
                }{% if not loop.last %},{% endif %}
                {%- endfor %}
            ],
            "score": {{ audio.score }},
            "remark": "{{ audio.remark }}"
        }{% if not loop.last %},{% endif %}
        {%- endfor %}
    ]
}
"""


class ParamItem:
    def __init__(self, gpt_sovits_version, gpt_model_name, gpt_model_path, vits_model_name,
                 vits_model_path):
        self.gpt_sovits_version = gpt_sovits_version  # 模型版本
        self.gpt_model_name = gpt_model_name  # GPT模型名称
        self.gpt_model_path = gpt_model_path  # GPT模型路径
        self.vits_model_name = vits_model_name  # Vits模型名称
        self.vits_model_path = vits_model_path  # Vits模型路径
        self.product_list = []
        self.version = params.version

    def generate_json_from_template(self, template: Template) -> str:
        # 渲染模板
        rendered_config = template.render({
            'version': self.version,
            'gpt_sovits_version': self.gpt_sovits_version,
            'gpt_model_name': self.gpt_model_name,
            'gpt_model_path': self.gpt_model_path,
            'vits_model_name': self.vits_model_name,
            'vits_model_path': self.vits_model_path,
            'product_list': self.product_list
        })
        return rendered_config

    def generate_model_file(self, directory: str, role_name: str, is_merge: bool, need_model: bool, template: Template):
        json_str = self.generate_json_from_template(template)
        real_obj = json.loads(json_str)
        model_dir = self.get_model_dir(directory, role_name, is_merge)
        config_file_path = os.path.join(model_dir, 'infer_config.json')
        write_text_to_file(json_str, config_file_path)
        self.copy_file(model_dir, real_obj, need_model)

    def copy_file(self, model_dir: str, real_obj: dict, need_model: bool):
        if need_model:
            gpt_path = real_obj.get('gpt_path')
            real_gpt_path = os.path.join(model_dir, gpt_path)
            copy_file_to_dest_file(self.gpt_model_path, real_gpt_path)
            sovits_path = real_obj.get('sovits_path')
            real_sovits_path = os.path.join(model_dir, sovits_path)
            copy_file_to_dest_file(self.vits_model_path, real_sovits_path)
        json_product_list = real_obj.get('product_list')
        # 使用 enumerate 函数
        for index, product in enumerate(self.product_list):
            json_product = json_product_list[index]
            audio_path = json_product.get('audio_path')
            real_audio_path = os.path.join(model_dir, audio_path)
            copy_file_to_dest_file(product.audio_path, real_audio_path)
            json_inp_refs = json_product.get('inp_refs')
            for second_index, sound in enumerate(product.sound_fusion_list):
                json_sound = json_inp_refs[second_index]
                audio_path = json_sound.get('audio_path')
                real_audio_path = os.path.join(model_dir, audio_path)
                copy_file_to_dest_file(sound.audio_path, real_audio_path)

    def get_model_dir(self, directory: str, role_name: str, is_merge: bool) -> str:
        dir_name = None
        if is_merge:
            dir_name = f'{role_name}-{self.gpt_sovits_version}-{self.gpt_model_name}-{self.vits_model_name}'
        else:
            dir_name = f'{role_name}-{self.product_list[0].name}-{self.product_list[0].id}'
        model_dir = os.path.join(directory, dir_name)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        return model_dir


class ProductParamConfigTemplate:
    def __init__(self, role_name, is_merge: bool, need_model: bool, product_list):
        self.role_name = role_name  # 角色名称
        self.is_merge = is_merge  # 是否合并
        self.need_model = need_model  # 是否需要包含模型
        self.param_item_list = []
        # 创建模板对象
        self.template = Template(config_template)
        self.merge_product_list(product_list)

    def merge_product_list(self, product_list):
        item_list = []
        if self.is_merge:

            seen = set()
            for product in product_list:
                gv_tuple = (product.gpt_model_name, product.vits_model_name)
                if gv_tuple not in seen:
                    item_list.append(
                        ParamItem(product.gpt_sovits_version, product.gpt_model_name, product.gpt_model_path,
                                  product.vits_model_name, product.vits_model_path))
                    seen.add(gv_tuple)
            for item in item_list:
                for product in product_list:
                    if product.gpt_model_name == item.gpt_model_name and product.vits_model_name == item.vits_model_name:
                        item.product_list.append(product)

        else:
            for product in product_list:
                item = ParamItem(product.gpt_sovits_version, product.gpt_model_name, product.gpt_model_path,
                                 product.vits_model_name, product.vits_model_path)
                item.product_list.append(product)
                item_list.append(item)

        self.param_item_list = item_list

    def generate_zip_file(self) -> tuple[str, str]:

        if len(self.param_item_list) == 0:
            return None

        temp_dir = f'{db_config.workspace}/temp/{uuid.uuid1()}'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        role_dir = os.path.join(temp_dir, self.role_name)
        if not os.path.exists(role_dir):
            os.makedirs(role_dir)

        try:
            for param_item in self.param_item_list:
                param_item.generate_model_file(role_dir, self.role_name, self.is_merge, self.need_model, self.template)

            zip_directory(role_dir, role_dir)

            zip_file_path = f'{role_dir}.zip'
            # zip_in_memory = read_zip_to_memory(zip_file_path)
        finally:
            # delete_directory(temp_dir)
            pass

        return temp_dir, zip_file_path
