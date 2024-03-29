'''
기상청 API 를 이용하여, 날씨 정보 호출
'''

import requests
from datetime import datetime
import xmltodict
import pandas as pd

def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour_string():
    now = datetime.now()
    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2330"
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"

    return base_time

def forecast():
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url, params = params)
    # print(res)
    #XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    #값 가져오기
    weather_data = dict()
    for item in dict_data['response']['body']['items']['item']:
        # 기온
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['fcstValue']
        # 습도
        if item['category'] == 'REH':
            weather_data['hum'] = item['fcstValue']
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item['category'] == 'PTY':
            weather_data['sky2'] = item['fcstValue']
        weather_data['fcstDate'] = item['fcstDate']
        weather_data['fcstTime'] = item['fcstTime']

    return weather_data

def xlsopen(location:str):
    "위경도값을 X, Y 좌표로 반환"
    file_name = 'weather\위경도xy.xlsx'

    df = pd.read_excel(file_name)
    search = df[df['1단계'].str.contains(location)|df['2단계'].str.contains(location)|df['3단계'].str.contains(location)]
    return search

def proc_weather():
    dict_sky = forecast()

    str_sky = location + " "
    if dict_sky['sky'] != None or dict_sky['sky2'] != None:
        str_sky = str_sky + "날씨 : "
        if dict_sky['sky2'] == '0':
            if dict_sky['sky'] == '1':
                str_sky = str_sky + "맑음"
            elif dict_sky['sky'] == '3':
                str_sky = str_sky + "구름많음"
            elif dict_sky['sky'] == '4':
                str_sky = str_sky + "흐림"
        elif dict_sky['sky2'] == '1':
            str_sky = str_sky + "비"
        elif dict_sky['sky2'] == '2':
            str_sky = str_sky + "비와 눈"
        elif dict_sky['sky2'] == '3':
            str_sky = str_sky + "눈"
        elif dict_sky['sky2'] == '5':
            str_sky = str_sky + "빗방울이 떨어짐"
        elif dict_sky['sky2'] == '6':
            str_sky = str_sky + "빗방울과 눈이 날림"
        elif dict_sky['sky2'] == '7':
            str_sky = str_sky + "눈이 날림"
        str_sky = str_sky + "\n"
    if dict_sky['tmp'] != None:
        str_sky = str_sky + "온도 : " + dict_sky['tmp'] + 'ºC \n'
    if dict_sky['hum'] != None:
        str_sky = str_sky + "습도 : " + dict_sky['hum'] + '% \n'

    if dict_sky['fcstDate'] != None:
        str_sky = str_sky + "날짜 : " + dict_sky['fcstDate'] + ' \n'
    if dict_sky['fcstTime'] != None:
        str_sky = str_sky + "시간 : " + dict_sky['fcstTime'] + ' \n'
    return str_sky
    
if __name__ == '__main__':
    # 지역명을 기준으로 x, y 좌표 취득
    location = input('지역 : ')
    df = xlsopen(location)

    keys = 'mPe5507lVJZkfJMjxR1h5Wi/hU67x7qcgG75ZJn1wd5U46niRp+5ouWNzUOiujcJfqrExmfvo5qf2iYaWjGtNQ=='
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params ={'serviceKey' : keys, 
            'pageNo' : '1', 
            'numOfRows' : '1000', 
            'dataType' : 'XML', 
            'base_date' : get_current_date_string(), 
            'base_time' : get_current_hour_string(), 
            'nx' : str(df['격자 X'].iloc[0]), 
            'ny' : str(df['격자 Y'].iloc[0]) }
    
    print(proc_weather())
    print(params)
