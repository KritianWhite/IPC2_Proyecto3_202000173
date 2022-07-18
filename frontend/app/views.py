from email.policy import HTTP
import string
from urllib import response
from xmlrpc.client import ResponseError
from django.shortcuts import render
from matplotlib.style import context

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template, render_to_string

import os
import pdfkit as pdf


from app.forms import FileForm, DateForm, DateForm2
from frontend.settings import PDF_FILES_FOLDER
from django.http import FileResponse
# Create your views here.




endpoint = 'http://127.0.0.1:4000/'
def pdf_view(request):
    pdf = open(PDF_FILES_FOLDER + "ManualTecnico.pdf", 'rb')
    return FileResponse(pdf)


def index(request):
    return render(request, 'index.html')


def CargaMasiva(request):
    ctx = {
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'CargaMasiva', data=xml_binary)
            print(response.status_code, response.json())
            if response.ok:
                ctx['response'] = "El archivo fue procesado correctamente"
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
    else:
        print("Estoy renderizando unicamente la plantilla", request.method)
        return render(request, 'carga.html')
    return render(request, 'carga.html', ctx)

def peticiones(request):
    return render(request, 'peticiones.html')

def consultar(request):
    if request.method == 'GET':
        response = requests.get(endpoint+"consultar")
        response = response.json()
        return render(request, 'consultar.html', response)

def clasicacionPor_Fecha(request):
    if request.method == 'GET':
        context = requests.get(endpoint+'clasificar-por-fecha')
        context = context.json()
        return render(request, 'Clasificacion por fecha.html', context)
    if request.method == 'POST':
        formulario = DateForm(request.POST)
        json = {
            'date': formulario['date'].value(),
            'empresa':formulario['empresa'].value()
        }
        context = requests.post(endpoint+'clasificar-por-fecha', json=json)
        context = context.json()
        return render(request, 'Clasificacion por fecha.html', context)
    
def resumenPor_Rango(request):
    if request.method == 'GET':
        contexto = requests.get(endpoint+'resumen-por-rango')
        contexto = contexto.json()
        return render(request, 'clasificacion por rango.html', contexto)
    if request.method == 'POST':
        form = DateForm2(request.POST)
        json = {
            'date1':form['date1'].value(),
            'date2':form['date2'].value(),
            'empresa':form['empresa'].value()
        }
        context = requests.post(endpoint+'resumen-por-rango', json=json)
        context = context.json()
        print(context)
        return render(request, 'clasificacion por rango.html', context)
        
def reportes(request):
    return render(request, 'reportes.html')

def reporte2(request):
    pdf.from_url('http://127.0.0.1:8000/clasificar-por-fecha/', 'Reporte2.pdf')
    return render(request, 'reportes.html')



def ayuda(request):
    if request.method == 'GET':
        return render(request, 'ayuda.html')

def reset(request):

    try:
        response = requests.delete(endpoint+'reset')
        print(response.json())
    except:
        print('API no levantada D:')
    return render(request, 'carga.html')