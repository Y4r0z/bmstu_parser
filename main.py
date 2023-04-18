from parse.webParser import WebParser
import logging as log
from dotenv import load_dotenv, find_dotenv

def main():
    load_dotenv(find_dotenv())
    #filename='data/app_logs.txt', encoding='utf-8', 
    log.basicConfig(level=log.ERROR)
    wb = WebParser()
    wb.start()


if __name__ == '__main__':
    main()