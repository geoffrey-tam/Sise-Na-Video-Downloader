import requests
import re
from bs4 import BeautifulSoup
import pprint
class Viewer:
    _format_url ="http://navod.scse.com.cn/nn_cms/data/template/100000/200003/index_v3_001.php?nns_template_type=100000&nns_template_id=200003&nns_user_id=g%2C172.16.115.12%2C5c016a591cd5a956&nns_tag=31&nns_media_asset_id={category}&nns_category_id=1000&nns_parent_category_id=1000&nns_page_name=newest&nns_page_num={page}"

    def getVideoList(self,category,page):
        url = self._format_url.format(category = category,page=page)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text,'lxml')
        classifyProgram = soup.find('div',class_="classsifyProgram")

        program_list = []
        for each in classifyProgram:
            program = each.find('a')

            if program != -1:
                program_name = program.find('span',class_='programName').get_text()
                program_url = program.get('href')
                program_list.append([{'title':program_name,'url':program_url}])

        return program_list


if __name__ == '__main__':
    viewer = Viewer()
    pprint.pprint(viewer.getVideoList("movies",0))


