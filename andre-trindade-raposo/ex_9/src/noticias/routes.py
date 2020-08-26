from flask import Flask, jsonify, request
from app import app
from noticias.models import *
from datetime import datetime

@app.route('/', methods=['GET'])
def home():
    return 'Página não encontrada', 404

# ADICIONA NOVAS NOTICIAS E EXIBE LISTA DAS NOTICIAS EXISTENTES

@app.route('/noticias/', methods=['GET', 'POST'])
def noticias():
    if request.method == 'GET':
        lista_noticias = []
        noticias = Noticia.objects()

        for noticia in noticias:
            get_noticia = {
                'titulo': noticia.titulo,
                'conteudo': noticia.conteudo,
                'data_criacao': noticia.data_criacao,
                'data_edicao': noticia.data_edicao,
                'autor': noticia.autor.nome + ' ' + noticia.autor.sobrenome
            }
            lista_noticias.append(get_noticia)

        return jsonify(lista_noticias), 200

    if request.method == 'POST':    # TODO formatar returns para excluir id
        nova_noticia = Noticia(
            titulo = request.form['titulo'],
            conteudo = request.form['conteudo'],
            autor = Autor()
        )

        # VERIFICA SE O AUTOR JÁ EXISTE PARA EVITAR DUPLICIDADE

        try:
            get_autor = Autor.objects(username=request.form['username']).get()
            
        except:
            autor_nome = request.form['autor'].split()
            nova_noticia.autor['username'] = request.form['username']
            nova_noticia.autor['email'] = request.form['email']
            nova_noticia.autor['nome'] = autor_nome[0]
            nova_noticia.autor['sobrenome'] = ' '.join(autor_nome[1:])
            nova_noticia.autor.save()
            nova_noticia.save()
            return jsonify(formata_return(nova_noticia)), 200

        nova_noticia.autor = get_autor
        nova_noticia.save()
        return jsonify(formata_return(nova_noticia)), 200

# LIDA COM NOTICIAS ESPECÍFICAS, RETORNA, EDITA OU REMOVE

@app.route('/noticia/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def noticia(id):
    if request.method == 'GET':
        try:
            noticia = Noticia.objects()[id - 1]
            return jsonify(formata_return(noticia)), 200

        except:
            return 'Noticia não encontrada', 404

    if request.method == 'PUT':
        try:
            noticia = Noticia.objects()[id - 1]

            titulo = request.form['titulo']
            conteudo = request.form['conteudo']
            data_edicao = datetime.now()

            noticia.titulo = titulo if titulo != '' else noticia.titulo
            noticia.conteudo = conteudo if conteudo != '' else noticia.conteudo
            noticia.data_edicao = data_edicao
            noticia.save()

            return jsonify(formata_return(noticia)), 200
        except:
            return 'Noticia não encontrada', 404

    if request.method == 'DELETE':
        try:
            noticia = Noticia.objects()[id - 1]
            noticia.delete()
            return 'Noticia excluída:', 200
        except:
            return 'Noticia não encontrada', 404

# LIDA COM FILTRAGEM DE RESULTADOS, RECEBE UM PARÂMETRO E RETORNA A QUERY

@app.route('/noticia/', methods=['GET'])
def noticia_filtrada():
    try:
        parametro = request.args
        noticias = []

        if len(parametro) > 1:
            return 'Erro: Argumentos demais', 404

        else:
            if 'titulo' in parametro:
                get_noticias = Noticia.objects(titulo__icontains=parametro['titulo'])
                for noticia in get_noticias:
                    noticias.append(
                        formata_return(noticia)
                    )

            elif 'conteudo' in parametro:
                get_noticias = Noticia.objects(conteudo__icontains=parametro['conteudo'])
                for noticia in get_noticias:
                    noticias.append(
                        formata_return(noticia)
                    )

            elif 'autor' in parametro:
                try:
                    get_noticias = Noticia.objects(
                        autor__icontains= Autor.objects(nome__icontains=parametro['autor']).get()
                    )

                except:
                    get_noticias = Noticia.objects(
                        autor__icontains= Autor.objects(sobrenome__icontains=parametro['autor']).get()
                    )

                if len(get_noticias) < 1:
                    get_noticias = Noticia.objects(
                        autor__icontains= Autor.objects(sobrenome__icontains=parametro['autor']).get()
                    )

                for noticia in get_noticias:
                    noticias.append(
                        formata_return(noticia)
                    )

            else:
                return 'Argumento inválido', 404

    except:
        return 'Nenhuma noticia encontrada', 404

    if len(noticias) > 0:
        return jsonify(noticias)
    else:
        return 'Nenhuma noticia encontrada', 404


def formata_return(noticia):
    return {
        'titulo': noticia.titulo,
        'conteudo': noticia.conteudo,
        'data_criacao': noticia.data_criacao,
        'data_edicao': noticia.data_edicao,
        'autor': noticia.autor.nome + ' ' + noticia.autor.sobrenome
    }
