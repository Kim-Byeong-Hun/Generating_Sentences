# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:33:44 2019

@author: kimbh
"""

from konlpy.tag import Twitter
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import mar_raw
import json, os, re

tw = Twitter()
form_class = uic.loadUiType("FTA.ui")[0]
app = None

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_pos.clicked.connect(self.btn_clicked_pos)
        self.pushButton_noun.clicked.connect(self.btn_clicked_noun)
        self.pushButton_phrases.clicked.connect(self.btn_clicked_phrases)
        self.pushButton_len
        self.category_button

        self.textBrowser_output.textChanged.connect(self.code_change_event_time)

        self.textEdit_first.setText("이 곳에 문장를 입력해 주세요.")
        self.textBrowser_output.setText("이곳에 결과가 출력됩니다.")

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

    def code_change_event_time(self):
        self.statusbar.showMessage("시간표시")

    def btn_clicked_pos(self):
        msg = self.textEdit_first.toPlainText()
        output = tw.pos(msg)
        msg2 = "{} \n" * len(output)
        self.textBrowser_output.verticalScrollBar().setValue(0)
        self.textBrowser_output.setText(msg2.format(*output))

    def btn_clicked_noun(self):
        msg = self.textEdit_first.toPlainText()
        output = tw.nouns(msg)
        msg2 = "{} \n" * len(output)
        self.textBrowser_output.setText(msg2.format(*output))

    def json_upload(self, fileName, dictfile):
        # 문장 읽어들이기
        file = fileName
        dict_file = dictfile
        if not os.path.exists(dict_file):
            # speech텍스트 파일 읽어오기
            fp = open(fileName, "r", encoding="utf-8")
            text = fp.read()
            # konlpy에서 잡지 못하는 구두점을 임시 해결하는 코드
            text = text.replace("…", "")
            # 형태소 분석
            twitter = Twitter()
            malist = twitter.pos(text, norm=True)
            words = []
            dic = []
            for word in malist:
                # 마침표를 제외한 구두점 등을 대상에서 제외
                if not word[1] in ["Punctuation"]:
                    words.append(word[0])
                if word[0] == ".":
                    words.append(word[0])
            # 딕셔너리 생성
            dic = make_dic(words)
            json.dump(dic, open(dict_file, "w", encoding="utf-8"))
        else:
            dic = json.load(open(dict_file,"r"))
            return dic

    def btn_clicked_phrases(self):
        msg = self.textEdit_first.toPlainText()
        twitter = Twitter()
        malist = twitter.pos(msg, norm=True)
        words = []
        for word in malist:
            # 마침표를 제외한 구두점 등을 대상에서 제외
            if not word[1] in ["Punctuation"]:
                words.append(word[0])
            if word[0] == ".":
                words.append(word[0])
        b = words[-1]
        a = words[-2]
        
        cate_index = self.category_button.currentIndex() + 1
        # 카테고리 별 문장
        if cate_index == 1:
            novel_dic = self.json_upload("./novel_1.txt", "./markov_novel.json")
            # 문장 만들기
            output_result = ""
            index = self.pushButton_len.currentIndex() + 1
            for i in range(index):
                output = mar_raw.make_sentence(novel_dic, a, b)
                output = re.sub(pattern='<[^>]*>', repl='', string=output)
                output_result += str(i+1) + '. ' + output + '\n\n'
            self.textBrowser_output.setText(output_result)
        elif cate_index == 2:
            speech_dic = self.json_upload("./speech_all.txt", "./markov_speech.json")
            # 문장 만들기
            output_result = ""
            index = self.pushButton_len.currentIndex() + 1
            for i in range(index):
                output = mar_raw.make_sentence(speech_dic, a, b)
                output = re.sub(pattern='<[^>]*>', repl='', string=output)
                output_result += str(i+1) + '. ' + output + '\n\n'
            self.textBrowser_output.setText(output_result)
        else:
            thesis_dic = self.json_upload("./thesis_all.txt", "./markov_thesis.json")
            # 문장 만들기
            output_result = ""
            index = self.pushButton_len.currentIndex() + 1
            for i in range(index):
                output = mar_raw.make_sentence(thesis_dic, a, b)
                output = re.sub(pattern='<[^>]*>', repl='', string=output)
                output_result += str(i+1) + '. ' + output + '\n\n'
            self.textBrowser_output.setText(output_result)

    def timeout(self):
        cur_time = QTime.currentTime()
        cur_time_txt = "현재시간: " + cur_time.toString("hh:mm:ss")
        self.statusbar.showMessage(cur_time_txt)
        

app = QApplication(sys.argv)
mywindow = MyWindow()
mywindow.show()
app.exec_()