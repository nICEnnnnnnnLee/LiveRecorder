# coding=utf-8
from ._base_recorder import recorders


def createRecorder(liver, short_id, **args):
    if liver in recorders:
        return recorders[liver](short_id, **args)
    else:
        return None
