import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from typing import  Optional
from matplotlib.axes import Axes
import matplotlib
matplotlib.use("Agg")

workdir = os.path.abspath(os.path.dirname(__file__))

def risk_scatter(risk_score:float,
                       ax: Optional[Axes] = None):
    df_predata = pd.read_csv(f'{workdir}/predict_data.tsv',sep='\t')

    plt.rcParams['figure.dpi'] =  120
    # plt.rcParams['font.sans-serif'] =  ['Arial Unicode MS']
    plt.rcParams['font.sans-serif']=["SimHei"]
    plt.rcParams['axes.unicode_minus']=False

    if not ax:
        plt.rcParams['figure.figsize'] =  (6,4)
        ax = plt.subplot(111)
    sns.scatterplot(y='predict',x='is_stone',data=df_predata,s=60,alpha=0.6,ax=ax)
    plt.axhline(y=0.2937039,ls='--',color='r')
    plt.axhline(y=0.6865758,ls='--',color='r')
    plt.xlabel('')
    plt.ylabel('预测值',fontsize=14)
    plt.plot(0.5,risk_score,marker='*',color='r',markersize=10)
    plt.text(0.3,risk_score+0.05,f'您的评分值 ({risk_score:.2f})')
    plt.xticks([-0.5,0,1,1.5],labels=['','阴性组','阳性组',''],fontsize=14);
    #plt.savefig(outfig,bbox_inches='tight',dpi=300)
    return ax

