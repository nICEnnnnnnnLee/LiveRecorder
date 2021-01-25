# coding=utf-8
import requests
import re
import json
from ._base_recorder import BaseRecorder

class AcfunRecorder(BaseRecorder):
    liver = 'acfun'
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
        
    
    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        roomInfo['room_id'] = self.short_id
        roomInfo['room_owner_id'] = self.short_id
        h_session = requests.session()
        
        # 先访问获取cookie
        common_url = "https://m.acfun.cn/live/detail/%s"%self.short_id
        common_headers = {
            'Host': "m.acfun.cn",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        }
        html = h_session.get(common_url, timeout=10, headers=common_headers).text
#         with open('html.txt', 'w', encoding='utf-8') as f:
#             f.write(html)
        searchObj = re.search(r"<title>(.*?)正在直播", html)
        roomInfo['room_owner_name'] = searchObj.group(1)
        
        if "直播已结束" in html:
            roomInfo['live_status'] = '0'
        else:
            roomInfo['live_status'] = '1'
        
        if roomInfo['live_status'] == '1':
            searchObj = re.search(r'<h1 class="live-content-title-text">(.*?)</h1>', html)
            roomInfo['room_title'] = searchObj.group(1)
            roomInfo['room_description'] = roomInfo['room_title']
            
            # 从cookie获取did参数
            _did = dict(h_session.cookies)['_did']
            
            # 游客登录，获取参数
            login_url = "https://id.app.acfun.cn/rest/app/visitor/login";
            login_param = {'sid':'acfun.api.visitor'}
            login_headers = {
                'Host': "id.app.acfun.cn",
                'Accept': "application/json, text/plain, */*",
                'Content-Type': "application/x-www-form-urlencoded",
                'Origin': "https://m.acfun.cn",
                'Referer': "https://m.acfun.cn",
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            }
            data_json = h_session.post(login_url, login_param, timeout=10, headers=login_headers).json()
            userId = data_json['userId']
            api_st = data_json['acfun.api.visitor_st']   
                     
            #根据参数组装，获取直播可提供的清晰度
            self.query_url = "https://api.kuaishouzt.com/rest/zt/live/web/startPlay?subBiz=mainApp&kpn=ACFUN_APP&userId=%s&did=%s&acfun.api.visitor_st=%s"%(userId, _did, api_st)
            self.query_param = {'authorId':self.short_id}
            self.query_headers = {
                'Host': "api.kuaishouzt.com",
                'Accept': "application/json, text/plain, */*",
                'Content-Type': "application/x-www-form-urlencoded",
                'Origin': "https://m.acfun.cn",
                'Referer': "https://m.acfun.cn/live/detail/%s"%self.short_id,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            }
            data_json = h_session.post(self.query_url, self.query_param, timeout=10, headers=self.query_headers).json()["data"]
            # 
            qnArray = json.loads(data_json['videoPlayRes'])['liveAdaptiveManifest'][0]['adaptationSet']['representation']
            quality = {}
            for rate in qnArray:
                quality[str(rate['id'])] = rate['name']
            roomInfo['live_rates'] = quality
#         self.headers = headers    
        self.roomInfo = roomInfo
        self.session = h_session
        return roomInfo
        
    def getLiveUrl(self, qn):
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        data_json = self.session.post(self.query_url, self.query_param, timeout=10, headers=self.query_headers).json()["data"]
        # 
        qnArray = json.loads(data_json['videoPlayRes'])['liveAdaptiveManifest'][0]['adaptationSet']['representation']
        print(qnArray[0])
        for rate in qnArray:
            if qn == str(rate['id']):
                self.live_url = rate['url']
                self.live_qn = rate['id']
                break
        
        if not hasattr(self, 'live_url'):
            self.live_url = qnArray[0]['url']
            self.live_qn = qnArray[0]['id']
            
        print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, self.live_qn))
        self.download_headers = {
            'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        }
        return self.live_url
