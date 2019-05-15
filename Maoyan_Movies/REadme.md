猫眼电影爬虫
===========================
注：目前测试的是电影院页面的信息：https://maoyan.com/cinemas
###########环境依赖

            python3
            依赖库：requests
            MongoDB/Mysql

###########操作步骤

            1. 执行run  

            2. 配置run.py文件：
                        main函数修改地区
                        
###########网站字体反爬策略

     网页中采取自定义字体：'stonefont'(可能自认为很顽固吧)对电影院的价格进行替换加密，位置在网页html的：      (//vfile.meituan.net/colorstone/ace4a85721374e3d55f9c7edb4b797b62076.woff)第三个url
            
            @font-face {
      font-family: stonefont;
      src: url('//vfile.meituan.net/colorstone/4dc54293aa2cd9011d5157a0719855183168.eot');
      src: url('//vfile.meituan.net/colorstone/4dc54293aa2cd9011d5157a0719855183168.eot?#iefix') format('embedded-opentype'),
           url('//vfile.meituan.net/colorstone/ace4a85721374e3d55f9c7edb4b797b62076.woff') format('woff');
    }
    
    直接获取url下载可以得到字体woff格式文件，用fontTools库进行解析，解析成xml文件：
        xml文件中观察到映射信息：网页的加密文字（&#xe64f）——》uniE64F——》id——》TTGlyph.最终形成的是一个点阵图，理论上价格数字就是图片，但机智的我发现了TTGlyph中的xMax结合第一个点阵信息可以作为唯一识别信息，所以自已写了新的映射表。从而避免OCR。
    其余的操作不是难度，不再赘述。
    
###########版本信息
  
    v1.00 草稿版 （等到我某天要分析电影院的数据时我会再写个完整版：包括多线程、多进程、入库之类）
