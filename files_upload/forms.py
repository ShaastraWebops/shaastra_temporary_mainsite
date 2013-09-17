from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import files_model

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100,help_text='(add a title to your file)')
    content  = forms.FileField(help_text='(please keep file size below 5MB and give only files in pdf format)')	
    def clean_content(self):
        content = self.cleaned_data['content']
        content_type = content.content_type
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content
    def clean_title(self):
        title=self.cleaned_data['title']
        check=files_model.objects.filter(title=title)#uncomment this after implementing login,user=user)
        if check:
            raise forms.ValidationError('This file name has already been used ,please choose another one')
        else:
            return title
