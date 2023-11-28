from flask import make_response, redirect, render_template
from sequelier import Sequelier

class Autenticacao:
	def __init__( self ):
		self.sequel = Sequelier()
		self.passos = []

	def pagina_erro( self ):
		template = render_template( "erro.html", status=404, descricao=self.passos )
		resposta = make_response( template )
		resposta.status_code = 404
		self.passos = []
		return resposta

	def logar( self, req, lista_usuario:list ):
		self.passos = []

		# verifica se foi encontrado um usuario
		usuario_do_form = req.form.get("usuario")
		usuario = self.sequel.encontrar_um( lista_usuario, usuario_do_form, ["usuario"] )

		if usuario == None:
			self.passos.append("❌ Usuário Não Encontrado")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Usuário Encontrado")

		# verifica se a senha está correta
		senha_do_form = req.form.get("senha")

		if usuario.get("senha") != senha_do_form:
			self.passos.append("❌ Senha Incorreta")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Senha Correta")

		resposta = redirect("/", code=302)
		resposta.set_cookie( "usuario", usuario.get("usuario") )
		return resposta

	def checar_login( self, req, lista_usuario:list ):
		self.passos = []

		usuario_do_cookie = req.cookies.get("usuario")
		usuario = self.sequel.encontrar_um( lista_usuario, usuario_do_cookie, ["usuario"] )

		if usuario == None:
			self.passos.append("❌ Usuário Não Logado")
			return self.pagina_erro()
		return True

	def checar_admin( self, req, lista_usuario:list ):
		self.passos = []

		usuario_do_cookie = req.cookies.get("usuario")
		usuario = self.sequel.encontrar_um( lista_usuario, usuario_do_cookie, ["usuario"] )

		if usuario == None:
			self.passos.append("❌ Usuário Não Logado")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Usuário Logado")

		# Verifica se é administrador
		if usuario.get("admin") != True:
			self.passos.append("❌ Usuário Não é Administrador")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Usuário é Administrador")

		return True
