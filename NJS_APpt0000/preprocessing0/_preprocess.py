import pandas as pd
import numpy as np

data1_range_dict= {'柠檬酸/肌酐': '0.09-0.31',
 '尿素氮/肌酐': '8.51-13.38',
 '尿酸/肌酐': '0.18-0.40',
 '钠离子/肌酐': '1.42-3.06',
 '铵根离子/肌酐': '0.26-0.44',
 '钾离子/肌酐': '0.66-1.16',
 '镁离子/肌酐': '0.04-0.08',
 '钙离子/肌酐': '0.03-0.10',
 '氯离子/肌酐': '0.69-3.93',
 '磷酸根离子/肌酐': '0.69-1.87',
 '硫酸根离子/肌酐': '0.39-1.33',
 '草酸/肌酐': '0.01-0.03',
 'pH': '5.44-6.18'}

def get_isrange(val,range_info):
    min_val,max_val = range_info.split('-')
    if float(val) < float(min_val):
        return 'below'
    elif float(val) > float(max_val):
        return 'above'
    else:
        return 'in'
    
def get_data1_results(df_data_reulsts,test_time):
    data1_results = []
    for idx,range_info in data1_range_dict.items():
        if idx.endswith('肌酐'):
            val = (df_data_reulsts[idx.split('/')[0]]/df_data_reulsts['肌酐']).squeeze()
        else:
            val = df_data_reulsts[idx].squeeze()
        
        if idx == '柠檬酸/肌酐':
            note = '柠檬酸上升有利于抑制结石'
        elif idx == '镁离子/肌酐':
            note = '镁上升有利于抑制结石'
        else:
            note = ''
        
        is_range = get_isrange(val,range_info)
        data1_results.append({'name':idx,
                              'test_time':test_time,
                              'value':f'{val:.3f}',
                              'is_range':is_range,
                               'range_info':range_info,
                               'note':note
                                 }) 
    return data1_results


def get_predict_risk(risk_file,sample_code):
    risk_chn = {'medium':'中风险',
           'high':'低风险',
           'low':'高风险'}
    
    df_risk = pd.read_csv(risk_file,index_col=0)
    risk_info = df_risk.loc[sample_code].to_dict()
    risk_info['predict_pls'] = f'{risk_info["predict_pls"]:.2f}'
    risk_info['risk'] = risk_chn[risk_info['risk']]
    return risk_info

def get_data2_results(df_data_reulsts):
    data2_results = []
    num = 0
    for i in np.array(df_data_reulsts.iloc[:,17:-6]).reshape(33,4):
        tmp = {}
        num_2nd = 0
        for j in i:
            num +=1
            num_2nd +=1
            tmp.setdefault(f'p{num_2nd}',{'num':f'OA{str(num).zfill(3)}','val':j})
        num_2nd = 0
        data2_results.append(tmp)
    return data2_results

