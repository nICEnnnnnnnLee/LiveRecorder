# coding=utf-8
from .douyu_recorder import DouyuRecorder
from .bili_recorder import BiliRecorder
from .kuaishou_recorder import KuaishouRecorder

def createRecorder(liver, short_id, **args):
    if liver == 'bili':
        recorder = BiliRecorder(short_id, **args)
    elif liver == 'douyu':
        recorder = DouyuRecorder(short_id, **args)
    elif liver == 'kuaishou':
        recorder = KuaishouRecorder(short_id, **args)
    else:
        recorder = None
    return recorder
