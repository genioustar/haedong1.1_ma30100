# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, calc
import log_result as res
import define as d
timestamp = None
def is_it_OK(subject_code, current_price):
    mesu_medo_type = None
    false = {'신규주문': False}

    if calc.data[subject_code]['idx'] < 300:
        return false

    if subject.info[subject_code]['상태'] == '매수중' or subject.info[subject_code]['상태'] == '매도중' or \
                    subject.info[subject_code]['상태'] == '청산시도중' or subject.info[subject_code]['상태'] == '매매시도중':
        log.debug('신규 주문 가능상태가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        print('신규 주분 가능상태 ㄴㄴ')
        return false

    if subject.info[subject_code]['반대매매'] == True:
        print("반대매매")
        return false

    ## waterfall code ##

    if subject.info[subject_code]['워터폴매매'] == False and subject.info[subject_code]['워터폴매매상태'] == '대기':
        #급락했을때
        if (calc.data[subject_code]['고가'][-80] - calc.data[subject_code]['저가'][-1]) / subject.info[subject_code]['단위'] > 85:

            subject.info[subject_code]['워터폴매매'] = True
            subject.info[subject_code]['워터폴매매상태'] = '매수대기'
            log.info("급락 확인!  워터폴 매수대기 상태로 변경")
            subject.info[subject_code]['워터폴매매틱'] = int((calc.data[subject_code]['고가'][-80] - calc.data[subject_code]['저가'][-1]) / subject.info[subject_code]['단위']* 0.4)


        #급등했을때
        elif (calc.data[subject_code]['고가'][-1] - calc.data[subject_code]['저가'][-80]) / subject.info[subject_code]['단위'] > 85:

            subject.info[subject_code]['워터폴매매'] = True
            subject.info[subject_code]['워터폴매매상태'] = '매도대기'
            log.info("급등 확인! 워터폴 매도대기 상태로 변경")
            subject.info[subject_code]['워터폴매매틱'] =  int((calc.data[subject_code]['고가'][-1] - calc.data[subject_code]['저가'][-80]) / subject.info[subject_code]['단위'] * 0.4)

        else:
            return false


    elif subject.info[subject_code]['워터폴매매'] == True:
        if subject.info[subject_code]['워터폴매매상태'] == '매도대기':
            #if is_it_blue_candle(subject_code) == True:
                #subject.info[subject_code]['워터폴매매틱'] = int(((calc.data[subject_code]['고가'][-5] - current_price) / subject.info[subject_code]['단위']) * 0.5 ) #급등한 격차의 반 * 0.7(보수적으로잡음)
            mesu_medo_type = '신규매도'
            #else:
            #    log.info("워터풀 매도 대기중으로 음봉이 나올때까지 대기합니다.")
            #    return false

        elif subject.info[subject_code]['워터폴매매상태'] == '매수대기':
            #if is_it_red_candle(subject_code) == True:
                #subject.info[subject_code]['워터폴매매틱'] = int(((current_price - calc.data[subject_code]['저가'][-5]) / subject.info[subject_code]['단위']) * 0.5 ) #급락한 격차의 반 * 0.7(보수적으로잡음)
            mesu_medo_type = '신규매수'
            #else:
            #    log.info("워터풀 매수 대기중으로 양봉이 나올때까지 대기합니다.")
            #    return false

    else:
        log.error("unknown error")
        return false

    if subject.info[subject_code]['워터폴매매틱'] < 5:
        log.info("워터폴 익절틱, 손절틱이 5틱 이하로 매매안합니다.")
        return false
    if subject.info[subject_code]['워터폴매매틱'] > 0:
        pass
        #log.info("워터폴매매틱 =%s" % subject.info[subject_code]['워터폴매매틱'])
    profit_tick = subject.info[subject_code]['워터폴매매틱']
    sonjal_tick = subject.info[subject_code]['워터폴매매틱']
    #profit_tick = 20
    # sonjal_tick = 15
    # contract_cnt = 2
    if d.get_mode() == d.REAL:  # 실제 투자 할때
        possible_contract_cnt = int(contract.my_deposit / subject.info[subject_code]['위탁증거금'])
        contract_cnt = int(contract.my_deposit / 1.2 / subject.info[subject_code]['위탁증거금'])
        if contract.recent_trade_cnt == possible_contract_cnt:
            contract_cnt = possible_contract_cnt
        log.info("매매 예정 수량은 %s개 입니다." % contract_cnt)
        contract_cnt = 2
    else:
        contract_cnt = 2  # 테스트 돌릴때

    log.debug("종목코드(" + subject_code + ") 신규 매매 계약 수 " + str(contract_cnt))


    if mesu_medo_type == None :
        # print('매매타입이 없음')
        return false
    if contract_cnt == 0: return false

    subject.info[subject_code]['신규매매수량'] = contract_cnt
    order_contents = {'신규주문': True, '매도수구분': mesu_medo_type, '익절틱': profit_tick, '손절틱': sonjal_tick, '수량': contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('waterfall.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)

    if mesu_medo_type == '신규매수': subject.info[subject_code]['워터폴매매상태'] = '매수중'
    elif mesu_medo_type == '신규매도': subject.info[subject_code]['워터폴매매상태'] = '매도중'

    global timestamp

    # log.info('워터폴 시간 체크 진입 전')
    if timestamp == None:
        # log.info('워터폴 시간값이 없음')
        pass
    else :
        # log.info('워터폴 시간 값 : ' + str(timestamp))
        if abs(int(get_time(0,subject_code))-int(timestamp)) >=500 :
            timestamp = get_time(0,subject_code)
            print('timestamp 갱신')
            pass
        else :
            # log.info('매매후 5분이 지나지 않아 매매포기')
            subject.info[subject_code]['워터폴매매상태'] ='대기'
            subject.info[subject_code]['워터폴매매'] = False
            return false
    timestamp = get_time(0,subject_code)

    return order_contents



def is_it_sell(subject_code, current_price):

    false = {'신규주문': False}
    try:
        if subject.info[subject_code]['워터폴매매'] == False: return false
        if contract.get_contract_count(subject_code) > 0:
            # 계약 보유중
            # log.debug("종목코드(" + subject_code + ") is_it_sell() / 보유 계약 : " + str(contract.get_contract_count(subject_code)))
            if contract.list[subject_code]['매도수구분'] == '신규매수':
                # 매수일때

                if current_price <= contract.list[subject_code]['손절가']:
                    res.info("워터폴 손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                    waterfall_init(subject_code)
                    return {'신규주문': True, '매도수구분': '신규매도', '수량': contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}


                elif current_price > contract.list[subject_code]['익절가']:
                    res.info("워터폴 익절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                    waterfall_init(subject_code)
                    return {'신규주문': True, '매도수구분': '신규매도', '수량': contract.list[subject_code]['계약타입'][contract.SAFE] +
                                                                 contract.list[subject_code]['계약타입'][contract.DRIBBLE]}

            elif contract.list[subject_code]['매도수구분'] == '신규매도':
                # 매도일때

                if current_price >= contract.list[subject_code]['손절가']:
                    res.info("워터폴 손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                    waterfall_init(subject_code)
                    return {'신규주문': True, '매도수구분': '신규매수','수량': contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}

                elif current_price < contract.list[subject_code]['익절가']:
                    res.info("워터폴 익절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                    waterfall_init(subject_code)
                    return {'신규주문': True, '매도수구분': '신규매수','수량': contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}

    except Exception as err:
        log.error(err)

    return {'신규주문': False}

def waterfall_init(subject_code):
    subject.info[subject_code]['워터폴매매상태'] = '대기'
    subject.info[subject_code]['워터폴매매'] = False
    subject.info[subject_code]['워터폴매매틱'] = 10



def is_it_red_candle(subject_code):
    jonga = calc.data[subject_code]['현재가'][-1]
    siga = calc.data[subject_code]['시가'][-1]

    if jonga - siga > 0:
        return True
    else:
        return False


def is_it_blue_candle(subject_code):
    jonga = calc.data[subject_code]['현재가'][-1]
    siga = calc.data[subject_code]['시가'][-1]

    if siga - jonga > 0:
        return True
    else:
        return False


def get_time(add_min, subject_code):
    # 현재 시간 정수형으로 return
    if d.get_mode() == d.REAL:  # 실제투자
        current_hour = time.localtime().tm_hour
        current_min = time.localtime().tm_min
        current_min += add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour * 100 + current_min

    elif d.get_mode() == d.TEST:  # 테스트
        current_hour = int(str(calc.data[subject_code]['체결시간'][-1])[8:10])
        current_min = int(str(calc.data[subject_code]['체결시간'][-1])[10:12])
        current_min += add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour * 100 + current_min

        current_time = int(str(calc.data[subject_code]['체결시간'][-1])[8:12])

    return current_time
