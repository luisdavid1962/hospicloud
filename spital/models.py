# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django_extensions.db.fields import UUIDField
from library import code128, image_to_content, pyqrcode
from persona.models import Persona
from sorl.thumbnail import ImageField #@UnresolvedImport

class Admision(models.Model):
    
    """Permite registrar el Ingreso y estadia de una :class:`Persona` en el
    Hospital.
    """
    
    ESTADOS = (
        ('A', 'Admitido'),
        ('B', 'Autorizado'),
        ('H', 'Hospitalizar'),
        ('I', 'Ingresado'),
        ('C', 'Alta'),
    )
    
    ARANCELES = (
               ('C', u"CEMESA"),
               ('E', u"Empleado"),
               ('M', u"Mediprocesos"),
               ('J', u"Ejecutivo"),
               ('X', u"Extranjero"),
    )
    
    PAGOS = (
             ('EF', u"Efectivo"),
             ('CK', u"Cheque"),
             ('CO', u"Empresa"),
             ("OC", u"Orden de Compra"),
             ('TC', u"Tarjeta Crédito"),
             ('TB', u"Transferencia Bancaria"),
    )
    
    ASEGURADORA = (
             ("PA","Particular"),
             ("PR", "Privado"),
    )
    
    momento = models.DateTimeField(default=datetime.now, null=True, blank=True)
    paciente = models.ForeignKey(Persona, related_name='admisiones')
    fiadores = models.ManyToManyField(Persona, related_name='fianzas')
    referencias = models.ManyToManyField(Persona, related_name='referencias')
    
    diagnostico = models.CharField(max_length=200, blank=True)
    doctor = models.CharField(max_length=200, blank=True)
    # especialidad = ReferenceField(Especialidad)
    
    tipo_de_habitacion = models.CharField(max_length=200, blank=True)
    habitacion = models.CharField(max_length=200, blank=True)
    arancel = models.CharField(max_length=200, blank=True, choices=ARANCELES)
    
    pago = models.CharField(max_length=200, blank=True, choices=PAGOS)
    
    poliza = models.CharField(max_length=200, blank=True)
    certificado = models.CharField(max_length=200, blank=True)
    aseguradora = models.CharField(max_length=200, blank=True,
                                   choices=ASEGURADORA)
    deposito = models.CharField(max_length=200, blank=True)
    
    observaciones = models.CharField(max_length=200, blank=True)
    admitio = models.ForeignKey(User)
    admision = models.DateTimeField(default=datetime.now,null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue ingresada en
    admisiones"""
    autorizacion = models.DateTimeField(default=datetime.now,null=True, blank=True)
    hospitalizacion = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue internada"""
    ingreso = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue enviada al area
    de enfermeria"""
    fecha_pago = models.DateTimeField(default=datetime.now,null=True, blank=True)
    fecha_alta = models.DateTimeField(default=datetime.now,null=True, blank=True)
    uuid = UUIDField(version=4)
    codigo = ImageField(upload_to="admision/codigo/%Y/%m/%d", blank=True)
    qr = ImageField(upload_to="admision/codigo/%Y/%m/%d/qr", blank=True)
    estado = models.CharField(max_length=1, blank=True, choices=ESTADOS)
    
    def generar_codigo(self):
        
        """
        Crea un codigo de barras del tipo Code 128 para una :class:`Admision`
        """
        
        codigo = code128.Code128(str(self.uuid))
        imagen = image_to_content(codigo.render())
        self.codigo.save('{0}.jpg'.format(self.uuid), imagen)
    
    def generar_qr(self):
        
        """
        Crea un codigo de barras del tipo Code 128 para una :class:`Admision`
        """
        
        imagen = image_to_content(pyqrcode.MakeQRImage(self.uuid))
        self.qr.save('{0}.jpg'.format(self.uuid), imagen)
    
    def autorizar(self):
        
        if self.autorizacion == self.momento:
            self.autorizacion = datetime.now()
        self.estado = 'B'
        self.save()
    
    def hospitalizar(self):
        
        if self.hospitalizacion == self.momento:
            self.hospitalizacion = datetime.now()
        self.estado = 'H'
        self.save()
    
    def tiempo_autorizacion(self):
        
        """Calcula el tiempo que se tarda una :class:`Persona` para ser admitida
        en el :class:`Hospital`"""
        
        if self.autorizacion <= self.momento:
            
            return 0
        
        return (self.autorizacion - self.momento).seconds / 60
    
    def tiempo_admisiones(self):
        
        """Calcula el tiempo que se tarda una :class:`Persona` para ser admitida
        en el :class:`Hospital`"""
        
        if self.admision <= self.momento:
            
            return 0
        
        return (self.admision - self.momento).seconds / 60
    
    def tiempo_ahora(self):
        
        ahora = datetime.now()
        if self.momento >= ahora:
            
            return 0
        return (ahora - self.momento).seconds / 60
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'admision-view-id', [self.id]
