from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from reporter import *
import time,json
import pandas

class WorkerThread(QThread):
    signal = pyqtSignal()
    def __init__(self,info_file,value_file,reports_result):
        super(WorkerThread,self).__init__()
        self.info_file = info_file
        self.value_file = value_file
        self.reports_result = reports_result
        basename = os.path.basename(self.info_file)
        self.js_file = os.path.join(reports_result,f'{basename}.json')

    def run(self):
        print('running ---1')
        df = pandas.read_excel(self.info_file)
        df_dct = df.to_dict()
        js_dct = {}
        info_dct = {}
        for k ,v in df_dct.items():
            if k != 'sample_code':
                info_dct[k] = str( v.get(0) )
            else:
                js_dct[k] = str( v.get(0) )
        js_dct['info'] = info_dct
        print(js_dct)
        print('self.info_file, self.js_file,self.value_file, self.reports_result')
        print(self.info_file)
        print(self.js_file)
        print(self.value_file)
        print(self.reports_result)
        with open(self.js_file,'w',encoding='utf-8') as out:
            json.dump(js_dct,out,indent=2,ensure_ascii=False)
        print('will run generate ')
        run_rpt(self.value_file, self.js_file, self.reports_result)

        time.sleep(2)
        print('running ---2')
