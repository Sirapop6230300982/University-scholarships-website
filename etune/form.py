from django import forms
from .models import *
#from ckeditor.fields import RichTextField
#from ckeditor.widgets import CKEditorWidget

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Scholar_news
        fields = '__all__'

# class Contents(forms.ModelForm):
#     class Meta:
#         model = Scholar_info
#         fields = {'si_description'}