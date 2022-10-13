#!/usr/bin/python3
# -*- coding: utf-8 -*-
from file_io.pdf_io import PDFReader
from DownloadAPI import buildBibDownloader

import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton)
from PyQt5.QtCore import QThread, pyqtSignal


class win(QDialog):
    '''
    gui窗口
    '''
    def __init__(self):
        self.filename = ''
        self.exportpath = ''

        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open pdf file', self)
        self.btnSave = QPushButton('Save Path', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.label1, 2, 1, 2, 1)
        layout.addWidget(self.label2, 2, 2, 2, 1)
        layout.addWidget(self.label3, 2, 3, 2, 1)        
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openpdf)
        self.btnSave.clicked.connect(self.savebib)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openpdf(self):
        filename,_ = QFileDialog.getOpenFileName(
            self, 'Open pdf', './example_pdf', '*.pdf'
        )
        self.filename = filename
        self.label1.setText(filename)
        return

    def savebib(self):
        exportpath = QFileDialog.getExistingDirectory(
            self, 'Save bib path', './bib'
        )
        self.exportpath = exportpath
        self.label2.setText(exportpath)
        return

    def processSlot(self):
        '''
        启动核心操作线程
        '''
        if self.filename == '':
            self.label1.setText("Please select input file!")
            return
        if self.exportpath == '':
            self.label2.setText("Please select output directory!")
            return
        pdf_file = self.filename
        exportpath = self.exportpath

        self.process_thread = processThread(self.filename,self.exportpath)
        self.process_thread.finished_signal.connect(self.finished_slot)
        self.label3.setText('Processing,please wait...')
        self.process_thread.start()


    def finished_slot(self,mmessage):
        self.label3.setText(mmessage)


class processThread(QThread):
    '''
    在gui中使用线程处理, 非阻塞
    '''
    finished_signal = pyqtSignal(str)                                                               

    def __init__(self, filename, exportpath,parent=None):
        super().__init__(parent)
        self.filename = filename
        self.exportpath = exportpath

    def run(self):
        '''
        执行核心操作
        '''
        pdf_file = self.filename
        exportpath = self.exportpath

        # parse pdf
        file_reader = PDFReader(pdf_file)
        ref_list = file_reader.parse_ref()
        # download bib file
        BibDowner = buildBibDownloader(db_name="crossref",file_list = ref_list)
        BibDowner.export_Bib_file(exportpath)

        self.finished_signal.emit('get bib done')

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())