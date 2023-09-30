from flask import Flask, request, send_from_directory, redirect, make_response, render_template
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

app = Flask(__name__)

#! Paginas estaticas sem autenticacao
'''
    Envia a pagina que esta no
    caminho especificado na rota
'''
@app.route('/<path:path>')
def paginas_publicas( path ):
    return send_from_directory('publico', path)

#! Paginas estaticas com autenticacao
'''
    procura no caminho especificado,
    porem antes verifica se nos cookies:
        - O usuario existe;
        - O usuario é um administrador;
    e por fim se ambos forem verdadeiros
    envia a pagina
    caso contrario retorna um erro
    que podem ser:
        - Usuario não tem permissao para acessar essa pagina
        - Usuario nao foi encontrado
'''
@app.route('/privado/<path:path>')
def paginas_privadas( path ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "serv/data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
            if usu.get("admin") == True:
                return send_from_directory('privado', path)
            return erro_html( "Usuario não tem permissao para acessar essa pagina" )
    return erro_html( "Usuario não foi encontrado" )

#! Realiza login
'''
    Abre um arquivo json com todos os usuarios
    visualiza entre todos eles qual tem o mesmo nome
    de usuario enviado pela pagina

    caso nao encontre retorna o erro:
    #! Usuario nao Encontrado

    depois verifica se a senha enviada pela pagina
    condiz com a do usuario selecionado

    caso sejam diferentes, retorna o erro:
    #! Senha Incorreta

    Se for logado corretamente, a pagina sera
    redirecionada para a rota '/livros'
'''
@app.route( '/login', methods=["POST"] )
def login():
    for usu in abrir_arquivo( "serv/data/usuario.json" ):
        if usu.get("usuario") == request.form.get("usuario"):

            if usu.get("senha") != request.form.get("senha"):
                return erro_html( "Senha Incorreta" )

            resposta = redirect("/livros", code=301)
            resposta.set_cookie( "nome_usuario", usu.get("usuario") )
            return resposta
    return erro_html( "Usuario não encontrado" )

#! Realiza cadastro de novos usuarios
'''

'''
@app.route( '/cadastre', methods=["POST"] )
def cadastro():
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "serv/data/usuario.json" )

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
                escrever_arquivo( "serv/data/usuario.json", usuarios )

                #resposta = make_response( "Usuário cadastrado com sucesso" )
                #return resposta
                return redirect( "/index.html", code=302 )

    return erro_html( "Usuario não encontrado" )

@app.route( '/sair', methods=["GET"] )
def sair():
    resposta = redirect( "/index.html", code=302 )
    resposta.delete_cookie( "nome_usuario" )
    return resposta

@app.route( "/livros", methods=["GET"] )
def get_livros():
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "serv/data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:
            data = abrir_arquivo( "serv/data/livros.json" )
            return render_template( "get_livros.html", livros=data, adm=usu.get("admin") )

    return erro_html( "Usuario não encontrado" )

@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "serv/data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            pre_data = abrir_arquivo( "serv/data/livros.json" )
            data = {}
            for d in pre_data:
                if d.get("id") == id:
                    data = d
                    break

            return render_template( "unico_livro.html", livro=data )

    return redirect( "/login/index.html", code=301 )

@app.route( "/add-livro", methods=["POST"] )
def add_livro():
    cookie_usuario = request.cookies.get("nome_usuario")
    data = abrir_arquivo( "serv/data/usuario.json" )

    for usu in data:
        if usu.get("usuario") == cookie_usuario :

            if usu.get("admin") == False:
                return erro_html( "Você não tem permissão para cadastrar livros" )

            maior = -1
            for d in abrir_arquivo( "serv/data/livros.json" ):
                if d.get("id") > maior:
                    maior = d.get("id")

            novo_livro = {
                "id": maior + 1,
                "disponivel": True,
                "titulo": request.form.get("titulo"),
                "autor": request.form.get("autor")
            }

            data = abrir_arquivo( "serv/data/livros.json" )
            data.append( novo_livro )
            escrever_arquivo( "serv/data/livros.json", data )

    return redirect( "/livros", code=301 )

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=3000, debug=True )
    # from waitress import serve
    # serve( app, host="0.0.0.0", port=3000 )
