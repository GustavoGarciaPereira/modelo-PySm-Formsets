from datetime import datetime
import hashlib
import random

from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    nome = models.CharField(('Nome'), max_length=70)
    cidade = models.CharField(('Cidade'), max_length=70, blank=True, null=True)
    tel_celular = models.CharField(('Telefone Celular'), max_length=13, blank=True, null=True)
    is_active = models.BooleanField(('Ativo'), default=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, null=True)
    email = models.EmailField(('E-mail'), blank=True, null=True)

    @property
    def get_list_url(self):
        return reverse('cliente:update',kwargs={'slug':self.slug})

    def gerar_hash(self):
        return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.gerar_hash()
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Dependente(models.Model):
    cliente = models.ForeignKey('Cliente',on_delete=models.PROTECT)
    descricao = models.CharField(('Nome'), max_length=40)
    tel_celular = models.CharField(('Telefone Celular'), max_length=13, blank=True, null=True)
    email = models.EmailField(('E-mail'), blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, null=True)

    @property
    def get_list_url(self):
        return reverse('cliente:update',kwargs={'slug':self.slug})
    
    def gerar_hash(self):
        return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.gerar_hash()
        super(Dependente, self).save(*args, **kwargs)

    def __str__(self):
        return self.descricao