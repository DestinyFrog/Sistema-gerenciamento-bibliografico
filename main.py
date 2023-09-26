from flask import Flask, request, send_from_directory, redirect, make_response, render_template
import json

app = Flask(__name__)

def erro_html( mensagem ):
    resposta = make_response( f"<p style=\"color:red;\">{mensagem}</p>\
                            <a href=\"/login/index.html\">Voltar</a>" )
    return resposta
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
def pagina_estatica( path ):
    return send_from_directory('static', path)

@app.route( '/login', methods=["POST"] )
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    data = json.loads( abrir_arquivo( "data/usuario.json" ) )

    for u in data:
        if u.get("usuario") == usuario:
            if u.get("senha") != senha:
                return erro_html( "Senha Incorreta" )

            response = make_response( redirect("/livros", code=302) )
            response.set_cookie( "nome_usuario", u.get("usuario") )
            return response
    return erro_html( "Usuario não encontrado" )

@app.route( "/livros", methods=["GET"] )
def get_livros():
    cookie_usuario = request.cookies.get("nome_usuario")
    data_arquivo = abrir_arquivo( "data/usuario.json" )
    usuarios = json.loads( data_arquivo )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
            data = json.loads( abrir_arquivo( "data/livros.json" ) )
            return render_template( "get_livros.html", livros=data )

    return erro_html( "Usuario não encontrado" )

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
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

            return render_template( "unico_livro.html", livro=data )

    resposta = make_response( redirect( "/login/index.html", code=401 ) )
    return resposta

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
