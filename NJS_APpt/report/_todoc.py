from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm 
import datetime
import os
workdir = os.path.abspath(os.path.dirname(__file__))

def todocx(results,outdir):
    tpl = DocxTemplate(f'{workdir}/template/NJS_template.docx')
    results['predict_risk']['fig'] = InlineImage(tpl, results['predict_risk']['fig'], width=Mm(160))
    tpl.render(results)
    sample_code = results['info']['bar_code_no']
    time = datetime.datetime.now().strftime('%Y%m%d%H')
    tpl.save(f'{outdir}/{sample_code}.{time}.NJS.report.docx')
    return  f'{outdir}/{sample_code}.{time}.NJS.report.docx'
