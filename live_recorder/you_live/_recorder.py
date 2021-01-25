# coding=utf-8
import sys

recorders = {}
module = sys.modules[__name__[:-10]]

for clazzName in dir(module):
    if 'Recorder' in clazzName and not 'Recorder' == clazzName:
        clazz = getattr(module, clazzName)
        liver = getattr(clazz, "liver")
        recorders[liver] = clazz

def createRecorder(liver, short_id, **args):
    if liver in recorders:
        return recorders[liver](short_id, **args)
    else:
        return None
