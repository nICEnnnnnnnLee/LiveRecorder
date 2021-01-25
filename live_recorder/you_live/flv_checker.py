# coding=utf-8
import os
import struct

class Flv(object):

    def __init__(self, path, dest_folder = None, debug = False):
        self.path = path
        self.debug = debug
        if dest_folder != None:
            self.dest_folder = dest_folder.rstrip('\\').rstrip('/')
        else:
            self.dest_folder = None
     
     
     
    def check(self):
        if self.dest_folder == None:
            file_folder = os.path.dirname(os.path.realpath(self.path))
        else:
            file_folder = self.dest_folder
        file_name = os.path.basename(os.path.realpath(self.path))
        file_short_name, file_extension = os.path.splitext(file_name)

        path_new = os.path.join(file_folder, file_short_name + '-checked0.flv')
        print(path_new)
        with open(self.path,"rb") as origin:
            with open(path_new,"wb+") as dest:
                # 复制头部
                data = origin.read(9)
                dest.write(data)
                # 处理Tag内容
                self.checkTag(origin, dest)
        
        self.changeDuration(self.path, float(self.lastTimestampWrite[b'\x08']) / 1000)    

    def checkTag(self, origin, dest):
        currentLength = 9
        latsValidLength = currentLength
        
        self.lastTimestampRead = { b'\x08':-1, b'\x09':-1 }
        self.lastTimestampWrite = { b'\x08':-1, b'\x09':-1 }
        
        isFirstScriptTag = True
        remain = 10
        while True:# and remain >0:
            remain -=1
            # 读取前一个tag size
            data = origin.read(4)
#             predataSize = int.from_bytes(data, byteorder='big', signed=False)
#             print("前一个 tagSize：", predataSize)
            dest.write(data)
            # 记录当前新文件位置，若下一tag无效，则需要回退
            latsValidLength = currentLength
            currentLength = dest.tell()
            
            # 读取tag类型
            tagType = origin.read(1)
#             print("当前tag 类型为：", tagType)
            if tagType == b'\x08' or tagType == b'\x09': # 8/9 audio/video
                dest.write(tagType)
                # tag data size 3个字节。表示tag data的长度。从streamd id 后算起。
                data = origin.read(3)
                dest.write(data)
                dataSize = int.from_bytes(data, byteorder='big', signed=False)
#                 print("当前tag data 长度为：", dataSize)
                
                # 时间戳 3 + 1
                timeData = origin.read(3)
                timeDataEx = origin.read(1)
                timestamp = int.from_bytes(timeData, byteorder='big', signed=False)
                timestamp |= (int.from_bytes(timeDataEx, byteorder='big', signed=False) << 24)
                self.dealTimeStamp(dest, timestamp, tagType)
#                 print("当前timestamp 长度为：", timestamp)
                
                # 数据
                data = origin.read(3 + dataSize)
                dest.write(data)
            elif tagType == b'\x12': # scripts
                # 如果是scripts脚本，默认为第一个tag，此时将前一个tag Size 置零
                dest.seek(dest.tell() - 4)
                dest.write(b'\x00\x00\x00\x00')
                dest.write(tagType)
                isFirstScriptTag = False
                # tag data size 3个字节。表示tag data的长度。从streamd id 后算起。
                data = origin.read(3)
                dest.write(data)
                dataSize = int.from_bytes(data, byteorder='big', signed=False)
#                 print("当前tag data 长度为：" , dataSize)
                # 时间戳 0
                origin.read(4)
                dest.write(b'\x00\x00\x00\x00')
                # 数据
                data = origin.read(3 + dataSize)
                dest.write(data)
            else:
                if self.debug:
                    print("未知类型", tagType)
                dest.truncate(latsValidLength)
                break
            
    def dealTimeStamp(self, dest, timestamp, tagType):   
#         print("上一帧读取timestamps 为：" , self.lastTimestampRead[tagType])  
#         print("上一帧写入timestamps 为：" , self.lastTimestampWrite[tagType])  
        # 如果是首帧
        if self.lastTimestampRead[tagType] == -1:
            self.lastTimestampWrite[tagType] = 0
        elif timestamp >= self.lastTimestampRead[tagType]: # 如果时序正常
            # 间隔十分巨大(1s)，那么重新开始即可
            if timestamp > self.lastTimestampRead[tagType] + 1000:
                self.lastTimestampWrite[tagType] += 10
                if self.debug:
                    print("---")
            else:
                self.lastTimestampWrite[tagType] = timestamp - self.lastTimestampRead[tagType] + self.lastTimestampWrite[tagType]
        else:  #如果出现倒序时间戳
            # 如果间隔不大，那么如实反馈
            if self.lastTimestampRead[tagType] - timestamp < 5 * 1000:
                tmp = timestamp - self.lastTimestampRead[tagType] + self.lastTimestampWrite[tagType]
                if tmp < 0 : tmp = 1
                self.lastTimestampWrite[tagType] = tmp
            else: # 间隔十分巨大，那么重新开始即可
                self.lastTimestampWrite[tagType] += 10
                if self.debug:
                    print("---rewind")
        self.lastTimestampRead[tagType] = timestamp
 
        # 低于0xffffff部分
        lowCurrenttime = self.lastTimestampWrite[tagType] & 0xffffff
        dest.write(lowCurrenttime.to_bytes(3,byteorder='big'))
        # 高于0xffffff部分
        highCurrenttime = self.lastTimestampWrite[tagType] >> 24
        dest.write(highCurrenttime.to_bytes(1,byteorder='big'))
        if self.debug:
            print(" 读取timestamps 为：%s, 写入timestamps 为：%s"%(timestamp, self.lastTimestampWrite[tagType]))
    
    
    def changeDuration(self, path, duration):
        if self.debug:
            print(duration)
        durationHeader = b"\x08\x64\x75\x72\x61\x74\x69\x6f\x6e"
        pointer = 0
        # 先找到 08 64 75 72 61 74 69 6f 6e所在位置
        with open(path,"rb+") as file:
            data = file.read(1024*20)
            i = 0
            findHeader = False
            while i < len(data):
                if data[i] == durationHeader[pointer]:
                    pointer += 1
                    # 如果完全包含durationHeader头部，则可以返回
                    if pointer == len(durationHeader):
                        findHeader = True
                        break;
                else:
                    pointer = 0
                i += 1
                
            if findHeader:
                file.seek(i + 1);
                file.write(b"\x00")
                file.write(struct.pack('>d', duration))
            else:
                if self.debug:
                    print("没有找到duration标签")
        
        
if __name__ == '__main__':
    flv = Flv(r"D:\Workspace\PythonWork\LiveRecorder\live\test-checked0.flv")
    flv = Flv(r"test.flv")
    flv.check()
#     flv.changeDuration(flv.path, 123)
