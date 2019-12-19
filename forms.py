from mdeditor.fields import MDTextFormField
from django import forms

from itnotes.models import LocalThemeTree
from django.shortcuts import render



class LocalNotesForm (forms.ModelForm):
    # name = forms.CharField(max_length=150)
    content = MDTextFormField()
    class Meta:
        model = LocalThemeTree
        fields = ('name', 'content')
    
    def __init__(self, user, *args, **kwargs):       
        super(LocalNotesForm, self).__init__(*args, **kwargs)
        self.user =user
        self.parent = None
        # self.fields['field1'].queryset = AnotherModel.objects.filter(pk=my_arg1)
    def set_parent(self, parent):
        self.parent = parent

    def save(self):
        result={'error': False, 'message': ''}            
        if not self.user.is_authenticated:
            result['error']= True
            result['message']= 'Не авторизованный пользователь не может создавать заметки!'
        else:
            LocalThemeTree.objects.create(
                name=self.cleaned_data['name'],
                content=self.cleaned_data['content'],
                author=self.user,
                parent=self.parent
            )
        return result
