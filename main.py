#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, unicode_literals
import requests
import bs4
import os
import json
from whaaaaat import prompt, print_json

mock = False

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
    if mock:
        return [{'docid': 'Y2850461', 'doctype': 'degree', 'title': '基于静态分析的PHP代码缺陷检测', 'author': '霍志鹏'}, {'docid': 'D499891', 'doctype': 'degree', 'title': '一种PHP程序自动化缺陷分析工具的设计与开发', 'author': '周瓒'}, {'docid': 'Y3097904', 'doctype': 'degree', 'title': 'Applying Web Server to Analyze the Limitations of Web Application Vulnerability Scanners', 'author': 'Sonkarlay J.Y.Weamie天才'}]
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
    if mock:
        return [{
            "id": "degreearticalY2850461",
            "collection_num": 0,
            "fulltext_reading_num": 0,
            "unit_name02": "北京邮电大学",
            "download_num": 0,
            "article_id": "Y2850461",
            "major_name": "信息安全",
            "third_party": [
                "CNKI:,CNKI:CDMD:2.1015.586475",
                "ISTIC:,Kyo6jSEmGQ9UwJ1VSrBIHE7r7ugKwPOfTkMjhZDcpvc="
            ],
            "cited_cnt": 8,
            "linkdoc_cnt": 0,
            "is_full": "0",
            "refdoc_cnt": 0,
            "is_oa": "0",
            "text_keywords": [
                "超文本预处 理器语言",
                "代码缺陷",
                "数据流分析法",
                "静态检测技术"
            ],
            "common_year": "2014",
            "org_name": "北京邮电大学",
            "pro_pub_date": 1419840000000,
            "service_model": "0",
            "source_db_single": "ISTIC",
            "keywords": [
                "超文本预处理器语言",
                "代码缺陷",
                "数据流分析法",
                "静态检测技术"
            ],
            "degree_level": "硕士",
            "language": "chi",
            "thirdparty_links_num": 0,
            "class_code": "TP312",
            "deunit_name": "北京邮电大学",
            "import_num": 27,
            "first_authors": "霍志鹏",
            "summary": "Web系统是当前最重要的一种信息交换手段，所以针对Web系统的攻击行为也在不断的增加。随着Web开发技术的不断演进，当前的Web系统已经不再仅仅是纯静态的HTML页面，而是由PHP等动态脚本语言开发的应用程序。PHP语言被广泛的用来开发Web系统，PHP语言的入门门槛很低，语法灵活，很多PHP开发人员并不具备基础的安全开发知识，导致使用PHP语言开发的Web系统一直是黑客攻击的重点 目标。<br>\u3000\u3000由于PHP语言开发的Web系统遭受的攻击正在不断增加，在网站实际部署之前有必要对其进行安全审查。然而当前采用的人工代 码审计方法不仅费时费力，而且对代码审计人员的技能要求非常高，所以需要开发自动化的代码缺陷检测工具。代码检测有静态分析和动态分析的方法 ，本文主要采用静态分析的方法检测PHP代码中的安全缺陷，然而由于PHP语言为动态脚本语言，具有动态弱类型，运行时文件包含等动态特性，导致对 其进行有效的静态分析是比较困难的。<br>\u3000\u3000本文在Facebook HHVM的基础上提出了一个针对PHP语言的流敏感、上下文敏感和过程间的前向 数据流分析方法。为了尽可能支持PHP语言的特性，本文提出了一种针对PHP的变量进行数据建模的方法，并在此基础上实现了别名分析，以尽可能提高 检测结果的准确度。为了处理PHP代码中灵活的审查过滤操作，尽可能的减少误报，本文静态检测技术还结合了一种基于有限自动机的字符串分析方法。本文还提出了一种规则定义方式，用来定义污染数据引入点、漏洞触发点与漏洞模式等信息。<br>\u3000\u3000本文主要关注的漏洞为污染传播类型的 漏洞，静态检测的目标是跨站点脚本漏洞和各种类型的注入漏洞，这些漏洞的产生原因都是因为用户可控的输入没有经过严格的审查过滤即传递到危险 函数，从而导致安全漏洞。",
            "head_words": [
                "超文本预处理器语言",
                "代码缺陷",
                "数据流分析法",
                "静态检测技术"
            ],
            "full_pubdate": 32503622400000,
            "page_cnt": "61",
            "publish_year": "2014",
            "abst_webdate": 1449043200000,
            "auto_keys": [
                "静态分析",
                "PHP语言",
                "代码",
                "Web系 统",
                "静态检测技术",
                "分析的方法",
                "动态",
                "脚本语言",
                "流分析方法",
                "安全",
                "污染数据",
                "审查"
            ],
            "unit_name": "北京邮电大学",
            "new_org": "北京邮电大学",
            "tag_num": 0,
            "cite_num": 8,
            "random_id": "XW_341AA1C731992B451918286063C1A4B9",
            "auth_area": "北京",
            "share_num": 0,
            "authors_name": "霍志鹏",
            "text_author": "霍志鹏",
            "title": "基于静态分析的PHP代码缺陷检测",
            "text_unit": "北京邮电大学",
            "subject_classcode_level": "TP312",
            "source_db": [
                "WF",
                "CNKI",
                "ISTIC"
            ],
            "tutor_name": "崔宝江",
            "subject_class_codes": "TP312",
            "note_num": 0,
            "common_sort_time": 1419840000000,
            "FilterCondition": [
                "orig_classcode",
                "auto_classcode"
            ],
            "abstract_reading_num": 1234,
            "data_state": "add",
            "orig_pub_date": "2014-12-30",
            "publish_year02": 1388476800000,
            "class_type": "degree_artical"
        }]
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
    return template.render(data=data)

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
        keyword = os.path.splitext(os.path.basename(filename))[0]
        print("Searching: {}".format(keyword))
        search_result = search(keyword)
        if len(search_result) == 0:
            print("0 matched.")
            continue
        selections = select(search_result)
        for choice in selections:
            title = choice.title
            authors = ",".join(choice.authors)
            docid = choice.docid
            doctype = choice.doctype
            data = export(docid, doctype)[0]
            data["file"] = ":{}$\\backslash$:{}:{}".format(filename[0], filename[2:].replace(os.path.sep, "/"), os.path.splitext(filename)[1][1:])
            bib = convert(data)
            print(bib)
            with open("{}.bib".format(title), "w", encoding="utf-8") as f:
                f.write(bib)

if __name__ == "__main__":
    main()