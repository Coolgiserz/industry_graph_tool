"""
日志工具
"""
import logging

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def create_logger(app_name, logfilename=None, level=logging.INFO, console=False, logdb=False):
    """
    1. 创建logger对象
    2. 配置处理程序（控制台、文件、套接字）
    3. 设置日志级别
    4. 格式化日志消息
    :param app_name:
    :param logfilename:
    :param level:
    :param console:
    :return:
    """
    log = logging.getLogger(name=app_name)
    log.setLevel(level)
    if logfilename is not None:
        log.addHandler(logging.FileHandler(logfilename))
    if console:
        log.addHandler(logging.StreamHandler())
    # 格式化
    formatter = logging.Formatter(
        f"{log.name} [%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s-%(lineno)s] [%(message)s]",
        datefmt=DATE_FORMAT)
    for handle in log.handlers:
        handle.setFormatter(formatter)
    return log


# class LogDAO(BusinessDAO):
#     pass

PROPERTY_TASK_ID = "task_id"
PROPERTY_IMAGE_ID = "image_id"

