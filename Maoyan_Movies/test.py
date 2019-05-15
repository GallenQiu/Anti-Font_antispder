import requests,re
from bs4 import BeautifulSoup
page=0
offset=page*12
url = 'https://maoyan.com/cinemas?offset={}'.format(offset)
headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"uuid_n_v=v1; uuid=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; _csrf=950aad5c013e2c3ab16ad00f3baf5e95f125e1e65ba45862a8007be7bdd5170d; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16ab924c3c8c8-0cdde02cd5e627-e323462-fa000-16ab924c3c8c8; _lxsdk=3D69540076B211E9BD3EF50F6735917591EBA6065D204C56943F0DA29FD84CBC; __mta=144137482.1557884355695.1557888314569.1557890189406.11; _lxsdk_s=16ab97dc678-25d-a2e-5c0%7C%7C2",
"Host":"maoyan.com",
"Referer":"https://maoyan.com/films",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",}
response = requests.get(url,headers=headers)
print(response.encoding)
soup=BeautifulSoup(response.text,'lxml')
# print(soup.original_encoding)
cinema_cell=soup.select('.cinemas-list .cinema-cell')
lis=[]
for cell in cinema_cell:
    li=[]
    name=cell.select('.cinema-info a')[0].text
    addr = cell.select('.cinema-info p')[0].text

    price= cell.select('.price')[0].text.replace('\n','\\').replace('\\','')
    # for p in price:

    li.extend([name,addr,price])
    lis.append(li)
for li in lis:
    print(li)
    data=li[2]
    pattern = re.compile(r'(u([A-Za-z0-9]{4}))')  # 查找密码
    result1 = pattern.findall(data.replace('\\', ''))
    # print(data.encode('unicode-escape'))
    c = 0
    price_real=''
    while True:
        try:
            da = data[c]
            try:
                a = da.encode('gbk').decode('gbk')
                # print(a)
            except:
                a = str(da.encode('unicode-escape')).replace('b\'\\\\', '').replace('\'', '')[-4:]
                # print(a)
            price_real+=a
            c += 1
        except:
            break
    li[2]=price_real
    print(li)





