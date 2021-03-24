import os, time
import threading

rlock = threading.RLock()
curPosition = 0  # 初始化位置为文件其实位置


class Reader(threading.Thread):
    def __init__(self, file):
        self.file = file
        super(Reader, self).__init__()  # 调用子类构造函数获得文件大小

    def run(self):
        global curPosition
        global count
        global failcount
        fstream = open(self.file.fileName, 'r')  # 打开文件
        while True:
            rlock.acquire()
            startPosition = curPosition  # 每次更新起始位置
            if (startPosition + self.file.fileSize / threadNum) < self.file.fileSize:  # 多少线程，就将文件分为多少块，每个线程负责一块
                curPosition = endPosition = (startPosition + self.file.fileSize / threadNum)
            else:
                curPosition = endPosition = self.file.fileSize
            rlock.release()

            if startPosition == self.file.fileSize:
                break
            elif startPosition != 0:  # 非第一个文件块
                fstream.seek(startPosition)  # 找到开始位置
                line = fstream.readline()  # 由于这一行在上一个循环中已经读取了，所以先读一行，把这行跳过
            pos = fstream.tell()  # 获取当前的位置
            while pos <= endPosition:
                line = fstream.readline()
                '''
                    对行进行处理
                '''
                pos = fstream.tell()  # 更新坐标
                if pos == self.file.fileSize:  # 如果读到了文件末尾，跳出循环
                    break
        print(failcount)
        fstream.close()


class Resource(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.getFileSize()
        self.fileSize = None

    # 计算文件大小
    def getFileSize(self):
        fstream = open(self.fileName, 'r')
        fstream.seek(0, 2)  # 这里0代表文件开始，2代表文件末尾
        self.fileSize = fstream.tell()
        fstream.close()


if __name__ == '__main__':
    fileName = "C:/Users/xxx/Downloads/testdata.out"
    starttime = time.perf_counter()
    # 线程数
    threadNum = 10
    # 文件
    file = Resource(fileName)
    threads = []
    # 初始化线程
    for i in range(threadNum):
        rdr = Reader(file)
        threads.append(rdr)
    # 开始线程
    for i in range(threadNum):
        threads[i].start()
    for i in range(threadNum):
        threads[i].join()
    print(time.perf_counter() - starttime)
