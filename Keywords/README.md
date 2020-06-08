# Key Words

>### 简介

* 基于jieba分词的中文文章提取，以及百度百科单词释义检索

>### 依赖
* python 3.5+
* requests
* jieba

>### 开始
1. >安装相关依赖
    ```
    pip install -r requirements.txt
    ```

1. >运行
    ```
    python spider.py
    ```

    * 依据提示输入需要处理的txt文件路径
    * 批量的txt文件可以放在一个文件夹内，然后输入文件夹路径即可

1. 配置文件config.json详解
    ```
    {
        "code":"utf-8",
        "threshold":60
    }
    ```

    * json文件格式
    * code输入输出文件编码格式（默认utf-8不建议更改）
    * threshold 单个文件提取的关键词个数。关键词按照关联性排序，取前threshold个。
