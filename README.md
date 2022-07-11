# crawl_foreign_business_data

使用scrapy抓取国外商业数据

# 抓取方案

    该网站与国内顺企网类似，
    公司详情页可通过不同检索方式获得

### 俄罗斯企业信息网

- 通过 [俄罗斯企业信息](https://www.rusprofile.ru/) 的（ClassName("letter-list")[1].下的a标签） 获得所有字母列表页（共31个字母分类）

- 其中分类页中每页最多9937*100（90w）个家公司详情页 其中分类页面命名规则均是 [/ip/字母 ‘/ip/А’](/ip/А)
  以[A 开头 ‘https://www.rusprofile.ru/ip/A’](https://www.rusprofile.ru/ip/%D0%90) 为例

- 其中公司详情页命名规则是 "/ip/一串id" [以 "/ip/311471627700048" ](https://www.rusprofile.ru/ip/311471627700048) 为例

### 西班牙企业信息网

- [西班牙企业信息](https://empresite.eleconomista.es/)
- 该网站解析过程：通过分类列表中获得抓取所有a标签下的链接， 并在pipelines中对所有链接进行分类，将分类链接、分页链接、公司详情页等存到不同的redis中， 分类链接中均存在‘provincia’
  ‘Actividad’字段，企业详情链接均以‘https://empresite.eleconomista.es’开头， 企业名称(大写字母)结尾的。

### 新西兰 澳大利亚

- [新西兰](https://www.nzlbusiness.com/) 与 [澳大利亚](https://www.aus61business.com/)
  是一家网站提供，结构相同。 通过首字母索引进行分类，并在每一次抓取中将分页链接以及公司详情页分别存到所对应的redis中，

### 新加坡企业信息网

- [新加坡](https://www.sgpbusiness.com/activities/industrial-classification/)
  该网站请求中设置了Google验证，所以目前选用自动化工具来完成， 思路仍然是通过不同链接的区别进行区分，最终遍历解析详情页。

### 使用命令行运行爬虫文件

- 使用cmdline前，确保settings中的对应pipeline配置处于打开状态。

### 公司详细信息结构

- 俄罗斯

  ```json

  {
  "page_code": "<page_code>",
  "Название компании":"ИПМещеряковДмитрийАндреевич",
  "Гражданство": "РФ",
  "Пол": "мужской",
  "ОГРНИП": "314132716000015",
  "ИНН": "132709043698",
  "Дата регистрации": "9июня2014г.",
  "Регион": "РеспубликаМордовия",
  "Вид предпринимательства": "Индивидуальныйпредприниматель",
  "Регистратор": "УПРАВЛЕНИЕМИНИСТЕРСТВАРОССИЙСКОЙФЕДЕРАЦИИПОНАЛОГАМИСБОРАМПОРЕСПУБЛИКЕМОРДОВИЯ",
  "Дата постановки на учёт": "9июня2014г." 
  }

  ```
- Spain

  ```json
  {
  "Razón Social": "Olam Assessors Sl",
  "page_code": "<page_code>",
  "CIF": "B63713879", 
  "Domicilio Social": "ESPAÑA Paseo Garcia i Faria, 69 - 9 2, Barcelona, 08019 , barcelona ¿Cómo llegar?", 
  "Objeto Social": "Servicios de consultoria en relacion con las actividades de desarrollo, adquisicion, gestion y explotacion de residencias para personas de la tercera edad y de la salud mental.etc", 
  "Forma jurídica": "Sociedad limitada", 
  "Actividad": "Servicio de gestión administrativa", 
  "Actividad CNAE": "8219 - Actividades de fotocopiado, preparación de documentos y otras actividades especializadas de oficinaConsulta los datos comerciales y CIF de Olam Assessors Sl", 
  "Grupo Sector": "Servicios empresariales", 
  "Cargos": "Encontrados 2 cargos en esta empresa Ver cargos de Olam Assessors Sl", 
  "Rango de Ventas": "Menor de 300 mil €"
  }
  ```

- Other (Australia or NewZealand)

  ```json
  {
  "country": "Australia or NewZealand",
  "page_code": "<page_code>",
  "ACN": "660416044", 
  "Company Name": "A &amp; A HAM PTY LTD", 
  "Entity Type": "A private Australian company is not listed on the stock exchange and is not included in the description of Australian public company or cooperative.", 
  "Company Class": "The liability of the members is limited to the amount unpaid on their shares. Shareholders are not required to contribute any further monies (in the case of a winding up) if the shares they have taken up are fully paid.", 
  "Company Sub-class": "Proprietary Other", 
  "Status": "REGISTERED", 
  "Date of Registration": "23 June 2022, Thursday"
  }
  ```