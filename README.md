you-live
===========================
![](https://img.shields.io/badge/Python-3-green.svg) ![](https://img.shields.io/badge/require-requests-green.svg)![](https://img.shields.io/badge/require-PyExecJS-green.svg)
### Live Recorder
A live recorder focus on China mainland livestream sites.   
Brother Repo of [BilibiliLiveRecorder](https://github.com/nICEnnnnnnnLee/BilibiliLiveRecorder)(java)  

    
****
## :dolphin:Installation
```
Linux/debian:

    sudo apt-get install python3-pip
    pip3 install you-live --upgrade --user
    add ~/.local/bin to your PATH

Windows:

    install python3 from python.org
    pip install --upgrade you-live

Other Linux: please follow debian

Other OS: please DIY.
```

## :dolphin:Usage
```
you-live [-h] [-qn QN] [-debug] [-check] [-delete] [-save_path SAVE_PATH] [-check_path CHECK_PATH]
                [-format FORMAT] [-time_format TIME_FORMAT] [-cookies COOKIES] [-cookies_path COOKIES_PATH]
                liver id

B站/斗鱼/快手 直播视频录制

positional arguments:
  liver                 要录制的直播源，如 bili,douyu,kuaishou,acfun
  id                    要录制的房间号，可以从url中直接获取

optional arguments:
  -h, --help            show this help message and exit
  -qn QN, -q QN         录制的清晰度，可以后续输入
  -debug                debug模式
  -check                校准时间戳
  -delete, -d           删除原始文件
  -save_path SAVE_PATH, -sp SAVE_PATH
                        源文件保存路径
  -check_path CHECK_PATH, -chp CHECK_PATH
                        校正后的FLV文件保存路径
  -format FORMAT, -f FORMAT
                        文件命名格式
  -time_format TIME_FORMAT, -tf TIME_FORMAT
                        时间格式
  -cookies COOKIES, -c COOKIES
                        cookie, 当cookies_path未指定时生效
  -cookies_path COOKIES_PATH, -cp COOKIES_PATH
                        指定cookie文件位置
```

### Example0
Record a live from <https://live.bilibili.com/6>
```
you-live bili 6
```

### Example1
Record a live from <https://www.douyu.com/593392>, correct the timestamp error and delete the origin files.
```
you-live -check -d douyu 593392
```
**Notice**:The record on this site(douyu) uses PyExecJS.  
You may need some extra installation about the JS Environment for linux OS.  
Here’s the guide for [Node.js installation](https://github.com/nodesource/distributions)  


**Notice**:You may need logged-in cookies to get high quality videos

### Example2
Record a live from <https://live.kuaishou.com/u/ZFYS8888>, speicify the file name you want.
```
you-live -format "{name}-{shortId} 的{liver}直播{startTime}" kuaishou ZFYS8888
```
**Notice**:You may need cookies(may not logged-in, just skip the captha test) to get room detail information


## :dolphin:LICENSE
MIT 


