from fontTools.ttLib import TTFont
import requests,re,json
from bs4 import BeautifulSoup

class Maoyan:
    def __init__(self,name):
        self.name=name
        self.page_max=0
        self.ci=0
    def reseach(self):
        city_ci = {}
        with open('city_code.json', 'r', encoding='utf8')as f:
            city_dict = json.loads(f.read())
        for capit in city_dict['letterMap']:
            for city in city_dict['letterMap'][capit]:
                city_ci[city['nm']] = city['id']
        self.ci= city_ci[self.name]

    def scheduler(self):
        self.reseach()
        self.initializer()
        for page in range(0,int(self.page_max)+1):
            self.parser(page)
    def parser(self,page):
        offset = page * 12
        url = 'https://maoyan.com/cinemas?offset={}'.format(offset)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "ci={};uuid_n_v=v1; uuid=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; _csrf=950aad5c013e2c3ab16ad00f3baf5e95f125e1e65ba45862a8007be7bdd5170d; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16ab924c3c8c8-0cdde02cd5e627-e323462-fa000-16ab924c3c8c8; _lxsdk=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; __mta=144137482.1557884355695.1557888314569.1557890189406.11; _lxsdk_s=16ab97dc678-25d-a2e-5c0%7C%7C2".format(self.ci),
            "Host": "maoyan.com",
            "Referer": "https://maoyan.com/films",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        }
        response = requests.get(url, headers=headers)

        '''下载解密文件'''
        i = r"url\('(.*?)'\)format\('woff'\);"
        woff = re.findall(i, response.text.replace(' ', ''))
        wofffile = requests.get('https:' + str(woff[0]))
        with open('猫眼电影.woff', 'wb')as f:
            f.write(wofffile.content)
        font1 = TTFont('猫眼电影.woff')
        font1.saveXML('猫眼电影.xml')
        '''下载解密文件'''

        soup = BeautifulSoup(response.text, 'lxml')

        cinema_cell = soup.select('.cinemas-list .cinema-cell')
        lis = []
        for cell in cinema_cell:
            li = []
            name = cell.select('.cinema-info a')[0].text
            addr = cell.select('.cinema-info p')[0].text

            price = cell.select('.price')[0].text.replace('\n', '\\').replace('\\', '')
            # for p in price:

            li.extend([name, addr, price])
            lis.append(li)
        for li in lis:
            data = li[2]
            c = 0
            price_real = ''
            while True:
                try:
                    da = data[c]
                    try:
                        a = da.encode('gbk').decode('gbk')
                    except:
                        qcode = str(da.encode('unicode-escape')).replace('b\'\\\\', '').replace('\'', '')[-4:]
                        a = self.qq(qcode)
                    price_real += str(a)
                    c += 1
                except:
                    break
            li[2] = price_real
            print(li)


    def initializer(self):
        '''下载解密的字体库，并base解密保存为‘字体.ttf’,再用TTFont进一步转化成xml文件'''
        '''返回该分类下总页面的数量'''
        url = 'https://maoyan.com/cinemas?offset=0'
        headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Cookie":"ci=10;uuid_n_v=v1; uuid=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; _csrf=950aad5c013e2c3ab16ad00f3baf5e95f125e1e65ba45862a8007be7bdd5170d; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16ab924c3c8c8-0cdde02cd5e627-e323462-fa000-16ab924c3c8c8; _lxsdk=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; __mta=144137482.1557884355695.1557888314569.1557890189406.11; _lxsdk_s=16ab97dc678-25d-a2e-5c0%7C%7C2",
    "Host":"maoyan.com",
    "Referer":"https://maoyan.com/films",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",

        }
        response = requests.get(url,headers=headers)
        p=r'<aclass=".*?"href=".*?">(.*?)</a>'
        pp=re.findall(p, response.text.replace(' ', '').replace('\n', ''))
        # print(pp)
        if pp == []:
            self.page_max  = 1
        else:
            self.page_max=pp[-2]
        print('Max page：{}'.format(self.page_max))

    def qq(self,qcode):
        qcode='uni'+qcode.upper()
        import xml.etree.ElementTree as et
        root = et.parse('猫眼电影.xml').getroot()
        # 找到map那一堆标签(PyQuery)
        TTGlyph_ele = root.find('glyf').findall('TTGlyph')
        TTGlyph_dict = {}
        # 把map那一堆数据存到字典中
        v_dict={
        '373':1,
        '503':2,
        '641':3,
        '831':4,
        '516':5,
        '510':6,
        '558':7,
        '689':8,
        '651':9,
        '550':0
        }
        '''
        1 373
        2 503
        3 511 130 641
        4 508 323 831
        5 516
        6 510
        7 511 47  558
        8 512 177 689
        9 512 139 651
        0 508 42  550'''
        for m in TTGlyph_ele:
            code = m.attrib['name']
            if 'uni' in m.attrib['name']:
                x1 = m.findall('contour')[0].findall('pt')[0].attrib['x']
                if int(m.attrib['xMax'])in [511,512,508]:
                    value=int(m.attrib['xMax'])+int(x1)
                else:
                    value = int(m.attrib['xMax'])
                TTGlyph_dict[code]=v_dict[str(value)]


        return TTGlyph_dict[qcode]
if __name__ == '__main__':
    M=Maoyan('深圳')
    M.scheduler()

