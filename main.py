from flask import Flask, request, send_from_directory, redirect, make_response, render_template
from util import erro_html, escrever_arquivo, abrir_arquivo, maior_id
import json

app = Flask(__name__)

@app.route('/<path:path>')
def paginas_publicas( path ):
    return send_from_directory('publico', path)

@app.route('/privado/<path:path>')
def paginas_privadas( path ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
            if usu.get("admin") == True:
                return send_from_directory('privado', path)
            return erro_html( "Usuario não tem permissao para acessar essa pagina" )
    return erro_html( "Usuario não encontrado" )

@app.route( '/login', methods=["POST"] )
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    data = abrir_arquivo( "data/usuario.json" )

    for u in data:
        if u.get("usuario") == usuario:
            if u.get("senha") != senha:
                return erro_html( "Senha Incorreta" )

            response = make_response( redirect("/livros", code=302) )
            response.set_cookie( "nome_usuario", u.get("usuario") )
            return response
    return erro_html( "Usuario não encontrado" )

@app.route( '/cadastre', methods=["POST"] )
def cadastro():
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
        
            if usu.get("admin") == False:
                return erro_html( "Você não tem permissão para criar usuários" )
            else:
                novo_usuario = {
                    "usuario": request.form.get("usuario"),
                    "senha": request.form.get("senha"),
                    "admin": request.form.get("admin") == "on"
                }

                usuarios.append( novo_usuario )
                escrever_arquivo( "data/usuario.json", json.dumps( usuarios ) )

                response = make_response( f"Usuário cadastrado com sucesso" )
                return response

    return erro_html( "Usuario não encontrado" )

@app.route( '/sair', methods=["POST"] )
def sair():
    resposta = make_response( redirect( "/index.html", code=200 ) )
    resposta.delete_cookie( "nome_usuario" )
    return resposta

@app.route( "/livros", methods=["GET"] )
def get_livros():
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
            data = abrir_arquivo( "data/livros.json" )
            return render_template( "get_livros.html", livros=data )

    return erro_html( "Usuario não encontrado" )

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            pre_data = abrir_arquivo( "data/livros.json" )
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
    cookie_usuario = request.cookies.get("nome_usuario")
    data = abrir_arquivo( "data/usuario.json" )

    for usu in data:
        if usu.get("usuario") == cookie_usuario :

            if usu.get("admin") == False:
                return erro_html( "Você não tem permissão para cadastrar livros" )

            novo_livro = { "id": maior_id() + 1, "disponivel": True }
            novo_livro.titulo = request.form.get("titulo")
            novo_livro.autor = request.form.get("autor")

            data = abrir_arquivo( "data/livros.json" )
            data.append( novo_livro )
            escrever_arquivo( "data/livros.json", json.dumps( data ) )

    return make_response( redirect("/livros", code=302) )

if __name__ == '__main__':
    app.run( '127.0.0.1', 3030, debug=True )
