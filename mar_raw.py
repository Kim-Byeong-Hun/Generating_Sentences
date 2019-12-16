# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:33:44 2019

@author: kimbh
"""

# ��Ű�� �ҷ�����
import codecs
import os, re, json, random
import urllib.request
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

# ��ųʸ��� ������ ���
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic:
        dic[w1] = {}
    if not w2 in dic[w1]:
        dic[w1][w2] = {}
    if not w3 in dic[w1][w2]:
        dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

# �������� ü�� ��ųʸ� ����
def make_dic(words):
    tmp = ["@"]
    dic = {}
    for word in words:
        tmp.append(word)
        if len(tmp) < 3: 
            continue
        if len(tmp) > 3: 
            tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == ".":
            tmp = ["@"]
            continue
    return dic

# ���� ���� ����
def make_sentence(dic, first, second):
    ret = []
    if not "@" in dic:
        return "no dic"
    top = dic["@"]
    w1 = first
    w2 = second
    ret.append(w1)
    ret.append(w2)
    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == ".":
            break
        w1, w2 = w2, w3
    ret = "".join(ret)
    # ���� ���
    params = urllib.parse.urlencode({
        "_callback": "",
        "q": ret
    })
    
    # ���� ���α׷� ������ ��ü�Ͽ� ���̹� ����� �˻�� �̿�
    request = urllib.request.Request(
        "https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn?"
        + params)
    request.add_header('Referer', 'https://search.naver.com/earch.naver')
    data = urllib.request.urlopen(request)
    data = data.read().decode("utf-8")[1:-2]
    data = json.loads(data)
    data = data["message"]["result"]["html"]
    
    return data

# �ܾ� ����
def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))