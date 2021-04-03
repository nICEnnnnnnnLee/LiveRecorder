# coding=utf-8
import requests
import execjs
import time
import re
import random
from ._base_recorder import BaseRecorder, recorder
from .resources import crypto_js

@recorder(liver = 'douyu')
class DouyuRecorder(BaseRecorder):
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
        if self.cookies == None:
            self.dy_did = ''.join(random.sample('1234567890qwertyuiopasdfghjklzxcvbnm', 32))
        else:
            searchObj = re.search("dy_did=([^&; ]+)", self.cookies)
            self.dy_did = searchObj.group(1)
    
    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        
        url = "https://www.douyu.com/%s"%self.short_id
        headers = {
            'Origin': 'https://www.douyu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        if not self.cookies is None:
            headers['Cookie'] = self.cookies
            
        http_result = requests.get(url, timeout=10, headers=headers)
#         print(http_result.text)
        searchObj = re.search( r'\$ROOM.room_id ?= ?([0-9]+);', http_result.text)
        
        roomInfo['room_id'] = searchObj.group(1)
        searchObj = re.search( r'\$ROOM.show_status ?= ?([0-9]+);', http_result.text)
        roomInfo['live_status'] = searchObj.group(1)
        searchObj = re.search( r'<h[0-9] class=\"Title-headlineH2\">([^/]*)</h[0-9]>', http_result.text)
        if searchObj:
            roomInfo['room_title'] = searchObj.group(1)
        else:
            searchObj = re.search( r'<title>([^/]*)</title>', http_result.text)
            roomInfo['room_title'] = searchObj.group(1)
        searchObj = re.search( r'<div class=\"AnchorAnnounce\"><h3><span>([^/]*)</span></h3></div>', http_result.text)
        if searchObj:
            roomInfo['room_description'] = searchObj.group(1)
        else:
            roomInfo['room_description'] = '无'
        searchObj = re.search( r'\$ROOM.owner_uid ?= ?([0-9]+);', http_result.text)
        roomInfo['room_owner_id'] = searchObj.group(1)
        searchObj = re.search( r'<a class="Title-anchorName" title="([^"]+)"', http_result.text)
        if searchObj:
            roomInfo['room_owner_name'] = searchObj.group(1)
        else:
            url = "https://www.douyu.com/betard/%s"%roomInfo['room_id']
            room_info_json = requests.get(url, timeout=10, headers=headers).json()
            roomInfo['room_owner_name'] = room_info_json['room']['owner_name']
            roomInfo['room_title'] = room_info_json['room']['room_name']
        
        if roomInfo['live_status'] == '1':
            quality = {}
            #self.api_url = "https://www.douyu.com/lapi/live/getH5Play/%s"%roomInfo['room_id']
            self.api_url = "https://playweb.douyu.com/lapi/live/getH5Play/%s"%roomInfo['room_id']
            
            begin = http_result.text.index("var vdwdae325w_64we")
            end = http_result.text.index("</script>", begin)
            js_code = crypto_js + '\r\n'
            js_code += http_result.text[begin:end]
            self.js_code = js_code
            
            ctx = execjs.compile(js_code)
            param = ctx.call("ub98484234", roomInfo['room_id'], self.dy_did, int(time.time()))    
            param += "&cdn=&rate=%d&ver=%s&iar=0&ive=1"%(0, "Douyu_219052705")
            
            self.api_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'x-requested-with': 'XMLHttpRequest',
                'Origin': 'https://www.douyu.com',
                'Referer': "https://www.douyu.com/topic/xyb01?rid=%s"%self.short_id,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            }
            if not self.cookies is None:
                self.api_headers['Cookie'] = self.cookies
            
            http_result = requests.post(self.api_url, timeout=10, headers=self.api_headers, data=param)
            multirates = http_result.json()['data']['multirates']
            for rate in multirates:
                quality[str(rate['rate'])] = rate['name']
                
            roomInfo['live_rates'] = quality
        
        self.roomInfo = roomInfo    
        return roomInfo
        
    def getLiveUrl(self, qn):
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        ctx = execjs.compile(self.js_code)
        param = ctx.call("ub98484234", self.roomInfo['room_id'], self.dy_did, int(time.time()))    
        param += "&cdn=&rate=%s&ver=%s&iar=0&ive=1"%(qn, "Douyu_219052705")
        json_result = requests.post(self.api_url, timeout=10, headers=self.api_headers, data=param).json()
        
        print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, json_result['data']['rate']))
        header = json_result['data']['rtmp_url']
        tail = json_result['data']['rtmp_live']
        
        self.live_url = header + "/" + tail
        self.live_qn = json_result['data']['rate']
        return self.live_url

