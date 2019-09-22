# -*- coding : utf-8 -*- #

__author__ = "Gallen_qiu"
import requests,json,re
from fontTools.ttLib import TTFont
import xml.etree.ElementTree as et

'''在html中搜索myFont,找到对应的woff字体文件，下载下来，转成xml'''
def initialize_woff():
    while True:
        try:
            response = requests.get('https://www.shixiseng.com/interns?page=10&keyword=%E6%95%B0%E6%8D%AE%E5%BA%93&type=intern&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend=',timeout=5)
            i=r'@font-face{font-family:myFont;src:url((.*?));}'
            base64_code=re.findall(i,response.text.replace(' ',''))[0][0].replace('(','').replace(')','')
            print(base64_code)
            # base64_code='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'
            wofffile = requests.get('https://www.shixiseng.com' + str(base64_code))

            with open('字体.woff', 'wb')as f:
                f.write(wofffile.content)
            font1 = TTFont('字体.woff')
            font1.saveXML('字体.xml')
            break
        except requests.exceptions.RequestException:
            print('Retry woff!')
            initialize_woff()

'''在xml文件中创建索引——解密模块'''
def parse_woff(qcode):
    '''
    传入qcode，格式：长度为4的密文：xeb25
    :param qcode:
    :return:
    '''
    qcode="0"+qcode
    root = et.parse('字体.xml').getroot()
    map_ele = root.find('cmap').find('cmap_format_4').findall('map')
    map_dict = {}
    # 把map那一堆数据存到字典中
    for m in map_ele:
        # code = m.attrib['code'].replace('0x', '')
        # print(m.attrib['name'])
        # print(m.attrib['code'])
        if m.attrib['code']== qcode:
            vaule = m.attrib['name'][-1]
            return vaule

'''请求数据，调用解密模块解密加密的数据'''
def req():
    url='https://www.shixiseng.com/app/interns/search/v2?build_time=1569124722750&page=3&keyword=%E6%95%B0%E6%8D%AE%E5%BA%93&type=intern&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend='
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.shixiseng.com",
        "If-None-Match": 'W/"02d6c2c96e9590c77f0f8cb9a908f8b59a64e114"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    }
    response=requests.get(url,headers=headers)
    data=json.loads(response.text)["msg"]["data"]
    for d in data:
        ms=''
        for  i in d["minsal"].split("&#"):
            if i !='':
                ms+=str(parse_woff(i))
        mas = ''
        for i in d["maxsal"].split("&#"):
            if i != '':
                mas += str(parse_woff(i))
        print(d["cname"],'工资：{}-{}/天'.format(ms,mas))

if __name__ == '__main__':

    initialize_woff()
    req()