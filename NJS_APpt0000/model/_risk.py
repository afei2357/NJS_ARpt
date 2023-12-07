import subprocess
import os
import datetime
import pandas as pd
import shutil


workdir = os.path.abspath(os.path.dirname(__file__))
r_dir = workdir + '/rscript'

def predict_risk(data_fi,outdir):
    time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    outdir = outdir + f'/tmp{time}'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    rscript_path = shutil.which('Rscript')
    if rscript_path is None:
        raise RuntimeError('Rscript not found ,please make sure R is installed and avaibale in the system PATH, 请查看R是否放在环境变量里')
    print(f'"{rscript_path}" --encoding=utf-8  {r_dir}/Risk.R --newdata={data_fi} --model={r_dir}/plsmodel.rds --variables={r_dir}/varnames.rds --rawdata={r_dir}/njs1_2.rds --outdir={outdir}')
    # print(f'Rscript {r_dir}/Risk.R --newdata={data_fi} --model={r_dir}/plsmodel.rds --variables={r_dir}/varnames.rds --rawdata={r_dir}/njs1_2.rds --outdir={outdir}')

    # subprocess.call(f'"{rscript_path}" --encoding=utf-8 {r_dir}/Risk.R --newdata={data_fi} --model={r_dir}/plsmodel.rds --variables={r_dir}/varnames.rds --rawdata={r_dir}/njs1_2.rds --outdir={outdir}',shell=True)
    subprocess.call(f'"{rscript_path}" --encoding=utf-8 {r_dir}/Risk.R --newdata={data_fi} --model={r_dir}/plsmodel.rds --variables={r_dir}/varnames.rds --rawdata={r_dir}/njs1_2.rds --outdir={outdir}',shell=True)
    # subprocess.call(f'Rscript {r_dir}/Risk.R --newdata={data_fi} --model={r_dir}/plsmodel.rds --variables={r_dir}/varnames.rds --rawdata={r_dir}/njs1_2.rds --outdir={outdir}',shell=True)

    df = pd.read_csv(f'{outdir}/predict_risk.csv',index_col=0)
    risk_chn = {'medium':'中风险',
        'high':'低风险',
        'low':'高风险'}
    df['risk'] = df['risk'].apply(lambda x:risk_chn[x])

    return df.to_dict('index')
