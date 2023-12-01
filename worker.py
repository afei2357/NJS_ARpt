from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from reporter import *
import time

class WorkerThread(QThread):
    signal = pyqtSignal()
    def __init__(self,xlxs_file,js_file,reports_result):
        super(WorkerThread,self).__init__()
        self.xlxs_file = xlxs_file
        self.js_file = js_file
        self.reports_result = reports_result

    def run(self):
        print('running ---1')
        run_rpt(self.xlxs_file, self.js_file, self.reports_result)
        # time.sleep(2)
        print('running ---2')
