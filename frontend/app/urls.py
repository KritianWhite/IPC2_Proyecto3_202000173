from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('carga/', views.CargaMasiva, name='carga'),
    path('peticiones/', views.peticiones, name='peticiones'),
    path('consultar/', views.consultar, name='consultar'),
    path('clasificar-por-fecha/', views.clasicacionPor_Fecha, name='clasificar-por-fecha'),
    path('resumen-por-rango/', views.resumenPor_Rango, name='resumen-por-rango'),
    path('reportes/', views.reportes, name='reportes'),
    path('reporte2/', views.reporte2, name='reporte2'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('documentacion/', views.pdf_view),
    path('reset/', view=views.reset, name='reset'),
]
