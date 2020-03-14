# Paper Exporter

## Install
```
pip install -r requirements.txt
```

## Usage
1. Put PDF file downloaded from CNKI into folder `paper`, each name of file is the title of the paper.
eg:
```bash
$ tree ./paper
.
├── 基于Fuzzing技术的WEB应用程序漏洞挖掘技术研究.pdf
├── 基于计算机漏洞的挖掘技术研究.pdf
└── 基于静态分析技术的PHP代码自动化缺陷检测工具的研究与设计.pdf
```
2. Login into [CNKI](https://kns.cnki.net/), get the following cookies
* ASP.NET_SessionId
* SID_kns
3. update parameter `cookies` of class `CNKI` in `config.py`
4. Run `python cnki.py` to generate the bibtex file
5. check the `paper` folder you will find `.bib` files
eg: 
```bib
@article{ YMmtfQlqkooVrfeI,
    title = {基于Fuzzing技术的WEB应用程序漏洞挖掘技术研究},
    author = {陈景峰},
    year = {2012},
    keywords = {Web应用程序漏洞,Fuzzing技术,漏洞挖掘},
    abstract = {随着Internet与Web2.0技术的快速发展...},
    journal = {北方工业大学},
}
```
5. import bibtex files into any reference manager software(eg: mendeley)