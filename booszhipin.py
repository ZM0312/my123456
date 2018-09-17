# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 17:17:11 2018

@author: Administrator
"""
import time
from multiprocessing.pool import Pool

import pymongo
import random
import requests
from pyquery import PyQuery as pq


def get_ip():
    IP = [
        {'http:': 'http://139.196.196.74:80'},
        {'http:': 'http://222.33.192.238:8118'},
        {'http:': 'http://219.150.189.212:9999'},
        {'http:': 'http://125.94.0.250:8080'},
        {'http:': 'http://117.90.2.230:9000'},
        {'http:': 'http://124.42.7.103:80'},
        {'http:': 'http://121.69.37.238:8118'},
        {'http:': 'http://121.69.37.238:8118'},
        {'http:': 'http://117.90.3.218:9000'},
        {'http:': 'http://219.150.189.212:9999'},
        {'http:': 'http://124.42.7.103:80'},
    ]
    IP = random.choice(IP)
    return IP

# 此函数用于提取详情页url
def get_href(IP, offes):
    # 设置cookie，UA
    headers = {
        'Cookie': 't=1PcpIpQYhhoilGUh; wt=1PcpIpQYhhoilGUh; sid=sem_pz_bdpc_dasou_title; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1537092367,1537162644; __c=1537162647; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D3%26rsv_bp%3D1%26tn%3Dbaidu%26wd%3Dboos%25E7%259B%25B4%25E8%2581%2598%26oq%3Dboos%2525E7%25259B%2525B4%2525E8%252581%252598%2525E7%2525BD%252591%252520-(boss)%26rsv_pq%3De921548e000444fc%26rsv_t%3D46e0WxbOt16sCyPJb9HY9BnoFC83MKaoCGUltbqwPgZVkNif6OUODMIgq5I%26rqlang%3Dcn%26rsv_enter%3D0%26rsv_sug3%3D2%26rsv_sug1%3D2%26rsv_sug7%3D100%26prefixsug%3Dboos%2525E7%25259B%2525B4%2525E8%252581%252598%26rsp%3D0%26inputT%3D2471%26rsv_sug4%3D3492&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; lastCity=101210100; __a=32380157.1537092423.1537092406.1537162647.50.3.6.6; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1537162722',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    url = 'https://www.zhipin.com/c100010000/h_100010000/?query=python&page=' + offes + '&ka=page-' + offes
    try:
        # 休息一会,频繁访问会弹出验证
        time.sleep(5)
        rep = requests.get(url, headers=headers, proxies=IP, timeout=5)
        if rep.status_code == 200:
            html = rep.text  # 返回结果
            # print(html)
            # 此处使用pyquery来获取详情页的 href 属性
            doc = pq(html)
            a = doc('.job-list > ul > li > .job-primary > .info-primary > .name > a')
            for item in a.items():
                # print(item.attr('href'))
                # 返回提取出的详情页 href
                yield {
                    'href': item.attr('href')
                    }
        return None
    except requests.ConnectionError:
        print('请求索引页出错')
        return None

# 接收详情页的 href，
def get_data(IP, href):
    headers = {
        'cookie': 't=1PcpIpQYhhoilGUh; wt=1PcpIpQYhhoilGUh; sid=sem_pz_bdpc_dasou_title; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1537092367,1537162644; __c=1537162647; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D3%26rsv_bp%3D1%26tn%3Dbaidu%26wd%3Dboos%25E7%259B%25B4%25E8%2581%2598%26oq%3Dboos%2525E7%25259B%2525B4%2525E8%252581%252598%2525E7%2525BD%252591%252520-(boss)%26rsv_pq%3De921548e000444fc%26rsv_t%3D46e0WxbOt16sCyPJb9HY9BnoFC83MKaoCGUltbqwPgZVkNif6OUODMIgq5I%26rqlang%3Dcn%26rsv_enter%3D0%26rsv_sug3%3D2%26rsv_sug1%3D2%26rsv_sug7%3D100%26prefixsug%3Dboos%2525E7%25259B%2525B4%2525E8%252581%252598%26rsp%3D0%26inputT%3D2471%26rsv_sug4%3D3492&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; lastCity=101210100; __a=32380157.1537092423.1537092406.1537162647.50.3.6.6; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1537162722',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    href = href['href']
    # print(href)
    # 此处拼接出真正的详情页 url
    url = 'https://www.zhipin.com' + href
    # print(url)
    try:
        # 此处要多停一会,每次等待时间随机
        time.sleep(random.uniform(3, 30))
        rep = requests.get(url, headers=headers, proxies=IP, timeout=5)
        if rep.status_code == 200:
            data = rep.text
            # 还是用 pyquery 提取所需数据
            doc = pq(data)
            titles = doc('.job-banner > .home-inner > .detail-box')
            title = titles('.info-primary > .name > h1').text()
            # 此处加一步验证，如果没有获取到 title，返回 None,不再继续往下执行
            if not title:
                return None
            pay = titles('.info-primary > .name > .badge').text()
            yaoqiu = titles('.info-primary > p').text()
            city = yaoqiu[3:5]
            jingyan = yaoqiu[8:12]
            xueli = yaoqiu[15:17]
            danwei = titles('.info-company > h3 > a').text()
            guimo = titles('.info-company > p').text()
            body = doc('.job-detail .detail-content .job-sec .text').text()
            yield {
                'title': title,
                'pay': pay,
                'danwei': danwei,
                'city': city,
                'jingyan': jingyan,
                'xueli': xueli,
                'daxiao': guimo,
                'sec': body}
        return None
    except requests.ConnectionError as e:
        print('二次请求索引页出错', e)
        return None

# 此方法用于将数据插入数据库
def save_mongo(data):
    client = pymongo.MongoClient(host='localhost', port=27017)      # 连接数据库
    db = client.test      # 指定数据库
    collection = db.booszhipin      # 指定集合（表）
    booszhipin = {
        'title': data['title'],
        'pay': data['pay'],
        'danwei': data['danwei'],
        'city': data['city'],
        'jingyan': data['jingyan'],
        'xueli': data['xueli'],
        'daxiao': data['daxiao'],
        'sec': data['sec']
    }
    collection.insert_one(booszhipin)
    print('插入成功', booszhipin)

if __name__ == '__main__':
    # pages 为要爬取的页数
    pages = 40
    IP = get_ip()
    for offes in range(1, pages + 1):
        for href in get_href(IP, str(offes)):
            for data in get_data(IP, href):
                save_mongo(data)