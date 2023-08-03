import requests
from fake_useragent import UserAgent
from requests.exceptions import RequestException
from math import radians, sin, cos, sqrt, atan2


ua = UserAgent()


def req_get(url):
    max_try = 3
    try_cnt = 0
    while try_cnt < max_try:
        try_cnt += 1
        try:
            random_header = {'User-Agent': ua.random}
            r = requests.get(url=url, headers=random_header)
            if r.status_code == 200:
                return r.text
        except RequestException as e:
            print('[Exception] %s. Retry.'%e)
    return ''


def haversine_distance(coord1, coord2):
    # 将经纬度转换成弧度
    lat1, lng1 = radians(coord1[0]), radians(coord1[1])
    lat2, lng2 = radians(coord2[0]), radians(coord2[1])

    # 计算纬度和经度的差
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # 使用哈弗辛公式计算地球上两点之间的距离
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # 地球的半径（单位：米）
    r = 6371.0 * 1000

    distance = r * c
    # print('[+] 地址偏差距离为 %.2f 米'%distance)
    return distance