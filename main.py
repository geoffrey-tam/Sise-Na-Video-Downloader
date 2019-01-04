import sys

import Downloader
import History
import Home
import Searcher
import Viewer
import platform
if platform.system() in ['Linux','Darwin']:
    import readline

class Exit(Exception):
    def __init__(self):
        super(Exit).__init__()


def pprint(obj):
    for index, each in enumerate(obj, start=1):
        index = str(index)
        title = each[0]['title']
        if len(index) == 1:
            print(index + ".  " + title)
        else:
            print(index + ". " + title)


def viwer():
    viewer = Viewer.Viewer()
    category_list = ["电影", "电视剧", "体育", "动漫", "校园视频", "日韩视频"]
    category_dict = {"电影": "movies", "电视剧": "TVseries", "体育": "variety", "动漫": "animation", "校园视频": "schoolmv",
                     "日韩视频": "KoreaJapan"}

    for index, each in enumerate(category_list, start=1):
        print(str(index) + ". " + each)
    choose = input("b:返回 | q:退出 | 序号:查看\n(操作) ")
    if choose in EXIT_CMDS:
        exit()
    elif choose in BACK_CMDS:
        return
    else:
        category = category_dict[category_list[int(choose) - 1]]

    page = 0
    while True:
        video_list = viewer.getVideoList(category, page)
        pprint(video_list)

        cmd = input("l:上一页 | n:下一页 | b:返回 | q:退出 | 序号:查看\n (操作): ")

        if cmd in BACK_CMDS:
            return
        elif cmd in EXIT_CMDS:
            exit()
        elif cmd in NEXTPAGE_CMDS or not cmd:
            page += 1
            continue
        elif cmd in LASTPAGE_CMDS:
            page -= 1 if page != 0 else page
            continue
        else:
            try:
                choose = int(cmd) - 1
            except:
                print("* 输入错误")
                continue
            video_url = video_list[choose][0]['url']
            ep_list = searcher.getEps(video_url)
            download_ep(ep_list)


def show_history():
    page = 0
    while True:
        if page < 0: page = 0
        res = history.show(page)
        print(res)


        if not res: page -= 1
        cmd = input("l:上一页 | n:下一页 | b:返回 | q:退出\n(操作) ")
        if cmd in BACK_CMDS:
            return
        elif cmd in EXIT_CMDS:
            exit()
        elif cmd in NEXTPAGE_CMDS or not cmd:
            page += 1
            continue
        elif cmd in LASTPAGE_CMDS:
            page -= 1 if page != 0 else page
            continue
        else:
            print("* 输入错误")
            continue


def search(key_word=None):
    while True:
        if not key_word:
            search_key_word = input("* 请输入你要搜索的电视、电影名: ")
        else:
            search_key_word = key_word
            key_word = None

        if search_key_word in EXIT_CMDS:
            exit()
        elif search_key_word in BACK_CMDS:
            return

        video_list = searcher.serachVideo(search_key_word)
        if not video_list:
            print("* 搜索不到你要的资源!")
            continue

        try:
            while True:
                try:
                    pprint(video_list)
                    index = input("b:返回 | q:退出 | 序号:查看\n(操作) ")
                    if index in EXIT_CMDS:
                        exit()
                    elif index in BACK_CMDS:
                        break
                    index = int(index) - 1
                except KeyError:
                    print("* 序号不存在")
                    continue
                except ValueError:
                    print("* 你在逗我呢？！")
                    continue
                video_url = video_list[index][0]['url']
                ep_list = searcher.getEps(video_url)

                download_ep(ep_list)

        except Exit:
            return


def download_ep(ep_list):
    while True:
        pprint(ep_list)
        choose = input("b:返回 | q:退出 | 序号:下载\n(操作) ")
        try:
            if choose in EXIT_CMDS:
                exit()
            elif choose in BACK_CMDS:
                return
            choose_set = set()
            if "," in choose:
                temp_list = choose.split(",")
                for temp in temp_list:
                    if "-" in temp:
                        start = int(temp.split("-")[0])
                        end = int(temp.split("-")[1]) + 1
                        for i in range(start, end):
                            choose_set.add(i)

                    else:
                        choose_set.add(int(temp))
            else:
                if "-" in choose:
                    start = int(choose.split("-")[0])
                    end = int(choose.split("-")[1]) + 1
                    for i in range(start, end):
                        choose_set.add(i)
                else:
                    choose_set.add(int(choose))
        except KeyError:
            print("序号不存在")
            continue
        except ValueError:
            print("你在逗我呢？！")
            continue

        choose_list = list(choose_set)
        for index in choose_list:
            index = index - 1
            ep_url = ep_list[index][0]['url']
            ep_download_url, filename = searcher.getEpDwonloadUrl(ep_url)
            downloader.download(ep_download_url, filename + ".mp4")

        # 历史记录
        history.put(filename)

def getHome():
    while True:
        box_video_l = home.getBoxVideoList()
        home.pprint(box_video_l)
        video_l = home.getVideoUrlList(box_video_l)

        choose = input("b:返回 | q:退出 | 序号:查看\n(操作) ")
        if choose in BACK_CMDS:
            return
        elif choose in EXIT_CMDS:
            exit()
        else:
            choose = int(choose) - 1
            video_url = video_l[choose]
            ep_list = searcher.getEps(video_url)
            download_ep(ep_list)


if __name__ == '__main__':
    try:
        EXIT_CMDS = ['exit', 'bye', 'quit', 'q']
        BACK_CMDS = ['b', 'back']
        LASTPAGE_CMDS = ['last', 'l']
        NEXTPAGE_CMDS = ['next', 'n']

        searcher = Searcher.Searcher()
        downloader = Downloader.Downloader()
        home = Home.Home()
        history = History.History()

        while True:
            if len(sys.argv) == 2:
                search(sys.argv[1])
                sys.argv.pop(1)

            else:
                cmd = input("1. 首页\n2. 频道\n3. 搜索\n4. 下载历史\n(操作): ")

                if cmd == '1':
                    getHome()
                elif cmd == '2':
                    viwer()
                elif cmd == '3':
                    search()
                elif cmd == '4':
                    show_history()
                elif cmd in ['exit', 'bye', 'q', 'quit']:
                    exit()
                else:
                    print("* Error: 错误序号")
                    continue

    except KeyboardInterrupt:
        print("\nbye~")
        exit()
