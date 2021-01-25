# coding=utf-8
import requests
from ._base_recorder import BaseRecorder

class BiliRecorder(BaseRecorder):
    liver = 'bili'
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
        
    
    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        
        url = "https://api.live.bilibili.com/room/v1/Room/get_info?id=%s&from=room"%self.short_id
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Origin': 'https://live.bilibili.com',
            'Referer': 'https://live.bilibili.com/blanc/%s'%self.short_id,
            'X-Requested-With': 'ShockwaveFlash/28.0.0.137',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        }
        data_json = requests.get(url, timeout=10, headers=headers).json()['data']
        roomInfo['room_id'] = str(data_json['room_id'])
        roomInfo['live_status'] = str(data_json['live_status'])
        roomInfo['room_title'] = data_json['title']
        roomInfo['room_description'] = data_json['description']
        roomInfo['room_owner_id'] = data_json['uid']
        
        if roomInfo['live_status'] == '1':
            url = "https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid=%s"%roomInfo['room_id']
            data_json = requests.get(url, timeout=10, headers=headers).json()['data']
            roomInfo['room_owner_name'] = data_json['info']['uname']
            
            quality = {}
            url = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=%s&platform=web"%(roomInfo['room_id'], 0)
            multirates = requests.get(url, timeout=10, headers=headers).json()['data']['quality_description']
            for rate in multirates:
                quality[str(rate['qn'])] = rate['desc']
            roomInfo['live_rates'] = quality
        self.headers = headers    
        self.roomInfo = roomInfo    
        return roomInfo
        
    def getLiveUrl(self, qn):
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        url = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=%s&platform=web"%(self.roomInfo['room_id'], qn)
        data_json = requests.get(url, timeout=10, headers=self.headers).json()['data']
#         print(data_json)
        self.live_url = data_json['durl'][0]['url']
#         self.live_qn = data_json['current_quality']
        self.live_qn = data_json['current_qn']
        print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, self.live_qn))
        self.download_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Origin': 'https://live.bilibili.com',
            'Referer': 'https://live.bilibili.com/%s'%self.short_id,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        }
        return self.live_url