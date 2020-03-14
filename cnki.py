#!/usr/bin/env python
# encoding: utf-8

import requests
import bs4
import os
import json
import random
import string
import time
import config

session = requests.Session()
for k, v in config.CNKI.cookies.items():
    session.cookies.set_cookie(requests.cookies.create_cookie(domain='kns.cnki.net', name=k, value=v))
session.headers.update(config.CNKI.headers)

def search(keyword):
    url = 'https://kns.cnki.net/kns/brief/brief.aspx'
    params = {
        "pagename": "ASP.brief_default_result_aspx", 
        "isinEn": "1", 
        "dbPrefix": "SCDB", 
        "dbCatalog": "中国学术文献网络出版总库", 
        "ConfigFile": "SCDBINDEX.xml", 
        "research": "off", 
        "t": "{}".format(int(time.time())), 
        "keyValue": keyword, 
        "S": "1", 
        "sorttype": "", 
    }
    response = session.get(url, params=params)
    soup = bs4.BeautifulSoup(response.content,"html.parser")
    trs = soup.find_all("tr")
    result = []
    for tr in trs:
        link = tr.find("a", class_="fz14")
        if not link:
            continue
        title = link.text
        authors = [i.text for i in tr.find_all("a", class_="KnowledgeNetLink") if i.has_attr('href')]
        journal = [i for i in tr.find_all("a", target="_blank") if not i.has_attr('class')][-1].text
        href = link['href']
        result.append({
            "title": title, 
            "authors": authors,
            "journal": journal,
            "href": href,
        })
    return result

def select():
    pass

def export():
    pass

def main():
    print(search("PHP代码缺陷检测技术的研究与实现"))

if __name__ == "__main__":
    main()