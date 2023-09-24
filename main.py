from flask import Flask, make_response
from jinja2 import Template
import json

app = Flask(__name__)

def abrir_arquivo( caminho ):
    data_arquivo = open( caminho )
    data = data_arquivo.read()
    data_arquivo.close()
    return data

@app.route( "/livros", methods=["GET"] )
def get_livros():
    data_arquivo = abrir_arquivo( "data/data.json" )
    data = json.loads( data_arquivo )

    model = abrir_arquivo( "templates/get_livros.html" )
    template = Template( model )
    template_final = template.render( { 'livros': data } )

    return template_final

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
    data_arquivo = abrir_arquivo( "data/data.json" )
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
    data_arquivo = abrir_arquivo( "data/data.json" )
    pre_data = json.loads( data_arquivo )

    data = []
    for d in pre_data:
        if d.get("autor") == autor:
            data.append( d )

    model = abrir_arquivo( "templates/get_livros.html" )
    template = Template( model )
    template_final = template.render( { 'livros': data } )

    return template_final

if __name__ == '__main__':
    app.run( '127.0.0.1', 3030, debug=True )