import pprint
import re
from urllib import parse
import os
import requests


class Searcher:
    def __init__(self):
        self.session = requests.session()  # 初始化网页会话

    def serachVideo(self, keyword):
        key_word_url_code = parse.quote(keyword)
        request_url = "http://navod.scse.com.cn/nn_cms/data/template/100000/200003/index_v3_001.php?nns_template_type=100000&nns_template_id=200003&nns_user_id=g%2C172.16.135.2%2C5ae5b66d1a9a5ac66&nns_tag=31&nns_page_name=search&nns_search=" + key_word_url_code + "&nns_category_id=1000&nns_media_asset_id=movies|TVseries|variety|animation|softmovies|schoolmv|KoreaJapan&nns_search_type=2&nns_search_method=2&nns_include_category=1"
        data = {
            'nns_template_type': 100000,
            'nns_template_id': 200003,
            'nns_user_id': 'g,172.16.135.2,5ae5b66d1a9a5ac66',
            'nns_tag': 31,
            'nns_page_name': 'search',
            'nns_search': '%s' % keyword,
            'nns_category_id': 1000,
            'nns_media_asset_id': 'movies|TVseries|variety|animation|softmovies|schoolmv|KoreaJapan',
            'nns_search_type': 2,
            'nns_search_method': 2,
            'nns_include_category': 1,
        }

        search_res = self.session.post(request_url, data)
        url_and_name = re.findall(
            '<a href=\"http://navod\.scse\.com\.cn/nn_cms/data/template/100000/200003/index_v3_001\.php\?.*</li>',
            search_res.text)

        res_list = []
        for each in url_and_name:
            res_dic = {}
            try:
                url = \
                    re.findall(
                        "http://navod\.scse\.com\.cn/nn_cms/data/template/100000/200003/index_v3_001\.php\?.*detail",
                        each)[0]
                title = re.findall("<span class=\"programName\">(.*)</span></a></li>", each)[0]
                res_dic[title] = url
                res_list.append([{'title':title,'url':url}])
            except BaseException:
                return None
        return res_list

    def getEps(self, videoUrl):
        html = requests.get(videoUrl)
        res = re.findall(
            "<li><a href=\"http://navod.scse.com.cn/nn_cms/data/template/100000/200003/index_v3_001.php\?.*\" class.*</a></li>",
            html.text)  # 获取链接
        ep_link_list = []
        if res:

            ## 电视剧
            for each in res:
                ep_link_dic = {}
                try:
                    ## 电视剧
                    video_link = re.findall(
                        "<li><a href=\"(http://navod.scse.com.cn/nn_cms/data/template/100000/200003/index_v3_001.php\?.*)\" class.*</a></li>",
                        each)[0]  # 处理链接
                    ep = re.findall("class=\"button1 movie_page_indexa.*\">(.*)</a></li>", each)[0]
                    ep_link_list.append([{'title':ep,'url':video_link}])
                except:
                    return None
        else:
            ## 电影
            ## 因为只有 1 集，所以返回当前网址
            try:
                ep_link_list.append([{'title':"E1",'url':videoUrl}])
            except:
                return None

        return ep_link_list

    def getEpDwonloadUrl(self,url):
        html = requests.get(url)
        link = re.findall("&play_url=(http%3A%2F%2F.*mp4)", html.text)[0]
        title = re.findall("<span id=\"OnlinePlay\" class=\"playingSpan\">正在播放：(.*)</span>", html.text)[0]
        title = title.replace("/", "-")
        return link, title
