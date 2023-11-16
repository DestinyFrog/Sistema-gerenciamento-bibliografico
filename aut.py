from flask import make_response, redirect, render_template
from memoria import Arquivo

class Autenticacao:
	def __init__( self ):
		self.base = Arquivo( "./data/usuario.json" )
		self.passos = []

	def pagina_erro( self ):
		template = render_template( "erro.html", status=404, descricao=self.passos )
		resposta = make_response( template )
		resposta.status_code = 404
		self.passos = []
		return resposta

	def logar( self, req ):
		self.passos = []

		# verifica se foi encontrado um usuario
		usuario_do_form = req.form.get("usuario")
		usuario = self.base.encontrar_um( "usuario", usuario_do_form )

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
		resposta.set_cookie( "usuario", usuario.get("id") )
		return resposta

	def checar_login( self, req ):
		self.passos = []

		usuario_do_cookie = req.cookies.get("usuario")
		usuario = self.base.encontrar_um( "id", usuario_do_cookie )

		if usuario == None:
			self.passos.append("❌ Usuário Não Logado")
			return self.pagina_erro()

		return True

	def checar_admin( self, req ):
		self.passos = []

		usuario_do_cookie = req.cookies.get("usuario")
		usuario = self.base.encontrar_um( "id", usuario_do_cookie )

		if usuario == None:
			self.passos.append("❌ Usuário Não Logado")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Usuário Logado")

		# Verifica se é administrador
		if usuario.get("admin") == True:
			self.passos.append("❌ Usuário Não é Administrador")
			return self.pagina_erro()
		else:
			self.passos.append("✅ Usuário é Administrador")

		return True

auth = Autenticacao()