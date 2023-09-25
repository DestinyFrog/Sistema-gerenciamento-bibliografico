from flask import Flask, request, send_from_directory, redirect
from jinja2 import Template

import json

app = Flask(__name__)

def escrever_arquivo( caminho, data ):
    data_arquivo = open( caminho, "w" )
    data_arquivo.write( data )
    data_arquivo.close()
def abrir_arquivo( caminho ):
    data_arquivo = open( caminho )
    data = data_arquivo.read()
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

@app.route('/<path:path>')
def send_report( path ):
    return send_from_directory('static', path)

@app.route( "/livros", methods=["GET"] )
def get_livros():
    data_arquivo = abrir_arquivo( "data/livros.json" )
    data = json.loads( data_arquivo )

    model = abrir_arquivo( "templates/get_livros.html" )
    template = Template( model )
    template_final = template.render( { 'livros': data } )

    return template_final

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
    data_arquivo = abrir_arquivo( "data/livros.json" )
    pre_data = json.loads( data_arquivo )

    data = None
    for d in pre_data:
        if d.get("id") == id:
            data = d
            break

    model = abrir_arquivo( "templates/unico_livro.html" )
    template = Template( model )
    template_final = template.render( { 'livro': data } )

    return template_final

@app.route( "/livros/autor/<string:autor>", methods=["GET"] )
def get_livros_por_autor( autor ):
    data_arquivo = abrir_arquivo( "data/livros.json" )
    pre_data = json.loads( data_arquivo )

    data = []
    for d in pre_data:
        if d.get("autor") == autor:
            data.append( d )

    model = abrir_arquivo( "templates/get_livros.html" )
    template = Template( model )
    template_final = template.render( { 'livros': data } )

    return template_final

@app.route( "/add-livro", methods=["POST"] )
def post_livro():
    titulo = request.form.get( "titulo" )
    autor = request.form.get( "autor" )

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "id": maior_id() + 1,
        "disponivel": True
    }

    data_arquivo = abrir_arquivo( "data/livros.json" )
    data = json.loads( data_arquivo )
    data.append( novo_livro )

    escrever_arquivo( "data/livros.json", json.dumps( data ) )
    return redirect("/livros", code=302)

if __name__ == '__main__':
    app.run( '127.0.0.1', 3030, debug=True )