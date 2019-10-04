from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from jira.client import JIRA
from polls.forms import *


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form1 = HomeForm()
        form2 = HomeForm2()
        form3 = HomeForm3()
        form4 = HomeForm4()
        form5 = HomeForm5()
        form6 = HomeForm6()
        form7 = HomeForm7()
        form8 = HomeForm8()
        form9 = HomeForm9()
        form10 = HomeForm10()
        return render(request, self.template_name, {'form_1': form1,'form_2': form2,'form_3': form3,
        'form_4': form4,'form_5': form5,'form_6': form6,'form_7': form7,'form_8': form8, 'form_9': form9
        , 'form_10': form10})


    def post(self, request):
        form1 = HomeForm(request.POST)
        form2 = HomeForm2(request.POST)
        form3 = HomeForm3(request.POST)
        form4 = HomeForm4(request.POST)
        form5 = HomeForm5(request.POST)
        form6 = HomeForm6(request.POST)
        form7 = HomeForm7(request.POST)
        form8 = HomeForm8(request.POST)
        form9 = HomeForm9(request.POST)
        form10 = HomeForm10(request.POST)
        if (request.method == "POST" and form1.is_valid() and form2.is_valid() and form3.is_valid() and 
        form4.is_valid() and form5.is_valid() and form6.is_valid() and form7.is_valid() and form8.is_valid()
        and form9.is_valid() and form10.is_valid()):
            text = form1.cleaned_data['Answer_1']
            text2 = form2.cleaned_data['Answer_2']
            text3 = form3.cleaned_data['Answer_3']
            text4 = form4.cleaned_data['Answer_4']
            text5 = form5.cleaned_data['Answer_5']
            text6 = form6.cleaned_data['Answer_6']
            text7 = form7.cleaned_data['Answer_7']
            text8 = form8.cleaned_data['Answer_8']
            text9 = form9.cleaned_data['Answer_9']
            text10 = form10.cleaned_data['Answer_10']
			
        args = {'form_1': form1, 'text': text, 'form_2': form2, 'text2': text2, 'form_3': form3, 
        'text3': text3, 'form_4': form4, 'text4': text4, 'form_5': form5, 'text5': text5, 'form_6': form6,
        'text6': text6, 'form_7': form7, 'text7': text7, 'form_8': form8, 'text8': text8, 'form_9': form9, 
        'text9': text9, 'form_10': form10, 'text10': text10}
        #return render(request, self.template_name, args)
        api_token = "API_TOKEN_EXAMPLE"
        username = "example@pilottravelcenters.com"
        jira = JIRA(options={'server': 'https://pilotflyingj.atlassian.net'},
            basic_auth=(username, api_token))
        description_text = ('1) Who is the primary software requestor? = '+text+'\n'
            '2) What is full intended userbase? = '+text2+'\n'
            '3) What is the business use case? = '+text3+'\n'
            '4) Who is the Department Director that will be accpting the risks/terms laid out by legal? Are they aware of the request? = '+text4+'\n'
            '5) What Strategic Pillar or Strategic Project will this software support? = '+text5+'\n'
            '6) Please provide copy of the EULA (license information). = '+text6+'\n'
            '7) How will access and distribution of the sofware be controlled? = '+text7+'\n'
            '8) Who will control licenses, if applicable? = '+text8+'\n'
            '9) Is this software pre-existing in our environment? = '+text9+'\n')
        new_issue = jira.create_issue(project='ITSEC', summary='SoftwareRequest: '+text10, labels=['AppSec'], 
            description=description_text, issuetype={'name': 'Task'}, customfield_10042=text, assignee={'name': 'AppSec'})
        return redirect('Success.html')

