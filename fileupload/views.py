#!/usr/bin/python
# encoding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .forms import UploadFileForm
from django.core.context_processors import csrf
from .models import Document

# Imaginary function to handle an uploaded file.

def upload_file(request):
    '''Préparation de l'upload du fichier'''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['file'])
            newdoc.save()
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/upload/list')
    else:
        form = UploadFileForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('fileupload/upload.html',c)


def handle_uploaded_file(file):
    '''Place le fichier à la destination choisie'''
    if file:
        destination = open('media/'+file.name, 'wb+')
        #destination = open('/tmp', 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()


def list(request):
    '''Liste les documents uploadés dans la page fileupload/list.html'''
    documents = Document.objects.all()

    return render_to_response(
        'fileupload/list.html',
        {'documents': documents},
    )
