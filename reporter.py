import pandas as pd
import json
import matplotlib.pyplot as plt
import argparse
import os
import time

 
import NJS_APpt as njs


ARGS = argparse.ArgumentParser(description="遗传解读与报告")

ARGS.add_argument(
	 '--data', dest='data', required=True, help='尿结石表格数据集合,excel格式')
ARGS.add_argument(
	'-s', '--sample-info', dest='sample_info', required=True, help='样本json文件')
ARGS.add_argument(
	'-o', '--out_dir', dest='out_dir', default='./workdir', help='工作目录，默认：当前目录。')

def run_rpt(data_fi,sample_fi,outdir):
    df_data = pd.read_excel(data_fi)
    sample_info = json.load(open(sample_fi,'r',encoding='utf-8'))

    sample_code = sample_info['info']['bar_code_no']
    outdir = f'{outdir}/{sample_code}'
    
    results = {}
    ## 样本信息
    results.update(sample_info)
    
    ## 抓取数据
    results['data1_results'] = njs.pp.get_data1_results(df_data,sample_info['info']['test_time'])
    results['data2_results'] = njs.pp.get_data2_results(df_data)
    
    ## 风险预测
    risk_info = njs.model.predict_risk(data_fi,outdir)
    results['predict_risk'] = risk_info[sample_code]
    
    ## 画图
    risk_score = risk_info[sample_code]['predict_pls']
    g = njs.pl.risk_scatter(risk_score)
    plt.savefig(f'{outdir}/{sample_code}.risk_scatter.png',bbox_inches='tight')
    plt.close()
    results['predict_risk']['fig'] = f'{outdir}/{sample_code}.risk_scatter.png'
    print('results')
    print(results)
    ## 生成报告
    njs.report.todocx(results,outdir)
    return results


def main():
    args = ARGS.parse_args()
    if not args.data and args.sample_info:
        print('Use --help for command line help')
        return
    try:
        os.makedirs(args.out_dir)
    except:
        print ('%s exists' %(args.out_dir))

    run_rpt(args.data,args.sample_info,args.out_dir)

if __name__ == '__main__':
	start = time.time()
	main()
	end = time.time()
	print ("时间总计%s"%(end - start))
