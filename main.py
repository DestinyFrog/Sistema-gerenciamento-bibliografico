from flask import Flask, request, send_from_directory, redirect, make_response, render_template
from memoria import Arquivo
from autenticacao import Autenticacao
from eventos import Eventos

arq_livros = Arquivo( "./data/livros.json" )
auth = Autenticacao()
empres = Eventos( arq_livros, auth )

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

#! Verifica Admin
@app.route('/souadmin')
def souadmin():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado
	else:
		return ""

#! Autenticação do usuário
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
		data = arq_livros.encontrar_similares( ["titulo","autor","generos"], procura_data )

	for d in data:
		empres.encontrar_por_livro( d )

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
	empres.encontrar_por_livro( data )

	# renderiza a pagina com os dados encontrador
	resposta = make_response( data )
	return resposta

#! Adiciona um dos livros
@app.route( "/novo_livro" )
def adicionar_livro():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	titulo = request.args.get("titulo")
	autor = request.args.get("autor")
	imagem = request.args.get("imagem")
	generos = request.args.get("generos").split("|")

	novo_livro = {
		"titulo": titulo,
		"autor": autor,
		"imagem": imagem,
		"generos": generos
	}

	arq_livros.adicionar( novo_livro )
	return redirect( "/", code=302 )

#! Remove um dos livros
@app.route( "/remover_livro" )
def remover_livro():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	arq_livros.remover( id )

	return redirect( "/admin/livros/index.html", code=302 )

# ! Edita informações de um livro
@app.route( "/editar_livro" )
def editar_livro():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	titulo = request.args.get("titulo")
	autor = request.args.get("autor")
	imagem = request.args.get("imagem")
	generos = request.args.get("generos").split("\n")

	arq_livros.editar( "titulo", titulo, id )
	arq_livros.editar( "autor", autor, id )
	arq_livros.editar( "imagem", imagem, id )
	arq_livros.editar( "generos", generos, id )

	return redirect( "/admin/livros/index.html", code=302 )

#! Lista os usuarios
@app.route( "/usuarios" )
def todos_usuarios():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	# Procura pelo livro requisitado
	procura_data = request.args.get("proc")

	if procura_data == None:
		data = auth.base.ler()
	else:
		data = auth.base.encontrar_similares( ["usuario"], procura_data )

	resposta = make_response( data )
	return resposta

#! Adiciona um dos usuarios
@app.route( "/novo_usuario" )
def adicionar_usuario():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	usuario = request.args.get("usuario")
	senha = request.args.get("senha")
	admin = request.args.get("admin")

	novo_usuario = {
		"usuario": usuario,
		"senha": senha,
		"admin": admin
	}

	auth.base.adicionar( novo_usuario )
	return redirect( "/", code=302 )

#! Remove um dos usuarios
@app.route( "/remover_usuario" )
def remover_usuario():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	auth.base.remover( id )

	return redirect( "/admin/usuarios/index.html", code=302 )

# ! Edita informações de um livro
@app.route( "/editar_usuario" )
def editar_usuario():
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	usuario = request.args.get("usuario")
	senha = request.args.get("senha")
	admin = request.args.get("admin")

	auth.base.editar( "usuario", usuario, id )
	auth.base.editar( "senha", senha, id )
	auth.base.editar( "admin", admin, id )

	return redirect( "/admin/usuarios/index.html", code=302 )

#! Retorna todos os eventos
@app.route( "/eventos" )
def todos_eventos():
	logado = auth.checar_login( request )
	if logado != True:
		return logado

	data = empres.ler()

	resposta = make_response( data )
	return resposta

#! Adiciona agendamentos
@app.route( "/agendar/<int:id>" )
def adicionar_agendamentos( id ):
	# Checar Login
	logado = auth.checar_login( request )

	# Retorna erro se nao logado
	if logado != True:
		return logado

	usuario_nome = request.cookies.get("usuario")
	usu = auth.base.encontrar_um( "usuario", usuario_nome )
	empres.agendar_emprestimo( id, usu.get("id") )

	return redirect( "/", code=302 )

#! Adiciona emprestimos
@app.route( "/emprestimo/<int:id>" )
def emprestar( id ):
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	empres.realizar_emprestimo( id )
	return redirect( "/", code=302 )

#! Adiciona emprestimos
@app.route( "/devolucao/<int:id>" )
def devolver( id ):
	logado = auth.checar_admin( request )
	if logado != True:
		return logado

	empres.excluir_evento( id )
	return redirect( "/", code=302 )

#! Roda toda a aplicaçao
if __name__ == "__main__":
	app.run( host="0.0.0.0", port=3000, debug=True )