# -*- coding: utf-8 -*-

mode = None # 현재 모드
REAL = 1    # 실제 투자
TEST = 2    # 테스트 프로그램
DB = 3      # DB 수집

PRODUCT_CNT = 5 # ['MTL','ENG','CUR','IDX','CMD']
RECEIVED_PRODUCT_COUNT = 0 # 현재 받은 상품 정보들

CANDLE = 'candle'
MA = '이동평균선'
WEEK = '주'
DAY = '일'
BOLLINGER_BAND = '볼린저밴드'

DATE = 'date'
HIGH = 'high'
LOW = 'low'
OPEN = 'open'
CLOSE = 'close'
VOLUME = 'volume'

def get_mode():
    return mode