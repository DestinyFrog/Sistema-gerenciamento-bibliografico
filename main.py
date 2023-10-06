from flask import Flask, request, send_from_directory, redirect, make_response, render_template
import json

# Retorna uma mensagem de erro em forma de HTML
def erro_html( mensagem ):
    return make_response( f"<p style=\"color:red;\">{mensagem}</p>\<a href=\"/login/index.html\">Voltar</a>" )

# Reescreve um arquivo em dicionario/lista python para JSON
def escrever_arquivo( caminho, data ):
    data_arquivo = open( caminho, "w" )
    texto = json.dumps( data )
    data_arquivo.write( texto )
    data_arquivo.close()

# Le um arquivo como JSON para dicionario/lista python
def abrir_arquivo( caminho ):
    data_arquivo = open( caminho )
    texto = data_arquivo.read()
    data_arquivo.close()
    return json.loads( texto )

app = Flask(__name__)

#! Redireciona o caminho "/" para "/login/index.html"
@app.route("/")
def ini():
    return redirect( "/login/index.html", code=302 )

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
    usuarios = abrir_arquivo( "data/usuario.json" )

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
    for usu in abrir_arquivo( "data/usuario.json" ):
        if usu.get("usuario") == request.form.get("usuario"):

            if usu.get("senha") != request.form.get("senha"):
                return erro_html( "Senha Incorreta" )

            resposta = redirect("/livros", code=301)
            resposta.set_cookie( "nome_usuario", usu.get("usuario") )
            return resposta
    return erro_html( "Usuario não encontrado" )

#! Realiza cadastro de novos usuarios
'''
	Pega o conteudo do arquivo de usuarios

    cria um dicionario com as informaçoes do novo usuario
		- usuario : puxado da pagina html
        - senha : puxado da pagina html
        - admin : puxado da pagina html
        - agendamento : por padrao uma lista vazia

    adiciona o novo usuario a lista de usuarios
    reescreve o arquivo de usuarios
    redireciona para a pagina de login
'''
@app.route( "/cadastre", methods=["POST"] )
def cadastro():
    usuarios = abrir_arquivo( "data/usuario.json" )
    novo_usuario = {
		"usuario": request.form.get("usuario"),
		"senha": request.form.get("senha"),
		"admin": request.form.get("admin") == "on",
        "agendamento": []
	}
    usuarios.append( novo_usuario )
    escrever_arquivo( "data/usuario.json", usuarios )
    return redirect( "/", code=302 )

#! Sai do site e apaga os cookies
'''
    Cria uma resposta para redirecionar a pagina para o login
    remove os cookies que identificam o usuario
'''
@app.route( "/sair", methods=["GET"] )
def sair():
    resposta = redirect( "/", code=302 )
    resposta.delete_cookie( "nome_usuario" )
    return resposta

#! Retorna todos os livros
'''
	pega os dados dos cookies;
    le o arquivo de usuarios

    realiza um looping para verificar se os
    dados dos cookies estao na lista de usuarios

    #! Caso nao esteja retorna o erro "Usuario nao encontrado"

    pega as informaçoes de procura do html
    verifica se proc existe e nao e um texto vazio

		#! Caso contrario retorna os dados de todos os livros

		transforma os dados de procura em um texto minusculo
        cria uma lista vazia

        cria um loop para verificar aqueles dados dos livros
		com titulo semelhantes aos dados de procura
        e adiciona esses dados a lista vazia
        
        renderiza uma pagina html com os dados dos livro encontrados

'''
@app.route( "/livros", methods=["GET","POST"] )
def get_livros():
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            proc = request.form.get("proc")

            if proc and proc != "":
                proc = proc.lower()
                data = []
                for liv in abrir_arquivo( "data/livros.json" ):
                    if proc in liv.get("titulo").lower() or proc in liv.get("autor").lower():
                        data.append( liv )
            else:
                data = abrir_arquivo( "data/livros.json" )

            return render_template( "get_livros.html", livros=data, adm=usu.get("admin") )

    return erro_html( "Usuario não encontrado" )

#! Sistema de agendamento
'''
	pega o parametro chamado ID

	pega os dados dos cookies
    pega os dados do arquivo de usuarios

    faz um loop para verificar se o usuario existe
		#! Caso contrario retorna o erro "Usuario nao encontrado
        
        pega o arquivo de livros
        faz um loop para encontrar aquele livro com o ID igual	
        ao parametro ID
        
        Quando encontrar inverte o valor de "disponivel"
		
        adiciona esse ID a lista de agendamentos do usuario
        atualiza o arquivo de usuarios
        atualiza a pagina
'''
@app.route( "/agendar/<int:id>", methods=["GET"] )
def agendar( id ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = abrir_arquivo( "data/usuario.json" )

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            livros = abrir_arquivo( "data/livros.json" )
            for liv in livros:
                if liv.get("id") == id:
                    liv["disponivel"] = ( liv["disponivel"] == False )

            escrever_arquivo( "data/livros.json", livros )

            usu["agendamento"].append( id )
            escrever_arquivo( "data/usuario.json", usuarios )

            return redirect( f"/livros/id/{id}", code=302 )

    return erro_html( "Usuario não encontrado" )

#! Le cada livro
'''
	pega o parametro ID do livro
    pega os dados dos cookies
    pega o arquivo dos usuario

    faz um loop para verificar se o usuario
    dos cookies existe
		#! Caso contrario retorna o erro "Usuario nao encontrado"

        le o arquivo de livros
        Encontra entre os livros aquele com o ID igual
        ao parametro

        encerra o loop
        retorna uma pagina html com os dados do livro
'''
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

    return redirect( "/login/index.html", code=301 )

#! Adicionar um unico livro
'''
	pega os dados dos cookies
    pega o arquivo dos usuarios

    faz um loop para verificar se o usuario
    dos cookies existe
		#! Caso contrario retorna o erro "Usuario nao encontrado"
        
        verifica se o usuario encontrado e Administrador
        #! Caso contrario retorna o erro "Você não tem permissão para cadastrar livros"
        
        encontra o maior ID entre os livros
        
        cria um novo livro em forma de dicionario
			- id : maior ID
            - disponivel : True por padrao
            - titulo : dados do forms
            - autor : dados do forms
        
		abre o arquivo de livros
        adiciona o novo livro a lista de livros
        reescreve arquivo de livros
        
    redireciona para a pagina da lista de livros
'''
@app.route( "/add-livro", methods=["POST"] )
def add_livro():
    cookie_usuario = request.cookies.get("nome_usuario")
    data = abrir_arquivo( "data/usuario.json" )

    for usu in data:
        if usu.get("usuario") == cookie_usuario :

            if usu.get("admin") == False:
                return erro_html( "Você não tem permissão para cadastrar livros" )

			# encontrar o maior numero
            maior = -1
            for d in abrir_arquivo( "data/livros.json" ):
                if d.get("id") > maior:
                    maior = d.get("id")

            novo_livro = {
                "id": maior + 1,
                "disponivel": True,
                "titulo": request.form.get("titulo"),
                "autor": request.form.get("autor")
            }

            data = abrir_arquivo( "data/livros.json" )
            data.append( novo_livro )
            escrever_arquivo( "data/livros.json", data )

    return redirect( "/livros", code=301 )

# Roda toda a aplicaçao
if __name__ == "__main__":
    app.run( host="0.0.0.0", port=3000, debug=True )