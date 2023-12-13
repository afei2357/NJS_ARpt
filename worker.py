
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from reporter import *
import time,json
import pandas
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

# 以进程的方式生成报告
class WorkerThread(QThread):
    signal = pyqtSignal(str)
    # signal = pyqtSignal()
    def __init__(self,info_file,value_file,reports_result,db):
        super(WorkerThread,self).__init__()
        self.info_file = info_file
        self.value_file = value_file
        self.reports_result = reports_result
        self.db = db
        basename = os.path.basename(self.info_file)
        self.js_file = os.path.join(reports_result,f'{basename}.json')

    def run(self):
        print('\n running ---1')
        # 从两个excel里提取A表、B表的信息
        sample_list_AB_table_path  = self.get_sub_xlsx(self.info_file,self.value_file,self.reports_result)
        # print('will run generate ')
        content = '已完成报告：\n'
        print(sample_list_AB_table_path)
        for sample_path in sample_list_AB_table_path:
            print(sample_path)
            results = run_rpt(sample_path[1],sample_path[0], self.reports_result)
            self.insert_tb(results)
            content += sample_path[2]+'\n'
            self.signal.emit(content)


# 将两个excel表格的内容，每个样本分别提取出来作为一个excel表格，
    def get_sub_xlsx(self,Axlsx, Bxlsx, result_out_dir):
        adf = pd.read_excel(Axlsx, dtype=str)
        bdf = pd.read_excel(Bxlsx)
        a_sample_lst = []
        b_sample_lst = []
        # 将A表内容每个样品分别保存为json
        for i in range(len(adf)):
            sample_code = adf.iloc[i, :].loc['sample_code']
            a_sample_lst.append(sample_code)
            outdir = os.path.join(result_out_dir, sample_code)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            a_outf_file = os.path.join(outdir, sample_code + '_Atable.json')
            df_dct = adf.loc[i].to_dict()
            js_dct = {}
            info_dct = {}
            for k, v in df_dct.items():
                if k != 'sample_code':
                    info_dct[k] = str(v)
                else:
                    js_dct[k] = str(v)
            js_dct['info'] = info_dct
            with open(a_outf_file, 'w', encoding='utf-8') as out:
                json.dump(js_dct, out, indent=2, ensure_ascii=False)
        # 将B表内容分别保存为xlsx:
        for i in range(len(bdf)):
            sample_code = bdf.loc[i, :].loc[u'实验号']
            b_sample_lst.append(sample_code)
            # print(sample_code)
            outdir = os.path.join(result_out_dir, sample_code)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            b_outf_file = os.path.join(outdir, sample_code + '_Btable.xlsx')
            bdf.loc[i:i, :].to_excel(b_outf_file, index=False)
        both2table_sampel = set(a_sample_lst) & set(b_sample_lst)
        print('both2table_sampel')
        print(both2table_sampel)

        return zip([os.path.join(result_out_dir, sample_code, sample_code + '_Atable.json') for sample_code in both2table_sampel],
                   [os.path.join(result_out_dir, sample_code, sample_code + '_Btable.xlsx') for sample_code in both2table_sampel],
                   both2table_sampel )

    # 将报告结果更新或者插入数据库
    def insert_tb(self,results):
        # 声明数据库查询对象
        self.query = QSqlQuery(self.db)

        sample_code = results.get('sample_code')
        name = results['info'].get('name')
        gender_desc = results['info'].get('gender_desc')
        birthday = results['info'].get('birthday')
        sampling_time = results['info'].get('sampling_time')
        risk = results['predict_risk'].get('risk')
        predict_pls = results['predict_risk'].get('predict_pls')
        print('risk,predict_pls')
        print(risk,predict_pls)
        # 查询某个样本是否已经存在数据库，如果存在就更新它的信息，否则新增样本
        self.query.exec(f"select 1 from patient_info where sample_code='{sample_code}'; ")
        if self.query.next():
            ok = self.query.exec(f"update patient_info set name='{name}',gender_desc='{gender_desc}',birthday='{birthday}',sampling_time='{sampling_time}',risk='{risk}',predict_pls='{predict_pls}' "
                            f" where sample_code='{sample_code}' ;")
        else:
            ok = self.query.exec(f"insert into patient_info (sample_code,name,gender_desc,birthday,sampling_time,risk,predict_pls) "
                             f" values('{sample_code}','{name}','{gender_desc}','{birthday}','{sampling_time}','{risk}','{predict_pls}')")
        if not ok:
            print('Error : ',self.query.lastError() .text() )
        # print('self.query.result()')
        # print(self.query.result())
        # print(ok )
        # print('self.query.lastError().text()')
        # print(self.query.lastError().text())
        # # self.db.close()
        # print('finish insert ')

