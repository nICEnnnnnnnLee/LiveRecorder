import argparse
from live_recorder import you_live
from live_recorder import version

args = None

def arg_parser():
    parser = argparse.ArgumentParser(prog='you-live', description="version %s : %s"%(version.__version__, version.__descriptrion__))
    parser.add_argument("liver", help="要录制的直播源，如 bili,douyu,kuaishou,acfun")
    parser.add_argument("id", help="要录制的房间号，可以从url中直接获取")
    parser.add_argument("-qn", "-q", help="录制的清晰度，可以后续输入", required=False, default=None)
    parser.add_argument("-debug", help="debug模式", required=False, action='store_true', default=False)
    parser.add_argument("-check", help="校准时间戳", required=False, action='store_true', default=False)
    parser.add_argument("-delete", '-d', help="删除原始文件", required=False, action='store_true', default=False)
    parser.add_argument("-save_path", '-sp', help="源文件保存路径", required=False, default='./download')
    parser.add_argument("-check_path", '-chp', help="校正后的FLV文件保存路径", required=False, default=None)
    parser.add_argument("-format", '-f', help="文件命名格式", required=False, default='{name}-{shortId} 的{liver}直播{startTime}-{endTime}')
    parser.add_argument("-time_format", '-tf', help="时间格式", required=False, default='%Y%m%d_%H-%M')
    parser.add_argument("-cookies", '-c', help="cookie, 当cookies_path未指定时生效", required=False, default=None)
    parser.add_argument("-cookies_path", '-cp', help="指定cookie文件位置", required=False, default=None)
    
    global args
    args = parser.parse_args()
#     args = parser.parse_args(('-delete bili 6').split())
#     print(args);

    
def main():
    arg_parser()
    liver = args.liver
    debug = args.debug
    params = {}
    params['save_folder'] = args.save_path
    params['flv_save_folder'] = args.check_path
    params['delete_origin_file'] = args.delete
    params['check_flv'] = args.check
    params['file_name_format'] = args.format
    params['time_format'] = args.time_format
    params['cookies'] = args.cookies
    params['debug'] = args.debug
    if args.cookies_path:
        try:
            with open(args.cookies_path,"r", encoding='utf-8') as f:
                params['cookies'] = f.read()
        except:
            print(args.cookies_path)
            print('指定cookie路径不存在')
    
    recorder = you_live.Recorder.createRecorder(liver, args.id, **params)
     
    # 获取房间信息
    roomInfo = recorder.getRoomInfo()
    if debug:
        print(roomInfo)
     
    # 获取如果在直播，那么录制
    if roomInfo['live_status'] == '1':
        print(roomInfo['live_rates'])
        if args.qn:
            qn = args.qn
        else:
            qn = input("输入要录制的清晰度\r\n")
             
        live_url = recorder.getLiveUrl(qn = qn) 
        if debug:
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

if __name__ == '__main__':
    main()