# coding=utf-8
import threading
import time
import sys

class MonitoringThread(threading.Thread):


    def __init__(self, live_recorder):
        threading.Thread.__init__(self)
        self.live_recorder = live_recorder
        
    def run(self):
        self.begin_time = time.time()
        while self.live_recorder.downloadFlag :
            time.sleep(10)
            self.current_time = time.time()
            print("当前已经录制了%s, 录制文件大小为%s"%(\
                        self.formatTime(self.current_time - self.begin_time),\
                        self.formatSize(self.live_recorder.downloaded)))
        print("监控线程已经结束")
        sys.exit()
        
    def formatTime(self, time):   
        time = int(time) 
        seconds = time % 60
        time = int(time / 60)
        minutes = time % 60
        hours = int(time / 60)
        if hours > 0:
            return "%dh %dmin %ds"%(hours, minutes, seconds)
        elif minutes > 0:
            return "%dmin %ds"%(minutes, seconds)
        else:
            return "%ds"%seconds
    
    KB = 1024;
    MB = KB * 1024;
    GB = MB * 1024;    
    def formatSize(self, size):   
        if size > MonitoringThread.GB:
            return "%.2fGB"%(size/MonitoringThread.GB)
        elif size > MonitoringThread.MB:
            return "%.1fMB"%(size/MonitoringThread.MB)
        else:
            return "%.1fKB"%(size/MonitoringThread.KB)