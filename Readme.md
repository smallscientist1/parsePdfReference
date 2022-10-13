# DLP2022 Lab1
## 任务说明
输入一个计算机/电子类文章的 PDF 文件（例如一篇 CVPR 文章，示例中使用`Attention Is All You Need`的PDF文件），解析出所有的参考文献，保存为ref.txt文件，并下载所有的文献的 BIB 文件（可以选择从 crossref或DBLP 下载）

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
#### dblp
dblp类
从`https://dblp.uni-trier.de` 下载参考文献的bib文件。
类接口与crossref相同

### main.py
使用Pyqt5实现的GUI
#### win类
基于PyQt5.QtWidgets.Qdialog的窗口
- win.initUI(): 初始化ui界面,包括设置布局、定义label、定义四个按钮,将信号与对应的槽相连
- win.openpdf(): 点击open按钮调用的槽, 返回要读取的pdf文件地址
- win.savebib(): 点击savepath按钮调用的槽, 返回存储路径
- win.processSlot(): 点击process按钮调用的槽, 新建一个线程来执行核心代码

#### processThread类
基于PyQt5.QtCore.QThread的类，执行核心功能。
- procsssThread.run(): 执行核心功能,即解析pdf,下载参考文献

## 实验难点
### parse_pdf
- 1. 不同的pdf文件可能有不同的格式,例如Reference的位置,条目样式等,对提取参考文献造成困难
解决方案: 在读取时尽量考虑各种情况,包括页眉页脚、参考文献跨页的情况、设计全面的正则表达式匹配等
### DownloadBib
- 1. 搜索bib文件,数据库可能返回多个结果或不返回结果,导致下载错误的bib文件或不下载bib文件。
解决方案: 设定阈值,下载返回结果相似度大于阈值的最可能的bib文件。若结果中没有大于阈值的bib文件,则认为该参考文献不在数据库中。

### GUI
- 由于网络原因,搜索下载bib文件可能需要一段时间,此时会造成GUI界面无响应
解决方案: 使用Python多线程, 新建一个线程执行操作。

## 代码运行
### 配置环境
`pip install -r requirements.txt`
### 启动GUI
`python ./main.py`