# coding=utf-8
import requests
import os
import time
import re
from .flv_checker import Flv

class BaseRecorder:

    def __init__(self, short_id, cookies = None, \
                 save_folder = '../download', \
                 flv_save_folder = None, \
                 delete_origin_file = False, check_flv = True,\
                 file_name_format = "{name}-{shortId} 的{liver}直播{startTime}-{endTime}",\
                 time_format = "%Y%m%d_%H-%M",\
                 debug = False):
        self.short_id = str(short_id)
        self.cookies = cookies
        self.delete_origin_file = delete_origin_file
        self.check_flv = check_flv
        
        self.save_folder = save_folder.rstrip('\\').rstrip('/')
        self.flv_save_folder = flv_save_folder
        self.file_name_format = file_name_format
        self.time_format = time_format
        self.debug = debug
        
        
        
        self.downloaded = 0
        self.downloadFlag = True
    
#     def getRoomInfo(self):
#         roomInfo = {}
#         roomInfo['short_id'] = self.short_id
#         roomInfo['room_id'] = searchObj.group(1)
#         roomInfo['live_status'] = searchObj.group(1)
#         roomInfo['room_title'] = searchObj.group(1)
#         roomInfo['room_description'] = searchObj.group(1)
#         roomInfo['room_owner_id'] = searchObj.group(1)
#         roomInfo['room_owner_name'] = searchObj.group(1)
#         if roomInfo['live_status'] == '1':
#             roomInfo['live_rates'] = quality
#         return roomInfo
        
#     def getLiveUrl(self, qn):
#         if not hasattr(self, 'roomInfo'):
#             self.getRoomInfo()
#         if self.roomInfo['live_status'] != '1':
#             print('当前没有在直播')
#             return None
#         self.live_url = ""
#         self.live_qn = ""
#         return self.live_url
    
    def startRecord(self, path = None, qn = 0, headers = None):
        try:
            if not hasattr(self, 'live_url'):
                self.getLiveUrl(qn)
            if hasattr(self, 'download_headers'):
                headers = self.download_headers
                
            if path == None:
                # 如果没有指定path，根据自定义文件名来生成
                roomInfo = self.roomInfo
                filename = self.file_name_format.replace("{name}", roomInfo['room_owner_name'])
                filename = filename.replace("{shortId}", roomInfo['short_id'])
                filename = filename.replace("{roomId}", roomInfo['room_id'])
                filename = filename.replace("{liver}", self.liver)
                filename = filename.replace("{seq}", '0')
                current_time = time.strftime(self.time_format, time.localtime())
                filename = filename.replace("{startTime}", current_time)
                filename = re.sub(r"[\/\\\:\?\"\<\>\|']", '_', filename)
                
                if not os.path.exists(self.save_folder):
                    os.makedirs(self.save_folder)
                
                path = os.path.abspath('{}/{}.flv'.format(self.save_folder, filename))
            
            with open(path,"wb") as file:
                response = requests.get(self.live_url, stream=True, headers=headers, timeout=120)
                for data in response.iter_content(chunk_size=1024*1024):
                    if not self.downloadFlag:
                        break
                    if data:
                        file.write(data)
                        self.downloaded += len(data)
                response.close()
            
            if '{endTime}' in path:
                current_time = time.strftime(self.time_format, time.localtime())
                filename = filename.replace("{endTime}", current_time)
                filename = re.sub(r"[\/\\\:\*\?\"\<\>\|\s']", '_', filename)
                new_path = os.path.abspath('{}/{}.flv'.format(self.save_folder, filename))
                os.rename(path, new_path)
                path = new_path
            
            if self.check_flv:
                print("正在校准时间戳")
                flv = Flv(path, self.flv_save_folder, self.debug)
                flv.check()
                if self.delete_origin_file:
                    os.remove(path)
            
            self.downloadFlag = False
            
        except Exception as e:
            print(e)
            self.downloadFlag = False
            raise e
            
    def stopRecord(self):
        self.downloadFlag = False

