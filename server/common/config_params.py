import server.common.config_manager as config_manager
from server.util.util import str_to_int

config = config_manager.get_config()

# [Base]
# 版本号
version = config.get_base('version')
# Gpt-Sovits2项目路径
gsv2_dir = config.get_base('gsv2_dir')
# 推理任务并发进程数量
inference_process_num = str_to_int(config.get_base('inference_process_num'), 1)
# service port
service_port = str_to_int(config.get_base('service_port'), 8000)
# api port
api_port = str_to_int(config.get_base('api_port'), 8001)

# [Log]
# 日志保存目录路径
log_dir = config.get_log('log_dir')
# 日志级别 CRITICAL、FATAL、ERROR、WARNING、WARN、INFO、DEBUG、NOTSET、
log_level = config.get_log('log_level')
# 函数时间消耗日志打印类型 file 打印到文件; close 关闭
time_log_print_type = config.get_log('time_log_print_type')
# 函数时间消耗日志保存目录路径
time_log_print_dir = config.get_log('time_log_print_dir')



