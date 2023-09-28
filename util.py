from flask import make_response
import json

def erro_html( mensagem ):
    return make_response( f"<p style=\"color:red;\">{mensagem}</p>\
                            <a href=\"/index.html\">Voltar</a>" )

def escrever_arquivo( caminho, data ):
    data_arquivo = open( caminho, "w" )
    texto = json.dumps( data )
    data_arquivo.write( texto )
    data_arquivo.close()

def abrir_arquivo( caminho ):
    data_arquivo = open( caminho )
    texto = data_arquivo.read()
    data_arquivo.close()
    return json.loads( texto )

