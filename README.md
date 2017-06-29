# Cartographer

## 概述

Cartographer 是一个 Python 爬虫程序，它可以从[国家统计局官网](http://www.stats.gov.cn/)上发布的[行政区划代码统计标准](http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/)中采集最新的中国行政区划数据。

## 前提条件

您的系统中必须安装下列组件：

- Python 3.x
- Scrapy 1.3+

## 运行

直接在当前目录下执行

```
crawl
```

这会在 `data/` 目录下生成一个 `.json` 文件，它包含了最新发布的行政区划代码表。