import os.path

from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from utils.reporter import *
import json
from PyQt6.QtSql import QSqlQuery
import configparser
from PyQt6.QtWidgets import QMessageBox
import shutil

import logging.config
import logging
basedir = os.path.join( os.path.abspath(__file__) ,os.pardir,os.pardir)
# print(basedir)
config_file = os.path.join(basedir,'config/logging.ini')
logging.config.fileConfig(config_file)
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
        self.query = QSqlQuery(self.db)

        basename = os.path.basename(self.info_file)
        self.js_file = os.path.join(reports_result,f'{basename}.json')
        self.create_tb()

    def run(self):
        logger.info('\n running ---1')
        self.adf = pd.read_excel(self.info_file, dtype=str)
        self.bdf = pd.read_excel(self.value_file)
        if not self.get_ABtable_headers() :
            return
        # self.bdf.to_sql(, connection, index=False)

        # 从两个excel里提取A表、B表的信息
        sample_list_AB_table_path  = self.get_sub_xlsx(self.reports_result)

        # 保存B表的内容
        self.insert_b_tb(self.bdf)
        # logger.info('will run generate ')
        content = '已完成报告：\n'
        final_report_dir = os.path.join( self.reports_result , 'final_report_dir' )
        if not os.path.exists(final_report_dir):
            os.makedirs(final_report_dir)
        logger.info(sample_list_AB_table_path)
        #todo
        # 下面隐藏，先调试数据库
        for sample_path in sample_list_AB_table_path:
            logger.info(sample_path)
            results,report_doc = run_rpt(sample_path[1],sample_path[0], self.reports_result)
            # os.rename()
            shutil.move(report_doc,final_report_dir)
            self.insert_tb(results)
            content += sample_path[2]+'\n'
            self.signal.emit(content)



    def insert_b_tb(self, df):
        # 构建预处理语句
        cols = ['`{}`'.format(col) for col in df.columns]
        query = f"INSERT INTO data_results ({', '.join(cols)}) VALUES "

        logger.info(query)
        for _, row in df.iterrows():
            # values = ", ".join([f"'{row[col]}'" for col in df.columns])
            values = ", ".join([f"'{row[col]}'" for col in df.columns])
            full_query = query + f"({values});"
            # self.query.exec()
            logger.info(full_query)
            ok = self.query.exec(full_query)
            if not ok:
                logger.info('Error : ', self.query.lastError().text())
        logger.info('finish insert ---------------')



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
        shell = f"insert into patient_info (sample_code,name,gender_desc,birthday,sampling_time,risk,predict_pls) " \
                             f" values('{sample_code}','{name}','{gender_desc}','{birthday}','{sampling_time}','{risk}','{predict_pls}')"
        logger.info(shell)
        ok1 = self.query.exec(shell)

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
            logger.info('A  表 或者 B 表不对！ 请重新选择两个表 ')
            # self.signal.emmit(content)
            self.signal.emit(content)
            self.info_signal.emit(content)
            return False
        return True

    def create_tb(self):
        create_tb_shell = ' create table if not exists  data_results(id integer primary key AUTOINCREMENT ,  "实验号" vchar,"性别" vchar,"年龄" vchar,"pH" vchar,"肌酐" vchar,"柠檬酸" vchar,"尿素氮" vchar,"尿酸" vchar,"钠离子" vchar,"铵根离子" vchar,"钾离子" vchar,"镁离子" vchar,"钙离子" vchar,"氯离子" vchar,"磷酸根离子" vchar,"硫酸根离子" vchar,"草酸" vchar,"乳酸-2" vchar, "2-羟基异丁酸-2" vchar,"己酸-1" vchar,"乙醇酸-2" vchar,"草酸-2" vchar,"2-羟基丁酸-2" vchar,"乙醛酸-OX-2" vchar,"3-羟基丙酸-2" vchar,"丙酮酸-OX-2" vchar,"丙戊酸-1" vchar,"3-羟基丁酸-2" vchar,"3-羟基异丁酸-2" vchar,"2-羟基异戊酸-2" vchar,"2-甲基-3-羟基丁酸-2" vchar,"丙二酸-2" vchar,"3-羟基-异戊酸-2" vchar,"2-酮异戊酸-OX-2" vchar,"甲基丙二酸-2" vchar,"2-羟甲基丁酸-2" vchar,"尿素-2" vchar,"4-羟基丁酸-2" vchar,"2-羟基异己酸-2" vchar,"3-羟基戊酸-2" vchar,"乙酰乙酸" vchar,"2-羟基-3-甲基戊酸-2" vchar,"安息香酸-1" vchar,"乙酰乙酸-OX-2" vchar,"辛酸-1" vchar,"2-酮-3-甲基戊酸-OX-2" vchar,"2-甲基-3-羟基戊酸-2(1)" vchar,"甘油-3" vchar,"磷酸-3" vchar,"2-甲基-3-羟基戊酸-2 (2)" vchar,"乙基丙二酸-2" vchar,"2-酮-异己酸-0X-2" vchar,"乙酰甘氨酸-1" vchar,"苯乙酸-1" vchar,"马来酸-2" vchar,"琥珀酸-2" vchar,"甲基琥珀酸-2" vchar,"甘油酸-3" vchar,"尿嘧啶-2" vchar,"富马酸-2" vchar,"丙酰甘氨酸-1" vchar,"乙酰甘氨酸-2" vchar,"甲羟戊酸内酯-2" vchar,"甲羟戊酸内酯-1" vchar,"异丁酰甘氨酸-1" vchar,"2-丙基-3-羟基戊酸-2" vchar,"甲基富马酸-2" vchar,"戊二酸-2" vchar,"3-甲基戊烯二酸-2" vchar,"3-甲基戊二酸-2" vchar,"2-丙基-3-酮戊酸-2" vchar,"丙酰甘氨酸-2" vchar,"异丁酰甘氨酸-2" vchar,"3,4-二羟基丁酸" vchar,"丁酰甘氨酸-1" vchar,"3-甲基戊烯二酸-2(1)" vchar,"戊烯二酸-2" vchar,"琥珀酰丙酮-OX-2(1)" vchar,"癸酸-1" vchar,"2-丙基-5-羟基戊酸-2" vchar,"3-甲基戊烯二酸-2(2)" vchar,"异戊酰甘氨酸-1" vchar,"丁酰甘氨酸-2" vchar,"苹果酸-3" vchar,"己二酸-2" vchar,"异戊酰甘氨酸-2" vchar,"2-己烯酸-2" vchar,"5-羟脯氨酸-2" vchar,"3-甲基己二酸-2" vchar,"亚硫基二乙酸-2" vchar,"2-丙基-羟基戊二酸-2" vchar,"7-羟基辛酸-2" vchar,"5-羟甲基-2-糠酸-2" vchar,"巴豆酰甘氨酸-2" vchar,"3-甲基巴豆酰甘氨酸-1" vchar,"巴豆酰甘氨酸-1" vchar,"3-甲基巴豆酰甘氨酸-2" vchar,"2-羟基戊二酸-3" vchar,"3-羟基戊二酸-3" vchar,"苯乳酸-2" vchar,"庚二酸-2" vchar,"3-羟基-3-甲基戊二酸-3" vchar,"3-羟基苯乙酸-2" vchar,"2-酮戊二酸-OX-2(1)" vchar,"4-羟基安息香酸-2" vchar,"4-羟基苯乙酸-2" vchar,"2-酮戊二酸-OX-2(2)" vchar,"己酰甘氨酸-2" vchar,"苯丙酮酸-OX-2" vchar,"N-乙酰天冬氨酸-2" vchar,"2-羟基己二酸-3" vchar,"辛烯二酸-2" vchar,"3-羟基己二酸-3" vchar,"辛二酸-2" vchar,"3-甲基戊烯二酸-2(3)" vchar,"2-酮己二酸-OX-3" vchar,"乌头酸-3" vchar,"乳清酸-3" vchar,"香草酸-2" vchar,"高香草酸-2" vchar,"壬二酸-2" vchar,"马尿酸-2" vchar,"异枸橼酸-4" vchar,"枸橼酸-4" vchar,"尿黑酸-3" vchar,"马尿酸-1" vchar,"甲基枸橼酸-4(1)" vchar,"3-(3-羟苯基）-3-羟基丙酸-3" vchar,"甲基枸橼酸-4(2)" vchar,"3-羟基辛烯二酸-3" vchar,"3-羟基辛二酸-3" vchar,"香草扁桃酸-3" vchar,"癸二酸-2" vchar,"癸二烯酸-2" vchar,"4-羟基苯乳酸-3" vchar,"4-羟基苯丙酮酸-OX-2" vchar,"2-羟基马尿酸-3" vchar,"吲哚-3-乙酸-2" vchar,"辛二酰甘氨酸-2" vchar,"棕榈酸-1" vchar,"2-羟基癸二酸-3" vchar,"3-羟基癸二酸-3" vchar,"2-羟基马尿酸-2" vchar,"十二烷二酸-2" vchar,"N-乙酰酪氨酸-3" vchar,"尿酸-4" vchar,"3,6-环氧-十二烷二酸-2" vchar,"3-羟基-十二烷二酸-3" vchar,"3,6-环氧-十四烷二酸-2" vchar,"二十四烷(C24)" vchar,"托品酸" vchar,"MGA（十七烷酸）" vchar,"4-羟基环己基乙酸" vchar,"2,3-二羟基-2-甲基丁酸" vchar,"4-羟基-6-甲基-2-吡喃酮" vchar);'

        self.query.exec(create_tb_shell)


