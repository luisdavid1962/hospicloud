# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from laboratory.views import (ExamenDetailView, ExamenCreateView,
    ExamenUpdateView, ImagenCreateView, AdjuntoCreateView,
    ExamenPersonaListView, ExamenIndexView, PersonaExamenCreateView,
    ExamenPreCreateView, DicomDetailView, DicomCreateView)

urlpatterns = patterns('',
    
    url(r'^$',
        ExamenIndexView.as_view(),
        name='examen-index'),
    
    url(r'^nuevo$',
        ExamenPreCreateView.as_view(),
        name='examen-nuevo'),
    
    url(r'^/persona/nuevo$',
        PersonaExamenCreateView.as_view(),
        name='examen-persona-nuevo'),
    
    url(r'^(?P<pk>\d+)$',
        ExamenDetailView.as_view(),
        name='examen-view-id'),
    
    url(r'^(?P<pk>\d+)/lista$',
        ExamenPersonaListView.as_view(),
        name='examen-persona-lista'),
    
    url(r'^(?P<persona>\d+)/agregar$',
        ExamenCreateView.as_view(),
        name='examen-agregar'),
    
    url(r'^(?P<pk>\d+)/editar$',
        ExamenUpdateView.as_view(),
        name='examen-editar'),
    
    url(r'^(?P<examen>\d+)/imagen/adjuntar$',
        ImagenCreateView.as_view(),
        name='examen-adjuntar-imagen'),
    
    url(r'^(?P<examen>\d+)/archivo/adjuntar$',
        AdjuntoCreateView.as_view(),
        name='examen-adjuntar-archivo'),
    
    url(r'^(?P<examen>\d+)/dicom/adjuntar$',
        DicomCreateView.as_view(),
        name='examen-adjuntar-dicom'),
    
    url(r'^/dicom/(?P<pk>\d+)$',
        DicomDetailView.as_view(),
        name='dicom-view'),
)
