import logging
import logging.config

logging.config.fileConfig('logging.ini')
main_logger = logging.getLogger('main')


# root_logger = logging.getLogger('root')
# root_logger.debug('root_logger debug')

# main_logger = logging.getLogger(__name__)

# logging.basicConfig(filename="test.log", filemode="a", format="%(asctime)s %(filename)s/%(lineno)d %(levelname)s: %(message)s", datefmt="%Y-%M-%d %H:%M:%S",level=logging.DEBUG)


# root_logger.debug('This is a debug message')

# root_logger.info('This is an info message')
# root_logger.warning('This is a warning message')
# root_logger.error('This is an error message')
# root_logger.critical('This is a critical message')

main_logger.debug('This is a main debug message')
main_logger.info('This is an  main info message')
main_logger.warning('This is a  main warning message')
main_logger.error('This is an  main error message')
main_logger.critical('This is a  main critical message')


# a = 5
# b = 0
# try:
#     c = a / b
# except Exception as e:
#     # 下面三种方式三选一，推荐使用第一种
#     # logging.exception("Exception occurred")
#     root_logger.exception(e)
