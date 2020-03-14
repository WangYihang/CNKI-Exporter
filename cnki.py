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

def random_string(legnth=0x10, charset=string.ascii_letters):
    return "".join([random.choice(charset) for _ in range(legnth)])

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
            "filename": href.split("FileName=")[1].split("&")[0],
            "dbname": href.split("DbName=")[1].split("&")[0],
        })
    return result

class Choice:
    def __init__(self, title, authors, journal, filename, dbname):
        self.title = title
        self.authors = authors
        self.journal = journal
        self.filename = filename
        self.dbname = dbname

    def __str__(self):
        return '[{}!{}!1!0] {}. {}. {}'.format(
            self.filename,
            self.dbname,
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
            filename=i['filename'],
            dbname=i['dbname'],
        )
        choice = {"name": "{}".format(x)}
        cache['{}!{}!1!0'.format(i['filename'], i['dbname'])] = x
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

def export(filename, dbname):
    print("{}!{}!1!0".format(filename, dbname))
    url = "https://kns.cnki.net/kns/ViewPage/viewsave.aspx?displayMode=NoteExpress"
    data = {
        "hid_kLogin_headerUrl": "%2FKLogin%2FRequest%2FGetKHeader.ashx%253Fcallback%253D%253F",
        "Ecp_TextBoxUserName": "",
        "Ecp_TextBoxPwd": "",
        "clearall": "",
        "IsPrev": "",
        "TablePre": "",
        "QueryID": "",
        "CookieName": "FileNameS",
        "displayMode": "GBTRefer",
        "FileOpen": "NO",
        "FieldMaxLength": "300",
        "FileDisplayMode": "GBTREFER",
        "FileSaveMode": "GBTREFER",
        "CurSaveModeType": "GBTREFER",
        "displayMode": "Refer",
        "displayMode": "new",
        "displayMode": "newdefine",
        "displayMode": "elearning",
        "displayMode": "Refworks",
        "displayMode": "EndNote",
        "displayMode": "NoteExpress",
        "displayMode": "NodeFirst",
        "displayMode": "selfDefine",
        "formfilenames": "{}!{}!1!0".format(dbname, filename),
        "searchinfo": "",
        "hid_KLogin_FooterUrl": "%2FKLogin%2FRequest%2FGetKFooter.ashx%253Fcallback%253D%253F",
    }
    response = session.post(url, data=data)
    soup = bs4.BeautifulSoup(response.content,"html.parser")
    td = soup.find("td", class_="CurContentID")
    content = td.text.replace("\n", "")
    fields = content.replace("{", "\n{").split("\n")[1:]
    data = {}
    for field in fields:
        key = field.split("{")[1].split("}:")[0]
        value = field.split("}: ")[1].replace("\n", "").replace("\r", "").replace(" ", "").replace("\t", "").strip()
        data[key] = value
    return data

def convert(data):
    '''
    {
        "Reference Type": "Journal Article",
        "Title": "基于遗传算法和Fuzzing技术的Web应用漏洞挖掘研究",
        "Author": "闫飞;",
        "Author Address": "西安翻译学院;",
        "Journal": "信息通信",
        "Year": "2018",
        "Issue": "09",
        "Pages": "61-62",
        "Keywords": "遗传算法;Fuzzing技术;Web应用;漏洞挖掘",
        "Abstract": "在网络快速发展普及的形势下,以B/S架构为基础的Web应用系统备受青睐,开始实现广泛应用,而网络用户的大部分个人隐私息,是通过Web应用,加以传输并处理,从而导致Web应用演变成了网络攻击的重灾区域。所以,构建健全的、有效的Web应用漏洞挖掘机制,以便于可以及时发现其中存在的安全性问题,在一定程度上避免被恶意攻击。据此,文章主要对基于遗传算法和Fuzzing技术的Web应用漏洞挖掘进行了深入探究。",
        "ISBN/ISSN": "1673-1131",
        "Notes": "42-1739/TN",
        "Database Provider": "CNKI"
    }
    '''
    from jinja2 import Template
    template = Template(open("example.bib.template").read())
    data = {
        "file": data["file"],
        "title": data["Title"],
        "author": ",".join(data["Author"].split(";")),
        "journal": data["Journal"],
        "year": data["Year"],
        "issue": data["Issue"],
        "pages": data["Pages"],
        "keywords": ",".join(data["Keywords"].split(";")),
        "abstract": data["Abstract"],
        "isbn": data["ISBN/ISSN"],
    }
    return template.render(data=data, citation_key=random_string())
    pass

def main():
    import glob
    filenames = glob.glob("{}\\paper\\*.pdf".format(os.getcwd()))
    for filename in filenames:
        ext = os.path.splitext(filename)[1][1:]
        exists_bib_filename = "{}.bib".format(filename)
        folder = os.path.abspath(os.path.dirname(filename))
        if os.path.exists(exists_bib_filename):
            print("bib file exists, skipping {}".format(exists_bib_filename))
            continue
        keyword = os.path.splitext(os.path.basename(filename))[0]
        print("Searching: {}".format(keyword))
        search_result = search(keyword)
        if len(search_result) == 0:
            print("0 matched.")
            continue
        selections = select(search_result)
        print(selections)
        for choice in selections:
            print(str(choice))
            data = export(choice.filename, choice.dbname)
            result_bib_filename = "{}{}{}.{}.bib".format(
                folder,
                os.path.sep,
                choice.title,
                ext,
            )
            title = choice.title
            authors = ",".join(choice.authors)
            data["file"] = ":{}$\\backslash$:{}:{}".format(filename[0], filename[2:].replace(os.path.sep, "/"), ext)
            bib = convert(data)
            print(bib)
            with open(result_bib_filename, "w", encoding="utf-8") as f:
                f.write(bib)
            break
        break

if __name__ == "__main__":
    main()