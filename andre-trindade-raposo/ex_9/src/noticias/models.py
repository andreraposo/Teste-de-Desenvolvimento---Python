from flask import Flask
import mongoengine as me
from datetime import datetime

class Autor(me.Document):
    username = me.StringField(max_length=50, required=True, unique=True)
    email = me.EmailField(required=True, unique=True)
    nome = me.StringField(max_length=100, required=True)
    sobrenome = me.StringField(max_length=100, required=True)
    data_criacao = me.DateTimeField(default=datetime.now())

class Noticia(me.Document):
    titulo = me.StringField(max_length=100, required=True)
    conteudo = me.StringField(required=True)
    autor = me.ReferenceField(Autor, required=True)
    data_criacao = me.DateTimeField(default=datetime.now())
    data_edicao = me.DateTimeField(default=datetime.now())
