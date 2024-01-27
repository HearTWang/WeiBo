# -*- codeing = utf-8 -*-
# @Time : 2023/9/13 16:03
# @Author : WxY
# @File : ZhihuClass.py
# @Software : PyCharm

import requests
import time
import pandas as pd
import os
import re
import random
from gne import GeneralNewsExtractor


class ZhihuSpider(object):
    def __init__(self, keywords, start_time, end_time):
        self.headers = None
        self.url = None
        self.keywords = keywords
        self.start_time = start_time
        self.end_time = end_time
        self.pagesLimit = 2000

    def set_header(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, likeGecko) '
                          'Chrome/115.0.0.0 Safari/537.36 '
        }
        question_id = 24429613
        self.url = 'https://www.zhihu.com/api/v4/questions/{' \
                   '}/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed' \
                   '%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by' \
                   '%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment' \
                   '%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time' \
                   '%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content' \
                   '%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked' \
                   '%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count' \
                   '%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5' \
                   '&offset=0&order=default&platform=desktop'.format(question_id)

    def get_pagedata(self):
        self.set_header()
        # 发送请求
        response = requests.request('GET', self.url, headers=self.headers)
        page_data = response.text
        return page_data

    def extract_pagedata(self):
        page_data = self.get_pagedata()
        extractor = GeneralNewsExtractor()
        content = extractor.extract(page_data)

        return content

