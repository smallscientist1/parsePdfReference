# DLP2022 Lab1
## 软件代码
### file_io
PDFReader类: 用于解析pdf文件, 提取出其中有关参考文献的部分
- PDFReader.\__init\__(file_path, passwd): 输入需要解析的pdf文件名和密码(若有),创建一个PDFReader对象
- PDFReader.extract_pdf():提取出pdf文件中的文字,找到Reference的部分,以字符串形式返回;
- PDFReader.parse_pdf():调用extract_pdf(), 并对其返回的Reference字符串进行正则表达式匹配, 提取出每条参考文献的信息。