from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
import logging

DB_ADDRESS = "https://dblp.uni-trier.de"

class dblp():
    def __init__(self, file_list, headers=None):
        '''
        file_list: list(dict)
            'article_name':
            'author_name'
        '''

        self.db_address = DB_ADDRESS
        self.file_list = file_list
        if headers is None:
            self.headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                            Chrome/55.0.2883.87 Safari/537.36'
                        }
        else:
            self.headers = headers

    def export_Bib_file(self, export_path):
        if not os.path.isdir(export_path):
            os.mkdir(export_path)

        file_list = self.file_list
        
        for pfile in file_list:
            file_addr_list,file_name_list = self.get_file_address(pfile['article_name'])
            if len(file_addr_list)!=1:
                logging.warning("implicit article,find multiple articles or nothing")
            for file_addr, file_name in zip(file_addr_list,file_name_list):
                downloaded_file = requests.get(file_addr)
                with open(os.path.join(export_path,file_name),"wb") as f:
                    f.write(downloaded_file.content)


        pass
    def get_file_address(self, article_name: str, author_name: str=None):
        '''
        input:
            文章名
        return:
            文件下载地址列表
        '''
        assert "dblp.uni-trier.de" in self.db_address, "该函数只兼容从dblp查询"

        # 从dblp搜索关键字
        url = urljoin(self.db_address, "search")
        params = {"q":article_name}
        res = requests.get(url, params=params, headers=self.headers)        # print(res.text)

        file_addr_list = []
        file_name_list = []

        # 从返回的网页内容找到论文列表
        soup = BeautifulSoup(res.text,'html.parser')
        article_list = soup.select("#completesearch-publs > div > ul") # block_list = soup.find_all(attrs={'id':'completesearch-publs'})   # /html/body/div[2]/div[9]
        assert len(article_list)==1
        # type(article_list)  bs4.element.Tag
        article_list = article_list[0]
        # list    "entry (***) toc marked"
        article_list = article_list.find_all(attrs={"class": "entry"})
        
        # 为从 https://dblp.uni-trier.de/rec/ 下载bib文件，获取下载地址
        url_download = self.db_address
        for article_item in article_list:
            addr = article_item['id']
            file_name = os.path.basename(addr)+'.bib'

            file_addr_list.append(urljoin(url_download,"rec/"+addr+".bib?param=1"))
            file_name_list.append(file_name)

        return file_addr_list, file_name_list


if __name__=='__main__':
    BibD = dblp([{"article_name":"pointpillar"}])
    # BibD.get_file_address("pointpillar")
    BibD.export_Bib_file("./bib/")
    pass
