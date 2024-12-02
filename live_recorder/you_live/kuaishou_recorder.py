# coding=utf-8
import requests, re, json
from ._base_recorder import BaseRecorder, recorder

@recorder(liver = 'kuaishou')
class KuaishouRecorder(BaseRecorder):
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
    
    def getLiveInfo(self):
        url = "https://live.kuaishou.com/u/" + self.short_id
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'content-type': 'application/json',
            'Origin': 'https://live.kuaishou.com',
            'Referer': 'https://live.kuaishou.com/u/%s'%self.short_id,
            'X-Requested-With': 'ShockwaveFlash/28.0.0.137',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        }
        self.headers = headers
        if not self.cookies is None:
            headers['Cookie'] = self.cookies
            
        html = requests.get(url, timeout=10, headers=headers).text
        searchObj = re.search("window\\.__INITIAL_STATE__ *= *(\\{.*?\\}) *; *\\(function\\(\\)", html)
        json_raw = searchObj.group(1)
        #print(json_raw)
        json_str = json_raw.replace("undefined", "null")
        return json.loads(json_str)["liveroom"]["playList"][0]

    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        roomInfo['room_id'] = self.short_id
        
        if self.cookies is None:
            print('缺少cookies(无需登录)')
            return None
            
        room_json = self.getLiveInfo()
        live_data_json = room_json["liveStream"]
        user_data_json = room_json["author"]
        if live_data_json and ("h264" in live_data_json["playUrls"]) and ("adaptationSet" in live_data_json["playUrls"]["h264"]):
            roomInfo['live_status'] = '1'
            roomInfo['room_title'] = live_data_json.get('caption', '空')
            roomInfo['live_rates'] = {}
            i = 0
            for rate in live_data_json['playUrls']["h264"]["adaptationSet"]["representation"]:
                key = int(rate["id"])
                roomInfo['live_rates'][key] = rate['name']
                i += 1
        else:
            roomInfo['live_status'] = '0'
        
        roomInfo['room_owner_id'] = user_data_json['originUserId']
        roomInfo['room_owner_name'] = user_data_json['name']
        roomInfo['room_description'] = user_data_json['description']

        
        self.roomInfo = roomInfo    
        return roomInfo
        
    def getLiveUrl(self, qn):
        qn = int(qn)
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        live_data_json = self.getLiveInfo()
        self.live_url = live_data_json["liveStream"]['playUrls']["h264"]["adaptationSet"]["representation"][qn]['url']
        self.live_qn = qn
        print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, self.live_qn))
#         self.download_headers = {
#             'Accept': 'application/json, text/plain, */*',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#             'Origin': 'https://live.bilibili.com',
#             'Referer': 'https://live.bilibili.com/%s'%self.short_id,
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
#         }
        return self.live_url