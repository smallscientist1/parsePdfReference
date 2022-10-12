# DLP2022 Lab1
## 软件代码
### file_io
PDFReader类: 用于解析pdf文件, 提取出其中有关参考文献的部分
- PDFReader.\__init\__(file_path, passwd): 输入需要解析的pdf文件名和密码(若有),创建一个PDFReader对象
- PDFReader.extract_pdf():提取出pdf文件中的文字,找到Reference的部分,以字符串形式返回;
- PDFReader.parse_pdf():调用extract_pdf(), 并对其返回的Reference字符串进行正则表达式匹配, 提取出每条参考文献的信息。

### DownloadAPI
Download bib file from online database
本项目支持从crossref与dblp两个数据库下载bib文件,默认使用crossref
#### crossref
crossref类:
使用 `https://www.crossref.org `提供的API `https://api.crossref.org/works` 下载参考文献的bib文件
- crossref.\__init\__(file_list, headers=None): 输入需要下载的文件列表,http请求的头部, 创建一个crossref对象
- crossref.export_Bib_file(self, export_path,score=70.0): 下载导出bib文件. `export_path`为导出bib文件的路径;`score`为搜索结果匹配阈值, 若搜索结果的匹配程度(由crossref返回)低于score, 则不导出。
- crossref.get_file_address(article_name: str, score=70.0):输入搜索的内容, 返回对应bib文件的下载地址
