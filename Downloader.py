import configparser
import os
import urllib.request
import xmlrpc.client
from urllib.parse import unquote
from subprocess import call
import platform
BaseDir = os.path.dirname(os.path.abspath(__file__))

def show_notify_on_mac(title, massage):
    if platform.system() == 'Windows':
        # windows
        pass
    elif platform.system() == 'Darwin':
        # mac
        cmd = 'display notification \"' + \
              "%s" % massage + '\" with title \"%s\"' % title
        try:
            call(["osascript", "-e", cmd])
        except:pass
    elif platform.system() == 'Linux':
        pass

def log(movie_name):
    if not os.path.exists("history"):
        open('history','w').close()

    with open('history','a') as f:
        f.write(movie_name + "\n")



class Downloader:
    _default = 1
    _axel = 2
    _aria2 = 3

    def __init__(self):
        self.dir, self.downloader,self.aria2_rpc,self.aria2_token = self.ConfigReader().getConfig()

    def download(self, url, filename):
        url = unquote(url)
        if self.downloader == self._default:
            self.RequestDownloader().download(url, self.dir, filename)
        elif self.downloader == self._axel:
            self.AxelDownloader().download(url, self.dir, filename)
        elif self.downloader == self._aria2:
            self.Aria2Downloader(self.aria2_rpc,self.aria2_token).download(url, self.dir, filename)
        else:
            print("Error: 下载器配置错误: %s" % self.downloader)
            exit()

    class RequestDownloader:

        def Schedule(self, a, b, c):
            '''
            :param a: 已经下载的代码块
            :param b: 数据块的大小
            :param c: 远程文件的大小
            '''
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print(":%.3f/%.3f MB [%.2f%%]" % (a * b / 1048576, c / 1048576, per), end='\r')

        def download(self, url, dir, filename):
            ## 默认方法下载
            try:
                print("* 开始下载 %s..." % filename)
                urllib.request.urlretrieve(url, dir + os.sep + filename, self.Schedule)
                show_notify_on_mac("Nadner", "下载完成: " + filename)
            except urllib.error.URLError:
                print("Error:连接被拒绝")
                return -1

    class AxelDownloader:
        def download(self, url, dir, filename):
            filename = filename.replace("(", " ")
            filename = filename.replace(")", " ")
            filename = filename.replace(" ", "\ ")

            try:
                print("* 开始下载 %s" % filename)
                os.system("axel -n 2 %s -o %s -a" % (url, (dir + os.sep + filename)))
                show_notify_on_mac("Nadner", "下载完成: " + filename)
            except BaseException as e:
                print(e)
                print("调用 axel 错误")
                return -1

    class Aria2Downloader:
        def __init__(self,rpc,token):
            self.rpc = rpc
            self.token = token
        def download(self, url, dir, filename):
            try:
                s = xmlrpc.client.ServerProxy(self.rpc)
                s.aria2.addUri("token:%s"%self.token, [url], {"out": filename})  # 添加下载链接
                print("* 提交任务成功 : %s" % filename)
                show_notify_on_mac("Nadner", "提交任务成功: " + filename)
            except BaseException as e:
                print(e)

    class ConfigReader:
        def __init__(self, path=BaseDir + os.sep +'config', encoding='utf-8'):
            self._path = path
            self._encoding = encoding
            self.cf = configparser.ConfigParser()


        def getConfig(self):
            if not os.path.exists(BaseDir + os.sep + "config"):
                with open(BaseDir + os.sep + "config", 'w') as f:
                    f.write("[download]\n")
                    f.write("download_path=%s\n"%BaseDir+os.sep+'downloads')
                    f.write("downloader=1\n")
                    if not os.path.exists(BaseDir + os.sep + 'downloads'):
                        os.mkdir(BaseDir + os.sep + 'downloads')

                    f.write("[aria2]\n")
                    f.write("jsonrpc=http://localhost:6800/rpc\n")
                    f.write("token= \n")

            self.cf.read(self._path, self._encoding)
            download_path = self.cf.get('download', "download_path")
            downloader = self.cf.getint('download', "downloader")
            aria2_rpc = self.cf.get('aria2','rpc')
            aria2_token = self.cf.get('aria2','token')
            return download_path, downloader,aria2_rpc,aria2_token


if __name__ == '__main__':
    Downloader().ConfigReader().getConfig()
