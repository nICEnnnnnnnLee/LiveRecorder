import pkgutil
import sys
module = sys.modules[__name__]

for filefiner, name, ispkg in pkgutil.iter_modules(["you_live."], ""):
    if not ispkg and not name.startswith("_") and name.endswith("_recorder"):
        __import__(__name__ + "." + name)
        try:
            for attr in dir(getattr(module, name)):
                if attr.endswith("Recorder") and not 'BaseRecorder' == attr:
                    importCmd = "from .%s import %s"%(name, attr)
                    #print(importCmd)
                    exec(importCmd)
        except:
            break

from .flv_checker import Flv
from .live_thread.download import DownloadThread
from .live_thread.monitoring import MonitoringThread
from . import _recorder as Recorder
