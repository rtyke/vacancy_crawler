import logging
import os
import sys


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG,
#     # filename='bot.log',
#     stream=sys.stdout,
# )
#
# my_logger = logging.getLogger()
logger = logging.getLogger('scrapper_logging')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('[%(asctime)s]    %(message)s')
formatter = logging.Formatter('[%(asctime)s]    %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

log = logger.debug
