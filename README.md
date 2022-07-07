# crawl_foreign_business_data
使用scrapy抓取国外商业数据


# 抓取方案

    该网站与国内顺企网类似，
    公司详情页可通过不同检索方式获得

### 俄罗斯企业信息网

- 通过 [俄罗斯企业信息](https://www.rusprofile.ru/) 的（ClassName("letter-list")[1].下的a标签） 获得所有字母列表页（共31个字母分类）

- 其中分类页中每页最多9937*100（90w）个家公司详情页 其中分类页面命名规则均是 [/ip/字母 ‘/ip/А’](/ip/А)  以[A 开头 ‘https://www.rusprofile.ru/ip/A’](https://www.rusprofile.ru/ip/%D0%90) 为例

- 其中公司详情页命名规则是 "/ip/一串id" [以 '/ip/311471627700048' ](https://www.rusprofile.ru/ip/311471627700048) 为例

### 西班牙企业信息网 

- [西班牙企业信息](https://empresite.eleconomista.es/) 
- 该网站解析过程：通过分类列表中获得抓取所有a标签下的链接，
并在pipelines中对所有链接进行分类，将分类链接、分页链接、公司详情页等存到不同的redis中，
分类链接中均存在‘provincia’ ‘Actividad’字段，企业详情链接均以‘https://empresite.eleconomista.es’开头，
企业名称(大写字母)结尾的。


### 新西兰 澳大利亚

- [新西兰](https://www.nzlbusiness.com/) 与 [澳大利亚](https://www.aus61business.com/) 
是一家网站提供，结构相同。
通过首字母索引进行分类，并在每一次抓取中将分页链接以及公司详情页分别存到所对应的redis中，


### 新加坡企业信息网

- [新加坡](https://www.sgpbusiness.com/activities/industrial-classification/) 
该网站请求中设置了Google验证，所以目前选用自动化工具来完成，
思路仍然是通过不同链接的区别进行区分，最终遍历解析详情页。


#### 使用命令行运行爬虫文件