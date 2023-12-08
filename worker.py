from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
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

    def set_tb(self):
        print('*** step2 SetTableView')
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()

        # 声明查询模型
        # self.queryModel = QSqlQueryModel(self)

        # 添加数据库
        # 设置数据库名称
        # 判断是否打开
        if not self.db.open():
            return False

        # 声明数据库查询对象
        self.query = QSqlQuery()
        self.query.exec('select * from student ')
        self.db.close()


    def run(self):
        print('running ---1')
        df = pandas.read_excel(self.info_file,dtype=str)
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
        self.results = run_rpt(self.value_file, self.js_file, self.reports_result)
        time.sleep(2)
        print('running ---2')
        print(self.results)
        # with open('result2.json','w',encoding='utf-8') as out:
        #     json.dump(self.results,out,indent=4,ensure_ascii=False)
        print('will insert ')

        self.insert_tb()

    def insert_tb(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db/database.db')
        # 打开数据库
        self.db.open()
        # 判断是否打开
        if not self.db.open():
            return False
        # 声明数据库查询对象
        self.query = QSqlQuery()

        sample_code = self.results.get('sample_code')
        name = self.results['info'].get('name')
        gender_desc = self.results['info'].get('gender_desc')
        birthday = self.results['info'].get('birthday')
        sampling_time = self.results['info'].get('sampling_time')
        risk = self.results['predict_risk'].get('risk')
        predict_pls = self.results['predict_risk'].get('predict_pls')
        print('risk,predict_pls')
        print(risk,predict_pls)
        self.query.exec(f"insert into patient_info (sample_code,name,gender_desc,birthday,sampling_time,risk,predict_pls)  values('{sample_code}','{name}','{gender_desc}','{birthday}','{sampling_time}','{risk}','{predict_pls}')")
        print('self.query.result()')
        print(self.query.result())
        self.db.close()
        print('finish insert ')
    # query.exec("insert into student values(1,'张三1','男',20,'计算机')")


    def ceate_table(self):
        self.query.exec("create table patient_info(id int primary key AUTOINCREMENT,"
                        " sample_code vchar,"
                        "name vchar, "
                        "gender_desc vchar, "
                        "birthday vchar, "
                        "sample_date vchar,"
                        "risk vchar,"
                        "predict_pls vchar)")