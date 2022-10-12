import pdfminer
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
import re
class PDFReader():
    def __init__(self, path="1812.05784PointPillar.pdf", passwd=None):
        fp = open(path, "rb")
        # 创建一个pdf文档分析器
        file_parser = PDFParser(fp)
        # 创建pdf文档
        pdf_file = PDFDocument()
        # 链接分析器与文档对象
        file_parser.set_document(pdf_file)
        pdf_file.set_parser(file_parser)
        # 提供初始化密码
        pdf_file.initialize(passwd)

        self.path = path
        self.file_parser = file_parser
        self.pdf_file = pdf_file

    def extract_pdfref(self):
        pdfFile = self.pdf_file
        ref_text = ""

        # 检测文档是否提供txt转换
        if not pdfFile.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
        # 解析数据
            # 数据管理
            manager = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(manager, laparams=laparams)
            # 解释器对象
            interpreter = PDFPageInterpreter(manager, device)

            # 开始循环处理，每次处理一页
            flag = 0
            for page in pdfFile.get_pages():
                if flag == 1:
                    break
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if(isinstance(x, LTTextBoxHorizontal)):
                        str = x.get_text()
                        if flag == 1:
                            ref_text = str
                            break
                        if "References\n" in str:
                            flag = 1
            
            return ref_text

    def parse_ref(self):
        '''
        return:
            ref_list : a list of references
        '''
        ref_text = self.extract_pdfref()

        # 将每条内的换行符去掉
        ref_text = re.sub(r'-\n',"",ref_text)
        ref_text = re.sub(r'\n[^\[]'," ",ref_text) # bug!!!!!!
        # 按标号与换行符匹配每一条ref(.*?: 非贪婪匹配),不返回标号
        ref_list = re.findall(r'\[\d+\](.*?\n)',ref_text,flags=re.DOTALL)
        return ref_list
        
        



if __name__=='__main__':
    file_reader = PDFReader()
    ref_text =     file_reader.extract_pdfref()
    with open("ref.txt","w") as f:
        f.write(ref_text)
    file_reader.parse_ref()

