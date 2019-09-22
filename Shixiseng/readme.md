#实习僧网站：https://www.shixiseng.com
#好久之前的做过一个，也是字体反爬虫，不过今天看了一下，发现策略改进了
#过去的策略：自定义字体反爬虫，通过base64加密字段，直接放在html页面里，匹配规则也很简单，ttf文件里面有直接的映射关系
#现在的策略：Html里面有myFont自定义字体，需要再次请求url获得woff字体文件，这次采用的是glygh的映射，映射关系是：网页密文-字体密文-字体图像（就是用点阵来描述文字）

#爬虫的反反机制：获取woff文件-通过字体密文设置映射字典-请求加密数据-解密
#怎么看到映射关系呢？：下载FontCreater，把woff文件拖进去，就会看到对应关系。打开xml文件可以看到网页密文和字体密文的映射关系。

#理论上，这种点阵文字破解总要手动设置字典，所以如果他后台的woff文件时多个或者是随机，那就比较麻烦了，不过我还没发现这种情况。