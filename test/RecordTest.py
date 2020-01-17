# coding=utf-8
import live_recorder

if __name__ == '__main__':
#     recorder = live_recorder.Recorder.createRecorder('bili', 903363, check_flv = False,
#                                     save_folder = '../download', delete_origin_file = True)
    # recorder = live_recorder.Recorder.createRecorder('douyu', 35954, check_flv = False)3xu46dsqc5eyp6e
    recorder = live_recorder.Recorder.createRecorder('kuaishou', 'Yxlmhuige', check_flv = True, cookies = None)
    # recorder = live_recorder.DouyuRecorder(312212, check_flv = False)
    
    # 获取房间信息
    roomInfo = recorder.getRoomInfo()
    print(roomInfo)
    
    # 获取如果在直播，那么录制
    if roomInfo['live_status'] == '1':
        print(roomInfo['live_rates'])
        qn = input("输入要录制的清晰度\r\n")
        live_url = recorder.getLiveUrl(qn = qn) #请查看roomInfo['live_rates']
        print(live_url)
        download_thread = live_recorder.DownloadThread(recorder)
        monitoring_thread = live_recorder.MonitoringThread(recorder)
          
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