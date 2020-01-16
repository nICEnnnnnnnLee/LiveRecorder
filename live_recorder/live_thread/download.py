# coding=utf-8
import threading

class DownloadThread(threading.Thread):


    def __init__(self, live_recorder, path = None, qn = '0'):
        threading.Thread.__init__(self)
        self.live_recorder = live_recorder
        self.path = path
        self.qn = qn
        
    def run(self):
        self.live_recorder.startRecord(self.path, qn = self.qn)
        print("下载线程已经结束")
    
