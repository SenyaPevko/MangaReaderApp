from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

import traceback
import sys

from utils.decorators import catch_exception


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        @catch_exception
        def wrapped_run():
            try:
                result = self.fn(*self.args, **self.kwargs)
            except Exception as e:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)
            finally:
                self.signals.finished.emit()

        wrapped_run()


