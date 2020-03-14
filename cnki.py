#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, unicode_literals
from whaaaaat import prompt, print_json
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
            "docid": href.split("FileName=")[1].split("&DbName=")[0]
        })
    return result


class Choice:
    def __init__(self, title, authors, journal, docid):
        self.title = title
        self.authors = authors
        self.journal = journal
        self.docid = docid

    def __str__(self):
        return '[{}] {}. {}. {}'.format(
            self.docid,
            ",".join(self.authors), 
            self.title,
            self.journal,
        )

def select(choices):
    cache = {}
    c = []
    for i in choices:
        x = Choice(
            authors=i['authors'],
            journal=i['journal'],
            title=i['title'],
            docid=i['docid'],
        )
        choice = {"name": "{}".format(x)}
        cache[i['docid']] = x
        c.append(choice)
    questions = [
        {
            'type': 'checkbox',
            'name': 'documents',
            'choices': c,
            'message': 'Please select documents you want to export',
        }
    ]
    answers = prompt(questions)
    result = []
    for i in answers["documents"]:
        result.append(cache[i.split("[")[1].split("]")[0]])
    return result

def export():
    pass

def main():
    search_result = search("PHP代码缺陷检测技术的研究与实现")
    selections = select(search_result)
    print(selections)
    # for choice in selections:
    #     result_bib_filename = "{}{}{}.{}.bib".format(
    #         folder,
    #         os.path.sep,
    #         choice.title,
    #         ext,
    #     )
    #     title = choice.title
    #     authors = ",".join(choice.authors)
    #     docid = choice.docid
    #     doctype = choice.doctype
    #     data = export(docid, doctype)[0]
    #     data["file"] = ":{}$\\backslash$:{}:{}".format(filename[0], filename[2:].replace(os.path.sep, "/"), ext)
    #     bib = convert(data)
    #     print(bib)
    #     with open(result_bib_filename, "w", encoding="utf-8") as f:
    #         f.write(bib)

if __name__ == "__main__":
    main()