from datetime import date, timedelta
from flask import Flask, make_response, request, redirect, send_from_directory
from sequelier import Sequelier
from autenticacao import Autenticacao
from pdfer import PDFer
import json
import sys

#region Dados
with open( "data/livros.json", "r" ) as f:
	l_livros = json.loads( f.read() )
 
with open( "data/usuario.json", "r" ) as f:
	l_usuarios = json.loads( f.read() )
 
with open( "data/eventos.json", "r" ) as f:
	l_eventos = json.loads( f.read() )
#endregion

PDFer = PDFer()
sequel = Sequelier()
auth = Autenticacao()
app = Flask(__name__)

#! Redireciona o caminho "/" para "/login/index.html"
@app.route("/")
def ini():
	# Checar Login
	logado = auth.checar_login( request, l_usuarios )

	if logado == True:
		# Se estiver logado ...

		if auth.checar_admin( request, l_usuarios ) == True:
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
	return send_from_directory('publico', path)

#region Livros

@app.route( "/relatorio_livros" )
def relatorio_livros():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	data = sequel.ler( l_livros )

	for i in data:
		evento = sequel.encontrar_um( l_eventos, i.get("id"), ["livro"] )
		if evento == None:
			i["status"] = "disponível"
		else:
			i["status"] = evento.get("status")

	PDFer.RelatorioLivros( data )

	with open( "doc.pdf", "rb" ) as file:
		resposta = make_response( file.read() )
		resposta.headers['Content-Type'] = 'application/pdf'
		return resposta

@app.route( "/ler_livros" )
def ler_livros():
	logado = auth.checar_login( request, l_usuarios )
	if logado != True:
		return logado

	proc = request.args.get("proc")
	id = request.args.get("id")

	if proc != None:
		data = sequel.encontrar_similares( l_livros, proc, [ "titulo", "autor", "generos" ] )
	elif id != None:
		id = int( id )
		data = sequel.encontrar_um( l_livros, id )
	else:
		data = sequel.ler( l_livros )

	data = sequel.copy( data )

	if id == None:
		for i in data:
			evento = sequel.encontrar_um( l_eventos, i.get("id"), ["livro"] )
			if evento == None:
				i["status"] = "disponível"
			else:
				i["status"] = evento.get("status")
	else:
		evento = sequel.encontrar_um( l_eventos, data.get("id"), ["livro"] )
		if evento == None:
			data["status"] = "disponível"
		else:
			data["status"] = evento.get("status")

	resposta = make_response( data )
	return resposta

@app.route( "/add_livros" )
def add_livros():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	novo_livro = {}
	novo_livro["titulo"] = request.args.get("titulo")
	novo_livro["autor"] = request.args.get("autor")
	novo_livro["imagem"] = request.args.get("imagem")
	novo_livro["generos"] = request.args.get("tags").split("\r\n")
	novo_livro["descricao"] = request.args.get("descricao")
	novo_livro["acessos"] = 0

	sequel.adicionar( l_livros, novo_livro )
	# resposta = make_response( data )
	# return resposta
	return redirect( "/admin/livros/index.html" )

@app.route( "/edit_livros" )
def edit_livros():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )

	livro_editado = {}
	livro_editado["titulo"] = request.args.get("titulo")
	livro_editado["autor"] = request.args.get("autor")
	livro_editado["imagem"] = request.args.get("imagem")
	livro_editado["generos"] = request.args.get("generos")

	if livro_editado.get("generos") != None:
		livro_editado["generos"].split("\n")

	sequel.editar( l_livros, id, livro_editado )
	return redirect( "/admin/livros/index.html" )

@app.route( "/del_livros" )
def del_livros():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	sequel.deletar( l_livros, id )
	return redirect( "/admin/livros/index.html" )

#endregion

#region Usuarios

@app.route( "/ler_usuarios" )
def ler_usuarios():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	proc = request.args.get("proc")
	id = request.args.get("id")

	if proc != None:
		data = sequel.encontrar_similares( l_usuarios, proc, [ "usuario", "email" ] )
	elif id != None:
		id = int( id )
		data = sequel.encontrar_um( l_usuarios, id )
	else:
		data = sequel.ler( l_usuarios )

	resposta = make_response( data )
	return resposta

@app.route( "/add_usuarios" )
def add_usuarios():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	novo_usuario = {}

	novo_usuario["usuario"] = request.args.get("usuario")
	novo_usuario["senha"] = request.args.get("senha")
	novo_usuario["admin"] = False
	novo_usuario["email"] = request.args.get("email")

	sequel.adicionar( l_usuarios, novo_usuario )
	return redirect( "/admin/usuarios/index.html" )

@app.route( "/edit_usuarios" )
def edit_usuarios():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )

	usuario_editado = {}
	usuario_editado["usuario"] = request.args.get("usuario")
	usuario_editado["senha"] = request.args.get("senha")
	usuario_editado["admin"] = request.args.get("admin") == "on"
	usuario_editado["email"] = request.args.get("email")

	sequel.editar( l_usuarios, id, usuario_editado )
	return redirect( "/admin/usuarios/index.html" )

@app.route( "/del_usuarios" )
def del_usuarios():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	sequel.deletar( l_usuarios, id )
	return redirect( "/admin/usuarios/index.html" )

@app.route( "/logar", methods=["POST","GET"] )
def logar():
	return auth.logar( request, l_usuarios )

@app.route( "/souadmin" )
def sou_admin():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado
	else:
		return ""

@app.route( "/sair" )
def sair():
	resposta = redirect( "/", code=302 )
	resposta.delete_cookie( "usuario" )
	return resposta

#endregion

#region Eventos

@app.route( "/relatorio_eventos" )
def relatorio_eventos():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	data = sequel.ler( l_eventos )
	data = sequel.conectar( data, l_usuarios, "usuario" )
	data = sequel.conectar( data, l_livros, "livro" )

	PDFer.RelatorioEventos( data )

	with open( "doc.pdf", "rb" ) as file:
		resposta = make_response( file.read() )
		resposta.headers['Content-Type'] = 'application/pdf'
		return resposta

@app.route( "/ler_eventos" )
def ler_eventos():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = request.args.get("id")

	if id != None:
		id = int( id )
		data = sequel.encontrar_um( l_eventos, id )
	else:
		data = sequel.ler( l_eventos )

	data = sequel.conectar( data, l_usuarios, "usuario" )
	data = sequel.conectar( data, l_livros, "livro" )

	resposta = make_response( data )
	return resposta

@app.route( "/add_eventos" )
def add_eventos():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado
	pass

@app.route( "/edit_eventos" )
def edit_eventos():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )

	evento_editado = {}
	evento_editado["usuario"] = request.args.get("usuario")
	evento_editado["senha"] = request.args.get("livro")
	evento_editado["admin"] = request.args.get("admin")
	evento_editado["email"] = request.args.get("email")

	data = sequel.editar( l_usuarios, id, evento_editado )
	resposta = make_response( data )
	return resposta

@app.route( "/del_eventos" )
def del_eventos():
	logado = auth.checar_admin( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	data = sequel.deletar( l_eventos, id )
	resposta = make_response( data )
	return resposta

@app.route( "/agendar" )
def agendar():
	logado = auth.checar_login( request, l_usuarios )
	if logado != True:
		return logado

	usuario_do_cookie = request.cookies.get("usuario")

	usuario = sequel.encontrar_um( l_usuarios, usuario_do_cookie, ["usuario"] )
	livro_id = int( request.args.get("id") )

	novo_evento = {
		"usuario": usuario.get("id"),
		"livro": livro_id,
		"data-inicial": date.today().strftime("%d/%m/%Y"),
		"status": "agendado"
	}

	evento = sequel.adicionar( l_eventos, novo_evento )
	livro = sequel.encontrar_um( l_livros, livro_id )
	usuario = sequel.encontrar_um( l_usuarios, evento.get("usuario") )

	livro["acessos"] = livro["acessos"] + 1

	PDFer.ComprovanteAgendamento( livro, usuario, evento )
	email = PDFer.criarEmail( f"Agendamento do Livro - { livro.get('titulo') }", usuario.get("email"), f"Comprovante de Agendamento do Livro { livro.get('titulo') }" )
	PDFer.AnexarArquivo( "ComprovanteAgendamento.pdf", email )
	PDFer.enviarEmail( email )

	return redirect( "/livros/index.html" )

@app.route( "/emprestar" )
def emprestar():
	logado = auth.checar_login( request, l_usuarios )
	if logado != True:
		return logado

	data_atual = date.today()
	data_final = data_atual + timedelta( days=7 )
	evento_editado = {
		"data-inicial": data_atual.strftime("%d/%m/%Y"),
		"data-final": data_final.strftime("%d/%m/%Y"),
		"status": "emprestado"
	}
	
	evento = sequel.editar( l_eventos, int( request.args.get("id") ), evento_editado )

	livro = sequel.encontrar_um( l_livros, evento.get("livro") )
	usuario = sequel.encontrar_um( l_usuarios, evento.get("usuario") )

	PDFer.ComprovanteEmprestimo( livro, usuario, evento )
	email = PDFer.criarEmail( f"Empréstimo do Livro - { livro.get('titulo') }", usuario.get("email"), f"Comprovante de Empréstimo do Livro { livro.get('titulo') }" )
	PDFer.AnexarArquivo( "ComprovanteEmprestimo.pdf", email )
	PDFer.enviarEmail( email )

	return redirect( "/admin/index.html" )

@app.route( "/devolver" )
def devolver():
	logado = auth.checar_login( request, l_usuarios )
	if logado != True:
		return logado

	id = int( request.args.get("id") )
	evento = sequel.encontrar_um( l_eventos, id )
	livro = sequel.encontrar_um( l_livros, evento.get("livro") )
	usuario = sequel.encontrar_um( l_usuarios, evento.get("usuario") )

	PDFer.ComprovanteDevolucao( livro, usuario, evento )
	email = PDFer.criarEmail( f"Devolução do Livro - { livro.get('titulo') }", usuario.get("email"), f"Comprovante de Devolução do Livro { livro.get('titulo') }" )
	PDFer.AnexarArquivo( "ComprovanteDevolucao.pdf", email )
	PDFer.enviarEmail( email )

	sequel.deletar( l_eventos, id )

	return redirect( "/admin/index.html" )

#endregion

if __name__ == '__main__':
	port = 3000

	try:
		port = int( sys.argv[1] )
	except:
		pass

	app.run( "0.0.0.0", port, debug=True )