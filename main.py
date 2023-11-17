from flask import Flask, request, send_from_directory, redirect, make_response, render_template
from memoria import Arquivo
from autenticacao import auth

arq_livros = Arquivo( "./data/livros.json" )

app = Flask(__name__)

#! Redireciona o caminho "/" para "/login/index.html"
@app.route("/")
def ini():
	# Checar Login
	logado = auth.checar_login( request )

	if logado == True:
		# Se estiver logado ...

		if auth.checar_admin( request ) == True:
			# e Admin
			# retorna pagina de Admin
			return redirect( "/admin/index.html", code=302 )
		else:
			# nao e Admin
			# retorna todos os livros
			return redirect( "/livros/index.html", code=302 )
	else:
		# Se nao estiver logado retorna a pagina de login
		return redirect( "/login/index.html", code=302 )

#! Paginas estaticas sem autenticacao
@app.route('/<path:path>')
def paginas_publicas( path:str ):
	# retorna a pagina requerida
	return send_from_directory('publico', path)

#! Sai do site e apaga os cookies
@app.route( "/sair" )
def sair():
    # Apaga os cookies de autenticacao do usuario
	resposta = redirect( "/", code=302 )
	resposta.delete_cookie( "usuario" )
	return resposta

# #! Autenticação do usuário
@app.route( '/logar', methods=["POST","GET"] )
def login():
	# Realizar login
	return auth.logar( request )

#! Retorna todos os livros
@app.route( "/livros" )
def todos_livros():
	# Checar Login
	logado = auth.checar_login( request )

	# Retorna erro se nao logado
	if logado != True:
		return logado

	# Procura pelo livro requisitado
	procura_data = request.args.get("proc")

	if procura_data == None:
		data = arq_livros.ler()
	else:
		data = arq_livros.encontrar_similares( ["titulo","autor"], procura_data )

	# template = render_template( "lista_livros.html", livros=data )
	resposta = make_response( data )
	return resposta

#! Procura livro por seu id
@app.route( "/livros/id/<int:id>" )
def livros_por_id( id:int ):
	# Checar Login
	logado = auth.checar_login( request )

	# Retorna erro se nao logado
	if logado != True:
		return logado

	# procura um livro igual ao parametro id
	data = arq_livros.encontrar_um( "id", id )

	# renderiza a pagina com os dados encontrador
	# template = render_template( "unico_livro.html", livro=data )
	resposta = make_response( data )
	return resposta

#! Roda toda a aplicaçao
app.run( host="0.0.0.0", port=3000, debug=True )