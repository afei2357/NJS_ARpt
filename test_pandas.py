import  pandas as pd
import os,json

adf = pd.read_excel('input/表A.xlsx')
bdf = pd.read_excel('input/尿结石表B：数据集.xlsx')
def get_sub_xlsx(Axlsx,Bxlsx,result_out_dir):
    adf = pd.read_excel(Axlsx ,dtype=str)
    bdf = pd.read_excel(Bxlsx)
    a_sample_lst = []
    b_sample_lst = []
    #将A表内容分别保存为json
    for i in range(len(adf) ) :
        sample_code = adf.iloc[i, :].loc['sample_code']
        a_sample_lst.append(sample_code)
        outdir = os.path.join(result_out_dir,sample_code)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        a_outf_file = os.path.join(outdir,sample_code+'_Atable.json')
        df_dct = adf.loc[i].to_dict()
        js_dct = {}
        info_dct = {}
        for k ,v in df_dct.items():
            if k != 'sample_code':
                info_dct[k] = str( v )
            else:
                js_dct[k] = str( v)
        js_dct['info'] = info_dct
        with open(a_outf_file,'w',encoding='utf-8') as out:
            json.dump(js_dct,out,indent=2,ensure_ascii=False)
    #将B表内容分别保存为xlsx:
    for i in range(len(bdf) ) :
        sample_code = bdf.loc[i,:].loc[u'实验号']
        b_sample_lst.append(sample_code)
        # print(sample_code)
        outdir = os.path.join(result_out_dir,sample_code)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        b_outf_file = os.path.join(outdir,sample_code+'_Btable.xlsx')
        bdf.loc[i:i, :].to_excel(b_outf_file,index=False)
    both2table_sampel = set(a_sample_lst) & set(b_sample_lst)
    return zip( [os.path.join(result_out_dir,sample_code,sample_code+'_Atable.json') for sample_code in both2table_sampel] ,\
                [os.path.join(result_out_dir,sample_code,sample_code+'_Btable.xlsx')  for sample_code in both2table_sampel  ] )

def get_sub_xlsx1(Axlsx,Bxlsx,subdir):
    adf = pd.read_excel(Axlsx ,dtype=str)
    bdf = pd.read_excel(Bxlsx)
    for i in range(len(adf) ) :
        sample_code = adf.iloc[i, :].loc['sample_code']
        a_outf_file = os.path.join(outdir,sample_code+'_Atable.json')
        # adf.loc[i:i, :].to_excel(a_outf_file,index=False)
        sub_adf = adf.loc[i:i, :]
        df_dct = sub_adf.to_dict()
        js_dct = {}
        info_dct = {}
        for k ,v in df_dct.items():
            if k != 'sample_code':
                info_dct[k] = str( v.get(i) )
            else:
                # js_dct[k] = str( v.get(0) )
                js_dct[k] = str( v.get(i) )
                # print(v.get(i))
                # print(js_dct[k])
        js_dct['info'] = info_dct
        with open(a_outf_file,'w',encoding='utf-8') as out:
            json.dump(js_dct,out,indent=2,ensure_ascii=False)



    # df_dct = adf.to_dict()
    # js_dct = {}
    # info_dct = {}
    # for k, v in df_dct.items():
    #     for j in len(v):
    #
    #     # sample_code = adf.iloc[i, :].loc['sample_code']
    #     outdir = os.path.join(subdir, sample_code)
    #     a_outf_file = os.path.join(outdir, sample_code + '_Atable.json')
    #
    #     if not os.path.exists(outdir):
    #         os.makedirs(outdir)
    #
    #     if k != 'sample_code':
    #         info_dct[k] = str(v.get(0))
    #     else:
    #         js_dct[k] = str(v.get(0))
    # js_dct['info'] = info_dct

    # with open(self.js_file, 'w', encoding='utf-8') as out:
    #     json.dump(js_dct, out, indent=2, ensure_ascii=False)


    # with open(subdir+'/outdct.json','w',encoding='utf-8') as fh:
    #     json.dump(df_dct,fh,indent=2,ensure_ascii=False)
'''
    for i in range(len(bdf) ) :
        sample_code = bdf.loc[i,:].loc[u'实验号']
        # print(sample_code)
        outdir = os.path.join(subdir,sample_code)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        b_outf_file = os.path.join(outdir,sample_code+'_Btable.xlsx')
        bdf.loc[i:i, :].to_excel(b_outf_file,index=False)
'''


if __name__ == '__main__':
    Axlsx = 'input/表A.xlsx'
    Bxlsx = 'input/尿结石表B：数据集.xlsx'
    outdir = 'input/testout'
    result = get_sub_xlsx(Axlsx,Bxlsx,outdir)
    # print(result)
    for j in result:
        print(j[0])