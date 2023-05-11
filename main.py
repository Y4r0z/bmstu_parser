from parse.webParser import WebParser
import logging as log
from dotenv import load_dotenv, find_dotenv

from debug.timer import Timer

"""
Данная программа парсит всё содержимое сайта.
В будущем она будет использоваться лишь для парсинга определенных объектов.
"""

def main():
    load_dotenv(find_dotenv())
    #filename='data/app_logs.txt', encoding='utf-8', 
    log.basicConfig(level=log.WARNING)
    wb = WebParser()
    wb.start()

if __name__ == '__main__':
    main()