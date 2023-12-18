
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from reporter import *
import json
from PyQt6.QtSql import QSqlQuery
import configparser
from PyQt6.QtWidgets import QMessageBox


import logging.config
import logging
logging.config.fileConfig('./config/logging.ini')
logger = logging.getLogger('worker')

# 以进程的方式生成报告
class WorkerThread(QThread):
    signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)
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
        logger.info('\n running ---1')
        self.adf = pd.read_excel(self.info_file, dtype=str)
        self.bdf = pd.read_excel(self.value_file)
        if not self.get_ABtable_headers() :
            return
        # 从两个excel里提取A表、B表的信息
        sample_list_AB_table_path  = self.get_sub_xlsx(self.reports_result)
        # logger.info('will run generate ')
        content = '已完成报告：\n'
        logger.info(sample_list_AB_table_path)
        for sample_path in sample_list_AB_table_path:
            logger.info(sample_path)
            results = run_rpt(sample_path[1],sample_path[0], self.reports_result)
            self.insert_tb(results)
            content += sample_path[2]+'\n'
            self.signal.emit(content)


# 将两个excel表格的内容，每个样本分别提取出来作为一个excel表格，
    def get_sub_xlsx(self,result_out_dir):
        a_sample_lst = []
        b_sample_lst = []
        # 将A表内容每个样品分别保存为json
        for i in range(len(self.adf)):
            sample_code = self.adf.iloc[i, :].loc['sample_code']
            a_sample_lst.append(sample_code)
            outdir = os.path.join(result_out_dir, sample_code)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            a_outf_file = os.path.join(outdir, sample_code + '_Atable.json')
            df_dct = self.adf.loc[i].to_dict()
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
        for i in range(len(self.bdf)):
            sample_code = self.bdf.loc[i, :].loc[u'实验号']
            b_sample_lst.append(sample_code)
            # logger.info(sample_code)
            outdir = os.path.join(result_out_dir, sample_code)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            b_outf_file = os.path.join(outdir, sample_code + '_Btable.xlsx')
            self.bdf.loc[i:i, :].to_excel(b_outf_file, index=False)
        both2table_sampel = set(a_sample_lst) & set(b_sample_lst)
        # logger.info('both2table_sampel')
        logger.info(both2table_sampel)

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
        # logger.info('risk,predict_pls')
        logger.info(str(risk))
        logger.info(str(predict_pls))
        # 查询某个样本是否已经存在数据库，如果存在就更新它的信息，否则新增样本
        self.query.exec(f"select 1 from patient_info where sample_code='{sample_code}'; ")
        logger.info(str(sample_code))
        logger.info(type(results))

        ok1 = self.query.exec(f"insert into patient_info (sample_code,name,gender_desc,birthday,sampling_time,risk,predict_pls) "
                             f" values('{sample_code}','{name}','{gender_desc}','{birthday}','{sampling_time}','{risk}','{predict_pls}')")
        # ok1 = self.query.exec(
        #     f"update patient_info set name='{name}',gender_desc='{gender_desc}',birthday='{birthday}',sampling_time='{sampling_time}',risk='{risk}',predict_pls='{predict_pls}' "
        #     f" where sample_code='{sample_code}' ;")
        # 不在判断是否已经存在，只要单击就生成新的报告
        # if self.query.next():
        #     ok1 = self.query.exec(f"update patient_info set name='{name}',gender_desc='{gender_desc}',birthday='{birthday}',sampling_time='{sampling_time}',risk='{risk}',predict_pls='{predict_pls}' "
        #                     f" where sample_code='{sample_code}' ;")
        # else:
        #     ok1 = self.query.exec(f"insert into patient_info (sample_code,name,gender_desc,birthday,sampling_time,risk,predict_pls) "
        #                      f" values('{sample_code}','{name}','{gender_desc}','{birthday}','{sampling_time}','{risk}','{predict_pls}')")
        if not ok1:
            logger.info('Error : ',self.query.lastError().text() )
        logger.info(self.query.result())
        logger.info(self.query.lastError().text())

    # 判断两个表格的表头是否正确：
    def get_ABtable_headers(self):
        config = configparser.ConfigParser()
        config.read(u'./config/headers.ini', encoding='utf-8')
        aheader = config['Atable']['headers']
        bheader = config['Btable']['headers']
        if not ( list(self.adf.columns) == aheader.split('|') and list(self.bdf.columns) == bheader.split('|') ) :
            logger.info(list(self.adf.columns) == aheader.split('|'))
            logger.info(list(self.bdf.columns) == bheader.split('|'))
            content = ("<font color=red size=2><b>A  表 或者 B 表不对！ 请重新选择两个表!</b></font>")
            # content =  'A表或者B表的表头不对！请重新选择两个表 '
            logger.info('A  表 或者 B 表不对！ 请重新选择两个表 ')
            # self.signal.emmit(content)
            self.signal.emit(content)
            self.info_signal.emit(content)
            return False
        return True



