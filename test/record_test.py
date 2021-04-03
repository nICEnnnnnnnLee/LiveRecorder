# coding=utf-8
import sys
sys.path[1] = r"D:\Workspace\javaweb-springboot\LiveRecorder\\"
from live_recorder import you_live

if __name__ == '__main__':
#    recorder = you_live.Recorder.createRecorder('bili', 7734200, check_flv = False,\
#                                      save_folder = '../download', delete_origin_file = True)
#    recorder = you_live.Recorder.createRecorder('douyu', 312212, check_flv = False, cookies = "acf_did=1474ee6ad3fff7616c76b88200011501; dy_did=1474ee6ad3fff7616c76b88200011501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1615709433,1616551448,1616722268,1617427549; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar_v3%2F201812%2F069809f62815f6d7ca106f786a5c89b3_; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1617427557; PHPSESSID=mrifqo3j1dk659lohpsapi6ci2; acf_auth=5699TLLSYBQVjqW5MRw6CdV%2FO4QZzytmXVxowZHfDHvS7uRukRVPaMcRBtWOf4QmJUbKywTltReQ%2FiOXBjRCM1TMcZurTfn7nqfNGPdrN67BizE6J7Nrj8U; dy_auth=b69cbCbSelxAo%2BT8suQjk43vWuiT9MnVIzZPWf8linIrX%2BT7iwnlyFxZTML4p%2BrFbHEeZyrc0Ceufk%2F07C4bGbNNHthKR1nrhJljaSWn4BZPt4rBji5Vy8g; wan_auth37wan=45e5ec57d6eecAERPwNXJdwb2gHcoDtFVrz9qb5%2BGD3xLC7b69INuVLGMyRLiqaW7CwKzmFAJ3DjHGWQsevZeHAXYxwYjE9QMEhEU5%2FWsCpgow3llQo; acf_uid=224961119; acf_username=224961119; acf_nickname=%E6%9F%B4%E5%8F%AF%E5%A4%AB%E8%80%81%E5%8F%B8%E5%9F%BA; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_ct=0; acf_ltkid=67003147; acf_biz=1; acf_stk=8719110960b818fc")
    recorder = you_live.Recorder.createRecorder('kuaishou', 'zxc774882278', check_flv = False, cookies = None)
#     recorder = you_live.Recorder.createRecorder('acfun', '40909488', check_flv = True, cookies = None)
#     recorder = you_live.DouyuRecorder(312212, check_flv = False)
    
    # 获取房间信息
    roomInfo = recorder.getRoomInfo()
    print(roomInfo)
    
    # 获取如果在直播，那么录制
    if roomInfo['live_status'] == '1':
        print(roomInfo['live_rates'])
        qn = input("输入要录制的清晰度")
        live_url = recorder.getLiveUrl(qn = qn) #请查看roomInfo['live_rates']
        print(live_url)
        download_thread = you_live.DownloadThread(recorder)
        monitoring_thread = you_live.MonitoringThread(recorder)
          
        download_thread.start()
        monitoring_thread.start()
          
        while recorder.downloadFlag:
            todo = input("输入q或stop停止录制\r\n")
            if todo == "q" or todo == "stop":
                recorder.downloadFlag = False
            else:
                print("请输入合法命令！！！")
    else:
        print("主播当前不在线!!")