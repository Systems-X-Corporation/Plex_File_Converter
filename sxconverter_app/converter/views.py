from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import pandas as pd
from datetime import datetime
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

import logging

logger = logging.getLogger(__name__)

class MainView(LoginRequiredMixin, TemplateView):
        template_name = 'converter/upload_file.html'
    
        def get(self, request):
            form = UploadFileForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = UploadFileForm(request.POST, request.FILES)
            logger.debug(f"CSRF token in cookie: {request.COOKIES.get('csrftoken')}")
            logger.debug(f"CSRF token in POST: {request.POST.get('csrfmiddlewaretoken')}")
            if form.is_valid():
                file_type = request.POST.get('fileType')
                file_content = request.FILES['file'].read().decode('utf-8')
                success, file_content = process_file(file_content, file_type)
                
                if success:
                    current_time = datetime.now()
                    formatted_time = current_time.strftime('%d%I%M.%m%y')
                    if file_type == 'TXT BOM':
                        file_name = f'BM{formatted_time}.txt'
                    elif file_type == 'TXT FINISHED GOODS':
                        file_name = f'FG{formatted_time}.txt'
                    elif file_type == 'TXT RAW MATERIALS':
                        file_name = f'RM{formatted_time}.txt'
                    response = HttpResponse(file_content, content_type='text/plain')
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    return response
                else:
                    return HttpResponse(f"An error occurred while processing the file: {file_content}")
            else:
                return HttpResponse(f"Invalid form data: {form.errors}")


def process_file(file_content, file_type):
    if file_type == 'TXT BOM':
        try:
            dataset = pd.read_csv(StringIO(file_content))
            dataset['Finished Good Part Number or Sub-Assy part'] = dataset['Finished Good Part Number or Sub-Assy part'].str.pad(width=30, side='left', fillchar='0')
            dataset['Component Part Number'] = dataset['Component Part Number'].str.pad(width=30, side='left', fillchar='0')
            dataset['Quantity'] = dataset['Quantity'].astype(str).str.pad(width=17, side='right', fillchar='0')
            dataset['Unit of Measure'] = dataset['Unit of Measure'].str.pad(width=3, side='left', fillchar='0')
            dataset['Component Classification'] = dataset['Component Classification'].fillna(' ' * 20)

            output = StringIO()
            dataset.to_csv(output, index=False, sep='\t', header=False)
            output.seek(0)
            return True, output.getvalue()
        
        except Exception as e:
            return False, str(e)

    if file_type == 'TXT FINISHED GOODS':
        try:
            dataset = pd.read_csv(StringIO(file_content))
            dataset['Part Number'] = dataset['Part Number'].astype(str).str.pad(width=30, side='left', fillchar='0')
            dataset['Description'] = dataset['Description'].str.pad(width=60, side='left', fillchar='0')
            dataset['Unit Weight Lb.'] = dataset['Unit Weight Lb.'].str.pad(width=17, side='left', fillchar='0')
            dataset['Dutiable Value (USD)'] = dataset['Dutiable Value (USD)'].astype(str).str.pad(width=17, side='right', fillchar='0')
            dataset['Filler'] = dataset['Filler'].fillna(' ' * 17)
            dataset['Added Value (USD)'] = dataset['Added Value (USD)'].astype(str).str.pad(width=17, side='right', fillchar='0')
            dataset['Unit of Measure'] = dataset['Unit of Measure'].str.pad(width=3, side='left', fillchar='0')
            dataset['Country of Origin'] = dataset['Country of Origin'].str.pad(width=2, side='left', fillchar='0')
            dataset['USA Importation HTS Code'] = dataset['USA Importation HTS Code'].astype(str).str.pad(width=12, side='right', fillchar='0')
            dataset['USA Exportation HTS Code'] = dataset['USA Exportation HTS Code'].astype(str).str.pad(width=12, side='right', fillchar='0')

            output = StringIO()
            dataset.to_csv(output, index=False, sep='\t', header=False)
            output.seek(0)
            return True, output.getvalue()
        
        except Exception as e:
            return False, str(e)


    if file_type == 'TXT RAW MATERIALS':
        try:
            dataset = pd.read_csv(StringIO(file_content))
            dataset['Part Number'] = dataset['Part Number'].astype(str).str.pad(width=30, side='left', fillchar='0')
            dataset['Description'] = dataset['Description'].str.pad(width=60, side='left', fillchar='0')
            dataset['Unit Weight Lb.'] = dataset['Unit Weight Lb.'].str.pad(width=17, side='left', fillchar='0')
            dataset['Unit Cost (USD)'] = dataset['Unit Cost (USD)'].astype(str).str.pad(width=17, side='right', fillchar='0')
            dataset['Unit of Measure'] = dataset['Unit of Measure'].str.pad(width=3, side='left', fillchar='0')
            dataset['Country of Origin'] = dataset['Country of Origin'].str.pad(width=2, side='left', fillchar='0')
            dataset['Importation HTS Code'] = dataset['Importation HTS Code'].astype(str).str.pad(width=12, side='right', fillchar='0')
            dataset['Exportation HTS Code'] = dataset['Exportation HTS Code'].astype(str).str.pad(width=12, side='right', fillchar='0')
            dataset['ECCN'] = dataset['ECCN'].fillna(' ' * 10)
            dataset['Filler'] = dataset['Filler'].fillna(' ' * 20)
            dataset['License Number (LCN)'] = dataset['License Number (LCN)'].fillna(' ' * 20)
            dataset['License Exception'] = dataset['License Exception'].fillna(' ' * 20)
            dataset['License Expiration date'] = dataset['License Expiration date'].fillna(' ' * 8)
            dataset['USML (ITAR)'] = dataset['USML (ITAR)'].fillna(' ' * 20)


            output = StringIO()
            dataset.to_csv(output, index=False, sep='\t', header=False)
            output.seek(0)
            return True, output.getvalue()
        
        except Exception as e:
            return False, str(e)

