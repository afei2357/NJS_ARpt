import  logging
logging.basicConfig(filename="test.log", filemode="a", format="%(asctime)s %(filename)s/%(lineno)d %(levelname)s: %(message)s", datefmt="%Y-%M-%d %H:%M:%S",level=logging.DEBUG)


logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')



a = 5
b = 0
try:
    c = a / b
except Exception as e:
    # 下面三种方式三选一，推荐使用第一种
    # logging.exception("Exception occurred")
    logging.exception(e)
