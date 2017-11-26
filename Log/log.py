import logging

logging.basicConfig(
    level=logging.DEBUG,                # 设置日志级别，只有高于设置级别的日记会被记录
    format='%(asctime)s [file: %(filename)s] [line: %(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',    # 设置日期输出格式，必须现在 format 中设置日期输出，否则无效
    filename='logging.log',             # 如果设置了 filename，日志就会被输出到文件而不是标准输出
    filemode='w',                       # 写入日志到文件的模式
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')