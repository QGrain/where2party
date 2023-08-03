import json
import requests
from private_config import *
from utils import *


g_region = ''
MAX_DIS_BIAS = 100


def get_loc_from_sugguestion(query, region):
    '''
    输入:
        query: 待查询的地址, 如某某小区
        region: 地区, 如北京、武汉等等
    返回值:
        lat, lng, address_name
    '''
    r_text = req_get(url='https://api.map.baidu.com/place/v2/suggestion?query=%s&region=%s&city_limit=true&output=json&ak=%s'%(query, region, baidu_ak))
    r_dict = json.loads(r_text)
    if r_dict['status'] == 0:
        if len(r_dict['result']) == 0:
            raise ValueError('status: 0, message: ok, len of result is 0')
        return r_dict['result'][0]['location']['lat'], r_dict['result'][0]['location']['lng'], r_dict['result'][0]['name']
    else:
        raise ValueError('status: %d, message: %s'%(r_dict['status'], r_dict['message']))


def get_loc_from_addr(struct_addr):
    '''
    输入:
        struct_addr: 标准结构化地址, 如 北京市XX区XX街道XX路XX号
    返回值:
        lat, lng, confidence, comprehension
    '''
    r_text = req_get(url='https://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=%s'%(struct_addr, baidu_ak))
    r_dict = json.loads(r_text)
    if r_dict['status'] == 0:
        return r_dict['result']['location']['lat'], r_dict['result']['location']['lng'], r_dict['result']['confidence'], r_dict['result']['comprehension']
    else:
        raise ValueError('status: %d'%r_dict['status'])


def get_region():
    global g_region
    g_region = input('[-] 请输入所在城市 (如北京、武汉等，回车默认北京): ')
    if g_region == '':
        g_region = '北京'


def get_loc():
    global g_region
    query = input('[-] 请输入地址: ')
    lat1, lng1, addr_name = get_loc_from_sugguestion(query, g_region)
    print('[+] 您的地址信息为: lat: %f, lng: %f, addr_name: %s'%(lat1, lng1, addr_name))

    struct_addr = input('[-] 请输入结构化地址以便精确查询，如北京市海淀区树村路19号 (此选项非必须，按回车键跳过):')
    if struct_addr == '':
        lat2, lng2, confi, compre = 0, 0, 0, 0
    else:
        lat2, lng2, confi, compre = get_loc_from_addr(struct_addr)
        print('[+] 您的地址信息为: lat: %f, lng: %f, confidence: %d, comprehension: %d'%(lat2, lng2, confi, compre))
    if (confi < 50 or compre < 80) and (confi + compre) != 0:
        print('[x] 结构化地址输入不准确，其confidence=%d，comprehension=%d，默认选取前一个地址作为您的地址'%(confi, compre))
        lat2, lng2 = 0, 0

    lat, lng = lat1, lng2
    if (lat2 + lng2) != 0:
        print('[*] 开始解析地址偏差...')
        dis = haversine_distance((lat1, lng1), (lat2, lng2))
        if dis > MAX_DIS_BIAS:
            print('[x] 警告: 两次输入的地址物理距离偏差为%.2f米，大于阈值%d米'%(dis, MAX_DIS_BIAS))
            print('[+] 根据经验，默认选取更精确的结构化地址作为您的地址')
            lat, lng = lat2, lng2
    return lat, lng

if __name__ == '__main__':
    get_region()
    get_loc()