import os

import requests
from bs4 import BeautifulSoup


class Home:
    base_url = "http://navod.scse.com.cn/nn_cms/data/template/100000/200003/index_v3_001.php?nns_template_type=100000&nns_template_id=200003&nns_user_id=g%2C172.16.115.146%2C5c01f7ae2723b3d&nns_tag=31&nns_page_name=home"

    def __init__(self):
        pass

    def getBoxVideoList(self):
        html_text = requests.get(self.base_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        smallboxs = soup.find_all("div", class_="smallbox")
        bigboxs = soup.find_all("div", class_="bigbox")

        boxs = list(smallboxs) + list(bigboxs)

        box_video_list = []
        for box in boxs:
            box_title = box.find('h1').get_text()
            programs = box.find_all('div', class_='program')
            box_dict = {"box_title": box_title, 'videos': []}

            for program in programs:
                a = program.find_all('a')
                for each in a:
                    video_url = each.get('href')
                    video_title = each.find('span', class_='programName').get_text()
                    video_dict = {'title': video_title, 'url': video_url}
                    box_dict['videos'].append(video_dict)

            box_video_list.append(box_dict)
        return box_video_list

    def pprint(self, box_video_list):
        try:
            os_size = os.get_terminal_size()
            os_col = os_size.columns
        except OSError:
            os_col = 80

        index = 1
        for box in box_video_list:
            box_title = ' ' + box['box_title'] + ' '

            print(format(box_title, "-^%s" % (os_col - len(box_title))))

            for video in box['videos']:
                i = str(index) + ". " if index > 9 else str(index) + ".  "
                print(i + video['title'])
                index += 1

    def getVideoUrlList(self, box_video_list):
        l = []
        for box in box_video_list:
            for video in box['videos']:
                video_url = video['url']
                l.append(video_url)


        return l


if __name__ == '__main__':
    home = Home()
    l = home.getBoxVideoList()

    home.getVideoUrlList(l)
