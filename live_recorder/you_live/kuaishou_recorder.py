# coding=utf-8
import requests
from ._base_recorder import BaseRecorder, recorder

@recorder(liver = 'kuaishou')
class KuaishouRecorder(BaseRecorder):
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
    
    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        roomInfo['room_id'] = self.short_id
        
        url = "https://live.kuaishou.com/graphql"
        param = "{\"operationName\":\"userInfoQuery\",\"variables\":{\"principalId\":\"%s\"\
            },\"query\":\"query userInfoQuery($principalId: String) {\\n  userInfo(principalId: $principalId) {\\n\
            id\\n    principalId\\n    kwaiId\\n    eid\\n    userId\\n    profile\\n    name\\n    description\\n    sex\\n\
            constellation\\n    cityName\\n    living\\n    watchingCount\\n    isNew\\n    privacy\\n    feeds {\\n\
            eid\\n      photoId\\n      thumbnailUrl\\n      timestamp\\n      __typename\\n    }\\n    verifiedStatus {\\n\
            verified\\n      description\\n      type\\n      new\\n      __typename\\n    }\\n    countsInfo {\\n\
            fan\\n      follow\\n      photo\\n      liked\\n      open\\n      playback\\n      private\\n      __typename\\n\
            }\\n    bannedStatus {\\n      banned\\n      defriend\\n      isolate\\n      socialBanned\\n      __typename\\n\
            }\\n    __typename\\n  }\\n}\\n\"}"%self.short_id
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
        if not self.cookies is None:
            headers['Cookie'] = self.cookies
        
        user_data_json = requests.post(url, timeout=10, headers=headers, data=param).json()['data']['userInfo']
        
        self.param="{\"operationName\":\"LiveDetail\",\"variables\":{\"principalId\":\"%s\"\
            },\"query\":\"query LiveDetail($principalId: String) {\\n  liveDetail(principalId: $principalId) {\\n\
            liveStream\\n    feedInfo {\\n      pullCycleMillis\\n      __typename\\n    }\\n    watchingInfo {\\n\
            likeCount\\n      watchingCount\\n      __typename\\n    }\\n    noticeList {\\n      feed\\n      options\\n\
            __typename\\n    }\\n    fastComments\\n    commentColors\\n    moreRecommendList {\\n      user{\\n\
            id\\n        profile\\n        name\\n        __typename\\n      }\\n      watchingCount\\n\
            src\\n      title\\n      gameId\\n      gameName\\n      categoryId\\n      liveStreamId\\n      playUrls {\\n\
            quality\\n        url\\n        __typename\\n      }\\n      quality\\n      gameInfo {\\n category\\n\
            name\\n        pubgSurvival\\n        type\\n        kingHero\\n        __typename\\n}\\n\
            redPack\\n      liveGuess\\n      expTag\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"\
            }\r\n"%self.short_id

        live_data_json = requests.post(url, timeout=10, headers=headers, data=self.param).json()['data']['webLiveDetail']['liveStream']
        print(user_data_json)
        print(live_data_json)
        
        if live_data_json['playUrls']:
            roomInfo['live_status'] = '1'
            roomInfo['room_title'] = live_data_json['caption']
            roomInfo['live_rates'] = {}
            i = 0
            for rate in live_data_json['playUrls']:
                roomInfo['live_rates'][i] = rate['quality']
                i += 1
        else:
            roomInfo['live_status'] = '0'
            
        if user_data_json != None and user_data_json['id'] != None:
            roomInfo['room_owner_id'] = user_data_json['userId']
            roomInfo['room_owner_name'] = user_data_json['name']
            roomInfo['room_description'] = user_data_json['description']
        else:
            print("当前Cookie无效，将无法获取到房间详细信息")
            roomInfo['room_owner_id'] = 0
            roomInfo['room_owner_name'] = '空'
            roomInfo['room_description'] = '无'

        self.headers = headers    
        self.roomInfo = roomInfo    
        return roomInfo
        
    def getLiveUrl(self, qn):
        qn = int(qn)
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        live_data_json = requests.post("https://live.kuaishou.com/graphql", timeout=10, headers=self.headers, data=self.param).json()['data']['webLiveDetail']['liveStream']
        self.live_url = live_data_json['playUrls'][qn]['url']
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