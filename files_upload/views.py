# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.files.storage import default_storage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# Imaginary function to handle an uploaded file.
#from .handle_file_upload import handle_uploaded_file
from .forms import UploadFileForm 
from .models import files_model

'''please uncomment the line below after implementing the login'''
#@login_required
def upload_file(request):
    user=request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    #only allows files only in pdf format
        if form.is_valid():
            title=request.POST['title']
            check=files_model.objects.filter(title=title)#uncomment this after implementing login,user=user)
            if check:
                error='please select another title for your file,it has already been used'
            else:
                doc=files_model(title=title,attachment=request.FILES['content'])#uncomment this after implementing login (user=user)
                doc.save()
                #files will be uploaded inside media folder(MEDIA_ROOT)
                message='your upload has been successful,please select a file to upload again'
    else:
        form = UploadFileForm()
        message='select a file to upload'
    return render_to_response('upload.html', locals(), context_instance=RequestContext(request))


