from flask import make_response, render_template
from memoria import Arquivo

import random
import string

class Autenticacao:

    def __init__( self ):
        self.base = Arquivo( "./data/usuario.json" )

    def gerar_ID( _, tamanho=8 ):
        letras = string.ascii_lowercase
        return ''.join(random.choice(letras) for _ in range( tamanho ))

    def autenticar( self, req, login=False, adm=False ):
        # procura por um usuario com o mesmo nome do usuario na base de dados 'usuarios'
        
        passos = []
        resposta = None

        if login == False:
            usu = self.base.encontrar_um( "id", req.cookies.get("usuario") )

            # verifica se foi encontrado um usuario	
            if usu == None:
                passos.append("❌ Usuário Não Logado")
                template = render_template( "erro.html", status=404, descricao=passos )
                resposta = make_response( template )
                resposta.status_code = 404
            else:
                passos.append("✅ Usuário Logado")

        else:
            usu = self.base.encontrar_um( "usuario", req.form.get("usuario") )

            # verifica se foi encontrado um usuario
            if usu == None:
                passos.append("❌ Usuário Não Encontrado")
                template = render_template( "erro.html", status=404, descricao=passos )
                resposta = make_response( template )
                resposta.status_code = 404
            else:
                passos.append("✅ Usuário Encontrado")

        yield resposta

        if req.form.get("senha") != None:

            # verifica se a senha enviada pelo form corresponde com a do usuario
            if usu.get("senha") != req.form.get("senha"):
                passos.append("❌ Senha Incorreta")
                template = render_template( "erro.html", status=403, descricao=passos ) 
                resposta = make_response( template )
                resposta.status_code = 403
            else:
                passos.append("✅ Senha Correta")

            yield resposta

        if adm == True:
            # verifica se o usuario e administrador
            if usu.get("admin") == False:
                passos.append("❌ Usuário Não Tem Permissão para Realizar essa Ação")
                template = render_template( "erro.html", status=403, descricao=passos, redireciona="/livros" )
                resposta = make_response( template )
                resposta.status_code = 403
            else:
                passos.append("✅ Usuário Tem Permissão de Administrador")

            yield resposta