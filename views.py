from django.shortcuts import render
from .models import LocalThemeTree
from django.conf import settings
from .forms import LocalNotesForm
from django.views.generic import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import Http404 

# Create your views here.

def itnotes_index(request):   
    return render(request, 'itnotes/index.html')

def treetest(request):   
    print(settings.AUTH_USER_MODEL)
    return render(request, 'itnotes/tree_test.html')


def treemptt(request):   
    # return render(request, 'itnotes/tree_testmptt.html', {'themes': GlobalThemeTree.objects.all()})
    return render(request, 'itnotes/tree_testmptt.html', {'themes': LocalThemeTree.objects.all()})

def devnavbar(request):   
    print(request.user)        
    form = LocalNotesForm(request.user)
    # return render(request, 'itnotes/tree_testmptt.html', {'themes': GlobalThemeTree.objects.all()})
    return render(request, 'itnotes/dev_navbar2.html',  {'themes': LocalThemeTree.objects.all(), 'form': form} )


class LocalNotesFormView(View):
    def get(self, request):
        print(request.user)        
        form = LocalNotesForm(request.user)
        return render(request, 'itnotes/tree_notes.html', context={'form': form})
    
    def post(self, request):
        bound_form = LocalNotesForm(request.user,request.POST)
        if bound_form.is_valid():
            contextsave=bound_form.save() 
            print(contextsave)
            print(contextsave['error'])
            if(contextsave['error']):
                return render(request, 'itnotes/error_message.html', context={'context': contextsave})         
        return render(request, 'itnotes/tree_notes.html', context={'form': bound_form})

def get_content_note(request, namenotes):
    error=False    
    contentnotes=''
    try: 
        note_obj=LocalThemeTree.objects.get(name=namenotes) 
        contentnotes=note_obj.content
    except ObjectDoesNotExist:         
        error=True
    
    data  = {
    'NameNote': namenotes,
    'ContentNote': contentnotes,
    'Error': error
    }
    # data = json.dumps(context)
    # return HttpResponse(data, content_type="application/json")
    # return HttpResponse(True, content_type="application/json;  charset=utf-8")
    return JsonResponse(data, safe=False)    

def post_update_note(request, namenotes):
    
    # print('+++++++')
    # print(request.method) 
    # # print('+++++++')
    # # print(request.body)
    # # print('+++++++')
    
    if request.method == 'GET':
        raise Http404()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    notename=content['notename']
    notename_update=content['notename_update']
    notecontent=content['content']    

    if not notecontent:
        notecontent = 'Добавьте текст!'
        

    # d_form = {'name': notename_update, 'content': '123'}    
    # form = LocalNotesForm(request.user)
    error=False
    errorMsg=''
    if request.user.is_authenticated:
        try:             
            d_form = {'name': notename_update, 'content': notecontent}
            lf = LocalNotesForm(request.user, d_form)
            if(lf.is_valid()):
                note_obj=LocalThemeTree.objects.get(name=notename)                
                note_obj.name=notename_update
                note_obj.content=notecontent
                note_obj.save()                
            else:
                error=True
                for value in lf.errors.values(): 
                    errorMsg=errorMsg+str(value)                        
        except ObjectDoesNotExist:         
            error=True
            errorMsg='Объект заметки с именем {} не найден в базе!'.format(notename)
    else:
        error=True
        errorMsg='Неавторизованный пользователь не может изменять заметки!'
    
    data  = {
    'Error': error,
    'ErrorMsg': errorMsg
    }

    return JsonResponse(data, safe=False)    

def post_create_note(request, namenotes):    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    # notename=content['notename']
    notename_update=content['notename_update']
    empty_parent=content['empty_parent']
    name_parent=content['name_parent']
    
    notecontent=content['content'] 
    if not notecontent:
        notecontent = 'Добавьте текст!'
    error=False
    errorMsg=''
    if request.user.is_authenticated:
        parent_obj=None
        if not empty_parent:
            try:             
                parent_obj=LocalThemeTree.objects.get(name=name_parent)  
            except ObjectDoesNotExist:         
                error=True
                errorMsg='Объект группы заметки с именем {} не найден в базе!'.format(name_parent)
        if not error:
            d_form = {'name': notename_update, 'content': notecontent}
            bound_form = LocalNotesForm(request.user, d_form)            
            bound_form.set_parent(parent_obj)
            if(bound_form.is_valid()):                
                result=bound_form.save() 
                error = result['error'] 
                errorMsg = result['message']          
            else:
                error=True
                for value in bound_form.errors.values(): 
                    errorMsg=errorMsg+str(value)                        
    else:
        error=True
        errorMsg='Неавторизованный пользователь не может изменять заметки!'
    
    data  = {
    'Error': error,
    'ErrorMsg': errorMsg
    }

    return JsonResponse(data, safe=False)    

def post_delete_note(request, namenotes):
    
    if request.method == 'GET':
        raise Http404()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    notename=content['notename']
    error=False
    errorMsg=''

    if request.user.is_authenticated:
        try:             
            parent_obj=LocalThemeTree.objects.get(name=notename)
            parent_obj.delete()
        except ObjectDoesNotExist:         
            error=True
            errorMsg='Объект группы заметки с именем {} не найден в базе!'.format(notename)
    else:
        error=True
        errorMsg='Неавторизованный пользователь не может изменять заметки!'    
    
    data  = {
    'Error': error,
    'ErrorMsg': errorMsg
    }

    return JsonResponse(data, safe=False)    
