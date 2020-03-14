#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, unicode_literals
import requests
import bs4
import os
import json
import random
import string
from whaaaaat import prompt, print_json

def random_string(legnth=0x10, charset=string.ascii_letters):
    return "".join([random.choice(charset) for _ in range(legnth)])

def getExportID(docid, doctype):
    doctypes = {
        "perio": "periodical",
        "degree": "thesis",
        "conference": "conference",
        "standards": "standard",
        "patent": "patent",
        "tech": "nstr",
        "techResult": "cstad",
        "Book": "book",
    }
    return "{}_{}".format(doctypes[doctype], docid)

def search(keyword):
    url = "http://www.wanfangdata.com.cn/search/searchList.do"
    params = {
        "searchType" : "all", 
        # "pageSize" : "20", 
        # "page" : "3", 
        "searchWord" : keyword, 
        # "order" : "correlation", 
        # "showType" : "detail", 
        # "isCheck" : "check", 
        # "isHit" : "", 
        # "isHitUnit" : "", 
        # "firstAuthor" : "false", 
        # "corePerio" : "false", 
        # "alreadyBuyResource" : "false", 
        # "rangeParame" : "", 
        # "navSearchType" : "all", 
    }
    response = requests.get(url, params=params)
    soup = bs4.BeautifulSoup(response.content,"html.parser")
    resultLists = soup.find_all("div", class_="ResultList")
    results = []
    for resultList in resultLists:
        docInfo = resultList.find("input", type="checkbox")
        authors = [i.text for i in resultList.find_all("a", target="_self")]
        result = {
            "docid": docInfo["docid"],
            "doctype": docInfo["doctype"],
            "title": resultList.find("a", target="_blank").text.strip(),
            "authors": authors,
        }
        results.append(result)
    return results

def export(docid, doctype):
    exportID = getExportID(docid, doctype)
    url = "http://www.wanfangdata.com.cn/export/export.do"
    data = {
        "isHtml5": "true",
        "isHtml5Value": exportID,
    }
    response = requests.post(url, data=data)
    return json.loads(response.content)

def convert(data):
    from jinja2 import Template
    template = Template(open("example.bib.template").read())
    data = {
        "abstract": data["summary"].replace("<br>", ""),
        "author": data["text_author"],
        "keywords": ",".join(data["keywords"]),
        "title": data["title"],
        "year": data["publish_year"],
        "file": data["file"],
    }
    return template.render(data=data, citation_key=random_string())

class Choice:
    def __init__(self, title, authors, doctype, docid):
        self.title = title
        self.authors = authors
        self.doctype = doctype
        self.docid = docid

    def __str__(self):
        return '[{}.{}] {}. {}'.format(
            self.doctype,
            self.docid,
            ",".join(self.authors), 
            self.title,
        )

def select(choices):
    cache = {}
    c = []
    for i in choices:
        x = Choice(
            authors=i['authors'],
            title=i['title'],
            doctype=i['doctype'],
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
        result.append(cache[i.split(".")[1].split("]")[0]])
    return result

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
        for choice in selections:
            result_bib_filename = "{}{}{}.{}.bib".format(
                folder,
                os.path.sep,
                choice.title,
                ext,
            )
            title = choice.title
            authors = ",".join(choice.authors)
            docid = choice.docid
            doctype = choice.doctype
            data = export(docid, doctype)[0]
            data["file"] = ":{}$\\backslash$:{}:{}".format(filename[0], filename[2:].replace(os.path.sep, "/"), ext)
            bib = convert(data)
            print(bib)
            with open(result_bib_filename, "w", encoding="utf-8") as f:
                f.write(bib)

if __name__ == "__main__":
    main()