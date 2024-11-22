import subprocess
import sys
import os
import time
import shutil
from pydub import AudioSegment
from io import BytesIO

from fastapi import UploadFile


class ValidationUtils:
    @staticmethod
    def is_empty(value):
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, (list, tuple, set, dict)) and not value:
            return True
        return False


def clean_path(path_str: str):
    if path_str.endswith(('\\', '/')):
        return clean_path(path_str[0:-1])
    path_str = path_str.replace('/', os.sep).replace('\\', os.sep)
    return path_str.strip(" ").strip('\'').strip("\n").strip('"').strip(" ").strip("\u202a")


def batch_clean_paths(paths):
    """
    批量处理路径列表，对每个路径调用 clean_path() 函数。

    参数:
        paths (list[str]): 包含待处理路径的列表。

    返回:
        list[str]: 经过 clean_path() 处理后的路径列表。
    """
    cleaned_paths = []
    for path in paths:
        cleaned_paths.append(clean_path(path))
    return cleaned_paths


def read_text_file_to_list(file_path):
    # 按照UTF-8编码打开文件（确保能够正确读取中文）
    with open(file_path, mode='r', encoding='utf-8') as file:
        # 读取所有行并存储到一个列表中
        lines = file.read().splitlines()
    return lines


def get_filename_without_extension(file_path):
    """
    Given a file path string, returns the file name without its extension.

    Parameters:
    file_path (str): The full path to the file.

    Returns:
    str: The file name without its extension.
    """
    base_name = os.path.basename(file_path)  # Get the base name (file name with extension)
    file_name, file_extension = os.path.splitext(base_name)  # Split the base name into file name and extension
    return file_name  # Return the file name without extension


def read_file(file_path):
    # 使用with语句打开并读取文件
    with open(file_path, 'r', encoding='utf-8') as file:  # 'r' 表示以读取模式打开文件
        # 一次性读取文件所有内容
        file_content = file.read()

    # 文件在with语句结束时会自动关闭
    # 现在file_content变量中存储了文件的所有文本内容
    return file_content


def write_text_to_file(text, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except IOError as e:
        print(f"Error occurred while writing to the file: {e}")
    else:
        print(f"Text successfully written to file: {output_file_path}")


def check_path_existence_and_return(path):
    """
    检查给定路径（文件或目录）是否存在。如果存在，返回该路径；否则，返回空字符串。
    :param path: 待检查的文件或目录路径（字符串）
    :return: 如果路径存在，返回原路径；否则，返回空字符串
    """
    if os.path.exists(path):
        return path
    else:
        return ""


def open_file(filepath):
    if sys.platform.startswith('darwin'):
        subprocess.run(['open', filepath])  # macOS
    elif os.name == 'nt':  # For Windows
        os.startfile(filepath)
    elif os.name == 'posix':  # For Linux, Unix, etc.
        subprocess.run(['xdg-open', filepath])


def str_to_int(input_str, default: int = None) -> int:
    """
    将字符串转换为整数。

    参数:
    input_str (str): 需要转换的字符串。
    default (int, optional): 如果转换失败时返回的默认值，默认为None。

    返回:
    int: 转换后的整数或默认值。
    """
    try:
        # 尝试直接转换为整数
        return int(input_str)
    except ValueError:
        try:
            # 如果是浮点数，尝试转换并四舍五入
            if '.' in input_str:
                return round(float(input_str))
        except ValueError:
            # 如果转换失败，则根据是否有默认值决定行为
            return default
    except TypeError:
        # 如果输入不是字符串类型，则抛出错误
        return default


def str_to_float(input_str, default=None):
    """
    尝试将输入的字符串转换为浮点数。
    
    参数:
    input_str (str): 要转换的字符串。
    default (float, optional): 如果转换失败时返回的默认值，默认为 None。
    
    返回:
    float or None: 如果成功转换为浮点数，则返回该浮点数；如果转换失败，则返回默认值或 None。
    """
    try:
        # 尝试将字符串转换为浮点数
        return float(input_str)
    except ValueError:
        # 如果转换失败，则返回默认值或 None
        return default
    except TypeError:
        # 如果输入不是字符串类型，则抛出错误
        return default


def get_absolute_path(relative_path):
    """
    将相对路径转换为绝对路径。
    
    :param relative_path: 相对路径字符串
    :return: 绝对路径字符串
    """
    absolute_path = os.path.join(os.getcwd(), relative_path)
    return os.path.normpath(absolute_path)


async def save_file(file: UploadFile, new_path: str):
    # 将文件内容写入指定路径
    with open(new_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024 * 8)  # 每次读取8KB
            if not chunk:
                break
            buffer.write(chunk)

        os.fsync(buffer.fileno())
        # Give some time for the filesystem to update if necessary
        # 这里添加一个小的等待时间，根据实际情况调整
        time.sleep(1)  # 可选


def delete_directory(temp_dir):
    """
    删除指定的目录及其所有内容。

    参数:
        temp_dir (str): 要删除的目录路径。
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def zip_directory(source_dir, output_filename):
    """
    将给定目录及其所有子目录压缩成一个 ZIP 文件。

    参数:
        source_dir (str): 要压缩的源目录路径。
        output_filename (str): 输出 ZIP 文件的名称（不包括扩展名）。
    """
    # 确保输出文件名没有 .zip 扩展名
    if output_filename.endswith('.zip'):
        output_filename = output_filename[:-4]

    # 创建压缩文件
    shutil.make_archive(output_filename, 'zip', source_dir)


def read_zip_to_memory(zip_file_path: str) -> BytesIO:
    """
    将 ZIP 文件读取到内存中，并返回一个 BytesIO 对象。

    参数:
        zip_file_path (str): ZIP 文件的路径。

    返回:
        BytesIO: 包含 ZIP 文件内容的内存对象。
    """
    # 打开 ZIP 文件并读取其内容到内存中
    with open(zip_file_path, 'rb') as file:
        zip_data = file.read()

    # 创建一个 BytesIO 对象并将 ZIP 文件内容写入其中
    zip_in_memory = BytesIO(zip_data)

    return zip_in_memory


def copy_file_to_dest_file(src_file, dest_file):
    """
    将指定文件复制到另一个指定文件路径，确保目标文件路径的所有上级目录存在。

    参数:
        src_file (str): 源文件的路径。
        dest_file (str): 目标文件的路径。
    """
    # 获取目标文件的上级目录
    dest_dir = os.path.dirname(dest_file)

    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 复制文件
    shutil.copy2(src_file, dest_file)


def merge_audio_files(audio_files, output_file):
    """
    将多个音频文件按顺序合并成一个音频文件。

    :param audio_files: 音频文件列表，每个元素是一个文件路径
    :param output_file: 合并后的音频文件路径
    """
    # 创建一个空的 AudioSegment 对象
    combined = AudioSegment.silent(duration=0)

    # 遍历音频文件列表，逐个加载并合并
    for file in audio_files:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"文件 {file} 不存在")
        audio_segment = AudioSegment.from_file(file)
        combined += audio_segment

    # 导出合并后的音频文件
    combined.export(output_file, format=os.path.splitext(output_file)[1][1:])