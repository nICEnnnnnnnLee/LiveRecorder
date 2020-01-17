# coding=utf-8
import live_recorder

def createRecorder(liver, short_id, **args):
    if liver == 'bili':
        recorder = live_recorder.BiliRecorder(short_id, **args)
    elif liver == 'douyu':
        recorder = live_recorder.DouyuRecorder(short_id, **args)
    elif liver == 'kuaishou':
        recorder = live_recorder.KuaishouRecorder(short_id, **args)
    else:
        recorder = None
    return recorder
