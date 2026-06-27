# coding=utf-8
import requests
from ._base_recorder import BaseRecorder, recorder

@recorder(liver = 'bili')
class BiliRecorder(BaseRecorder):
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
        
    
    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Origin': 'https://live.bilibili.com',
            'Referer': 'https://live.bilibili.com/blanc/%s'%self.short_id,
            'X-Requested-With': 'ShockwaveFlash/28.0.0.137',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        }
        if not self.cookies is None:
            headers['Cookie'] = self.cookies
        
        url = "https://api.live.bilibili.com/room/v1/Room/get_info?id=%s&from=room"%self.short_id
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
            url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo"
            params = {
                'room_id': roomInfo['room_id'],
                'protocol': '0,1',
                'format': '0,1,2',
                'codec': '0,1',
                'qn': '0',
                'platform': 'web',
                'ptype': '8',
            }
            playinfo = requests.get(url, params=params, timeout=10, headers=headers).json()
            if playinfo['code'] == 0:
                playurl = playinfo['data']['playurl_info']['playurl']
                if playurl:
                    g_qn_desc = playurl.get('g_qn_desc', [])
                    desc_map = {qn_info['qn']: qn_info['desc'] for qn_info in g_qn_desc}
                    try:
                        accept_qn = playurl['stream'][0]['format'][0]['codec'][0]['accept_qn']
                    except (KeyError, IndexError, TypeError):
                        accept_qn = list(desc_map.keys())
                    for qn_val in accept_qn:
                        quality[str(qn_val)] = desc_map.get(qn_val, str(qn_val))
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
        
        url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo"
        params = {
            'room_id': self.roomInfo['room_id'],
            'protocol': '0,1',
            'format': '0,1,2',
            'codec': '0,1',
            'qn': qn,
            'platform': 'web',
            'ptype': '8',
        }
        data_json = requests.get(url, params=params, timeout=10, headers=self.headers).json()
        if data_json['code'] == 0:
            try:
                playurl = data_json['data']['playurl_info']['playurl']
                if playurl and playurl.get('stream'):
                    stream = playurl['stream'][0]
                    for fmt in stream['format']:
                        if fmt['format_name'] == 'flv':
                            codec_info = fmt['codec'][0]
                            self.live_qn = codec_info['current_qn']
                            url_info = codec_info['url_info'][0]
                            self.live_url = url_info['host'] + codec_info['base_url'] + url_info['extra']
                            print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, self.live_qn))
                            self.download_headers = {
                                'Accept': 'application/json, text/plain, */*',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                                'Origin': 'https://live.bilibili.com',
                                'Referer': 'https://live.bilibili.com/%s'%self.short_id,
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                            }
                            if not self.cookies is None:
                                self.download_headers['Cookie'] = self.cookies
                            return self.live_url
            except (KeyError, IndexError, TypeError):
                pass
        
        url = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=%s&platform=web"%(self.roomInfo['room_id'], qn)
        data_json = requests.get(url, timeout=10, headers=self.headers).json()['data']
        self.live_url = data_json['durl'][0]['url']
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
        if not self.cookies is None:
            self.download_headers['Cookie'] = self.cookies
        return self.live_url