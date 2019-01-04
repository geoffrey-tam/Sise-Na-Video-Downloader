import os
import time

BaseDir = os.path.dirname(os.path.abspath(__file__))


class History:
    def __init__(self, path=BaseDir + os.sep + 'history'):
        self.path = path
        self.max = 20
        self.check_file()

    def check_file(self):
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def get_now_time(self):
        localtime = time.localtime()
        now_time = str(localtime.tm_mon) + "-" + str(localtime.tm_mday) + ' ' + ':'.join(
            [str(localtime.tm_hour), str(localtime.tm_min), str(localtime.tm_sec)])
        return now_time

    def put(self, movie_name):
        self.check_file()
        with open(self.path, 'r+') as f:
            context = f.read()
            f.seek(0,0)
            f.write(self.get_now_time() + " " + movie_name + '\n')
            f.write(context)

    def show(self, page):
        self.check_file()
        need = ''
        start = page * self.max
        end = start + self.max
        with open(self.path, 'r') as f:
            for line_num,line in enumerate(f):
                if line_num >= start and line_num < end and line!='\n':
                    need += line
                elif line_num > end:
                    break
        return need.rstrip('\n')

if __name__ == '__main__':
    history = History()
