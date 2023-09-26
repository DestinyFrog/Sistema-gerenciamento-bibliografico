from flask import Flask, request, send_from_directory, redirect, make_response
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
def pagina_statica( path ):
    return send_from_directory('static', path)

# editar cookies
'''
@app.route( '/ver', methods=["GET","POST"] )
def ver():
    cook = request.cookies.get("nome_usuario")
    resposta = make_response( cook or "nothing" )
    return resposta

@app.route( '/apagar', methods=["GET","POST"] )
def apagar():
    resposta = make_response( "cookies apagados" )
    resposta.delete_cookie( "nome_usuario" )
    return resposta
# '''

@app.route( '/login', methods=["POST"] )
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    data = json.loads( abrir_arquivo( "data/usuario.json" ) )

    for u in data:
        if u.get("usuario") == usuario:
            if u.get("senha") != senha:
                response = make_response( f"<p style=\"color:red;\">Senha Incorreta</p>\
                                            <a href=\"/login/index.html\">Voltar</a>" )
                return response

            response = make_response( redirect("/livros", code=302) )
            response.set_cookie( "nome_usuario", u.get("usuario") )
            return response

    response = make_response( f"<p style=\"color:red;\">Usuario não Encontrado</p>\
                                <a href=\"/login/index.html\">Voltar</a>" )
    return response

@app.route( "/livros", methods=["GET"] )
def get_livros():
    # ''' Verifica autenticacao
    cookie_usuario = request.cookies.get("nome_usuario")
    data_arquivo = abrir_arquivo( "data/usuario.json" )
    usuarios = json.loads( data_arquivo )

    for d in usuarios:
        if d.get("usuario") == cookie_usuario:

            data = json.loads( abrir_arquivo( "data/livros.json" ) )
            model = abrir_arquivo( "templates/get_livros.html" )
            template = Template( model )
            template_final = template.render( { 'livros': data } )

            resposta = make_response( template_final )
            return resposta

    return make_response( redirect( "/login/index.html", code=401 ) )
    # '''

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
    # ''' Verifica autenticacao com cookies
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = json.loads( abrir_arquivo( "data/usuario.json" ) )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            pre_data = json.loads( abrir_arquivo( "data/livros.json" ) )
            data = {}
            for d in pre_data:
                if d.get("id") == id:
                    data = d
                    break

            modelo = abrir_arquivo( "templates/unico_livro.html" )
            template = Template( modelo )
            template_final = template.render( { 'livro': data } )
            resposta = make_response( template_final )
            return resposta

    resposta = make_response( redirect( "/login/index.html", code=401 ) )
    return resposta
    # '''

@app.route( "/add-livro", methods=["POST"] )
def post_livro():
    # ''' Verifica autenticacao
    cookie_usuario = request.cookies.get("nome_usuario")
    data = json.loads( abrir_arquivo( "data/usuario.json" ) )

    for usu in data:
        if usu.get("usuario") == cookie_usuario :

            if usu.get("admin") == False:
                return make_response( f"<p style=\"color:red;\">Vocẽ não tem permissao para cadastrar livros</p>\
                                        <a href=\"/login/index.html\">Voltar</a>" )

            # ''' Adicionar Livros no arquivo 'data/livros.json'
            novo_livro = {
                "titulo": request.form.get( "titulo" ),
                "autor": request.form.get( "autor" ),
                "id": maior_id() + 1,
                "disponivel": True
            }

            data = json.loads( abrir_arquivo( "data/livros.json" ) )
            data.append( novo_livro )
            escrever_arquivo( "data/livros.json", json.dumps( data ) )

            resposta = make_response( redirect("/livros", code=302) )
            return resposta
            # '''

    return make_response( redirect( "/livros", code=401 ) )
    # '''

if __name__ == '__main__':
    app.run( '127.0.0.1', 3030, debug=True )