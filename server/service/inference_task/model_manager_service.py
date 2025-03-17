import os
from server.bean.inference_task.gpt_model import GptModel
from server.bean.inference_task.vits_model import VitsModel
import server.common.config_params as params


class ModelManagerService:
    @staticmethod
    def get_gpt_model_list() -> list[GptModel]:
        GptModel.create_dir()
        v1_file_list = read_files_with_suffix(GptModel.get_base_v1_dir(), '.ckpt')
        v2_file_list = read_files_with_suffix(GptModel.get_base_v2_dir(), '.ckpt')
        v3_file_list = read_files_with_suffix(GptModel.get_base_v3_dir(), '.ckpt')
        gpt_model_list = [GptModel(version='v1', name=os.path.basename(file_path), path=file_path) for file_path in
                          v1_file_list]
        gpt_model_list = gpt_model_list + [GptModel(version='v2', name=os.path.basename(file_path), path=file_path) for
                                           file_path in v2_file_list]

        current_dir = os.getcwd()
        api_dir = os.path.join(current_dir, params.gsv2_dir)
        pretrained_models_dir = os.path.join(api_dir, 'GPT_SoVITS/pretrained_models')

        v3 = GptModel(version='v3', name='s1v3.ckpt', path=os.path.join(pretrained_models_dir, 's1v3.ckpt'))
        if os.path.exists(v3.path):
            gpt_model_list.append(v3)

        gpt_model_list = gpt_model_list + [GptModel(version='v3', name=os.path.basename(file_path), path=file_path) for
                                           file_path in v3_file_list]

        return gpt_model_list

    @staticmethod
    def get_vits_model_list() -> list[VitsModel]:
        VitsModel.create_dir()
        v1_file_list = read_files_with_suffix(VitsModel.get_base_v1_dir(), '.pth')
        v2_file_list = read_files_with_suffix(VitsModel.get_base_v2_dir(), '.pth')
        v3_file_list = read_files_with_suffix(VitsModel.get_base_v3_dir(), '.pth')
        vits_model_list = [VitsModel(version='v1', name=os.path.basename(file_path), path=file_path) for file_path in
                           v1_file_list]
        vits_model_list = vits_model_list + [VitsModel(version='v2', name=os.path.basename(file_path), path=file_path)
                                             for file_path in v2_file_list]

        current_dir = os.getcwd()
        api_dir = os.path.join(current_dir, params.gsv2_dir)
        pretrained_models_dir = os.path.join(api_dir, 'GPT_SoVITS/pretrained_models')

        v3 = VitsModel(version='v3', name='s2Gv3.pth', path=os.path.join(pretrained_models_dir, 's2Gv3.pth'))
        if os.path.exists(v3.path):
            vits_model_list.append(v3)

        vits_model_list = vits_model_list + [VitsModel(version='v3', name=os.path.basename(file_path), path=file_path)
                                             for file_path in v3_file_list]
        return vits_model_list

    @staticmethod
    def get_vits_model_by_name(gpt_sovits_version, vits_model_name):
        return next(filter(lambda model: model.equals(gpt_sovits_version, vits_model_name),
                           ModelManagerService.get_vits_model_list()))

    @staticmethod
    def get_gpt_model_by_name(gpt_sovits_version, gpt_model_name):
        return next(filter(lambda model: model.equals(gpt_sovits_version, gpt_model_name),
                           ModelManagerService.get_gpt_model_list()))


def read_files_with_suffix(directory, suffix):
    """
    读取指定目录下符合指定后缀名称的文件。
    参数:
    directory (str): 要搜索的目录路径。
    suffix (str): 要查找的文件后缀名。
    返回:
    list: 包含所有匹配后缀的文件路径的列表。
    """
    matching_files = []

    # 遍历目录中的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件是否匹配指定的后缀
            if file.endswith(suffix):
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                matching_files.append(file_path)

    return matching_files
