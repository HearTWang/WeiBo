from ZhihuClass import ZhihuSpider

if __name__ == '__main__':
    keywords, start_time, end_time = '北师大', '2023-08-01', '2023-08-31'
    spider = ZhihuSpider(keywords, start_time, end_time)
    content = spider.get_pagedata()
    print(content)