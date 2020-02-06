# coding=utf-8
from live_recorder import you_live

if __name__ == '__main__':
#     recorder = you_live.Recorder.createRecorder('bili', 903363, check_flv = False,
#                                     save_folder = '../download', delete_origin_file = True)
    recorder = you_live.Recorder.createRecorder('douyu', 198859, check_flv = True)
#     recorder = you_live.Recorder.createRecorder('kuaishou', 'Yxlmhuige', check_flv = True, cookies = None)
    # recorder = you_live.DouyuRecorder(312212, check_flv = False)
    
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