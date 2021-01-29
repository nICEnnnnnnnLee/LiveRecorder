from .flv_checker import Flv
from .live_thread.download import DownloadThread
from .live_thread.monitoring import MonitoringThread
from . import _recorder as Recorder
import pkgutil
import inspect
import os

filepath, tmpfilename = os.path.split(inspect.getfile(Recorder))

for filefiner, name, ispkg in pkgutil.iter_modules([filepath]):
    if not ispkg and not name.startswith("_") and name.endswith("_recorder"):
        __import__(__name__ + "." + name)