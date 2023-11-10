from flask import Flask, request, send_from_directory, redirect, make_response, render_template
from memoria import Arquivo
from autenticacao import Autenticacao

arq_usuarios = Arquivo( "./data/usuario.json" )
arq_livros = Arquivo( "./data/livros.json" )
auth = Autenticacao()

app = Flask(__name__)

#! Redireciona o caminho "/" para "/login/index.html"
@app.route("/")
def ini():
    return redirect( "/get_livros/index.html", code=302 )

#! Paginas estaticas sem autenticacao
@app.route('/<path:path>')
def paginas_publicas( path:str ):
    # retorna a pagina requerida
    return send_from_directory('publico', path)

#! Paginas estaticas com autenticacao de administrador
@app.route('/privado/<path:path>')
def paginas_privadas( path:str ):
    # procura por um usuario com o mesmo nome do usuario na base de dados 'usuarios'
    resposta = next( auth.autenticar( request, adm=True ) )

    # retorna a pagina requerida
    if resposta == None:
        resposta = send_from_directory( "admin", path )

    return resposta

#! Autenticação do usuário
@app.route( '/logar', methods=["POST","GET"] )
def login():
    for r in auth.autenticar( request, True ):
        if r != None:
            return r

    # caso esteja tudo certo, ele retorna uma resposta ...
    # que redireciona para a pagina de livros ... e ...
    # um cookie com o id do usuario autenticado
    resposta = redirect("/get_livros/index.html", code=302)
    resposta.set_cookie( "usuario", arq_usuarios.encontrar_um( "usuario", request.form.get("usuario") ).get("id") )
    return resposta

#! Realiza cadastro de novos usuarios
@app.route( "/cadastre", methods=["POST"] )
def cadastro():
    # Cria um novo objeto de usuario    
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    resposta = auth.cadastrar_usuario( usuario, senha )

    if resposta == None:
        # redireciona para a pagina de login
        resposta = redirect( "/", code=302 )

    return resposta

#! Sai do site e apaga os cookies
@app.route( "/sair" )
def sair():
    resposta = redirect( "/", code=302 )
    resposta.delete_cookie( "usuario" )
    return resposta

#! Retorna todos os livros
@app.route( "/todos-livros" )
def get_livros():    
    resposta = next( auth.autenticar( request ) )

    # Procura pelo livro requisitado
    if resposta == None:
        procura_data = request.args.get("proc")

        if procura_data == "" or procura_data == None:
            data = arq_livros.ler()
        else:
            data = arq_livros.encontrar_similares( ["titulo","autor"], procura_data )

        template = render_template( "get_livros.html", livros=data )
        resposta = make_response( template )

    return resposta

# /livros/id/2

#! Procura livro por seu id
@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id:int ):
    resposta = next( auth.autenticar( request ) )

    if resposta == None:
        # procura um livro igual ao parametro id
        data = arq_livros.encontrar_um( "id", id )

        # renderiza a pagina com os dados encontrador
        template = render_template( "unico_livro.html", livro=data )
        resposta = make_response( template )

    return resposta

#! Roda toda a aplicaçao
app.run( host="0.0.0.0", port=3000, debug=True )