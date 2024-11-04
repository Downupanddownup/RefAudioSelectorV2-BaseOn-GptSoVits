import subprocess
import sys
import os
import time

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

