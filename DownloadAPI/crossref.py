from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
import logging
import json

DB_ADDRESS = "https://api.crossref.org/works"

class crossref():
    def __init__(self, file_list, headers=None):
        '''
        file_list: list of refences
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
        self.bib_header = {"Accept": "application/x-bibtex"} # crossref

    def export_Bib_file(self, export_path,score=70.0):
        '''
        export_path: 导出bib文件的路径
        scores: crossref返回的置信度，设置一个阈值
        '''
        if not os.path.isdir(export_path):
            os.mkdir(export_path)

        file_list = self.file_list
        bib_header = self.bib_header
        
        for pfile in file_list:
            file_addr,file_idx = self.get_file_address(pfile,score=score)
            if file_addr is None:
                continue

            downloaded_file = requests.get(file_addr,headers=bib_header).content
            with open(os.path.join(export_path,file_idx+'.bib'),"wb") as f:
                f.write(downloaded_file)

        return



    def get_file_address(self, article_name: str, score=70.0):
        '''
        input:
            文章名
        return:
            文件下载地址, 文件id
        '''
        params = {"query.bibliographic":article_name,
                    "rows": '2'}
        ret = requests.get(self.db_address, params=params)
        if ret.status_code != 200: # 未正确返回
            return None, None
        ret_dict = json.loads(ret.content)
        ret_ref = ret_dict['message']['items'][0] # 取置信度最高的结果
        if ret_ref['score']<score:
            return None, None
        file_addr = ret_ref['URL']
        file_idx = ret_ref['prefix']

        return file_addr,file_idx


if __name__=='__main__':
    BibD = crossref(["W. Liu, D. Anguelov, D. Erhan, C. Szegedy, S. Reed, C.-Y. Fu, and A. C. Berg. SSD: Single shot multibox detector. In ECCV, 2016. 2, 4"])
    BibD.export_Bib_file("./bib/")
    pass
