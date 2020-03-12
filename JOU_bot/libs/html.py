
#-*- coding=utf-8 -*-
import os

html_part1='''
<!Doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="./default.css">
    <title>机器人的下载站点</title>
</head>
<body>
    <style type='text/css'>
            .link_class {
              width:auto;
              height: 30px;
              color: #fff;
              text-align: center;
              display: block;
              -webkit-border-radius: 3px;
              -moz-border-radius: 3px;
              border-radius: 3px;
              background: #000;
              text-decoration: none;
              line-height: 30px;
            }
    </style>
'''

html_part2='''
</body>
</html>
'''
async def generate_html(target,headline="机器人の下载站"):
    files=os.listdir(target)
    filenames=[]
    for x in files:
        if not os.path.isdir(x):
            filenames.append(x)
    with open(target+"/index.html","w+",encoding="utf-8") as f:
        f.write(html_part1)
        f.write("<h1>{}</h1><br>".format(headline))
        f.write('<a class="link_class" href="./BDPurl.html">电影百度盘链接</a><br><br>')
        for x in filename:
            if x!="index.html":
                f.write('<a class="link_class" href="./{}" download>{}</a>'.format(x,x))
                f.write('<br>')
        f.write(html_part2)
        f.close()