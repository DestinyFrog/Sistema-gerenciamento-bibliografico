from flask import make_response
import json

def erro_html( mensagem ):
    return make_response( f"<p style=\"color:red;\">{mensagem}</p>\
                            <a href=\"/login/index.html\">Voltar</a>" )

def escrever_arquivo( caminho, data ):
    data_arquivo = open( caminho, "w" )
    data_arquivo.write( data )
    data_arquivo.close()

def abrir_arquivo( caminho ):
    data_arquivo = open( caminho )
    texto = data_arquivo.read()
    data = json.loads( texto )
    data_arquivo.close()
    return data

def maior_id():
    data_arquivo = abrir_arquivo( "data/livros.json" )
    data = json.loads( data_arquivo )

    maior = 0
    for d in data:
        if d["id"] > maior:
            maior = d["id"]
    return maior
