from flask import Flask, request, send_from_directory, redirect, make_response, render_template
from memoria import Arquivo

# Retorna uma mensagem de erro em forma de HTML
def erro_html( mensagem ):
    resposta = make_response( f"<p style=\"color:red;\">{mensagem}</p>\<a href=\"/login/index.html\">Voltar</a>" )
    resposta.status_code = 401
    return resposta

arq_usuarios = Arquivo( "./data/usuario.json" )
arq_livros = Arquivo( "./data/livros.json" )

app = Flask(__name__)

#! Redireciona o caminho "/" para "/login/index.html"
@app.route("/")
def ini():
    return redirect( "/login/index.html", code=302 )

#! Paginas estaticas sem autenticacao
@app.route('/<path:path>')
def paginas_publicas( path:str ):
    # retorna a pagina requerida
    return send_from_directory('publico', path)

#! Paginas estaticas com autenticacao de administrador
@app.route('/privado/<path:path>')
def paginas_privadas( path:str ):    
    # procura por um usuario com o mesmo nome do usuario na base de dados 'usuarios'
    usu = arq_usuarios.encontrar_um( "usuario", request.cookies.get("usuario") )

    # verifica se foi encontrado um usuario
    if usu == None:
        template = render_template( "erro.html", status=404, descricao="Usuário Não Encontrado" )
        resposta = make_response( template )
        resposta.status_code = 404

    # verifica se o usuario encontrado e um administrador
    elif usu.get("admin") == False:
        template = render_template( "erro.html", status=401, descricao="Usuario não tem permissao para acessar essa pagina" )
        resposta = make_response( template )
        resposta.status_code = 401

    # retorna a pagina requerida
    else:
        resposta = send_from_directory( "admin", path )

    return resposta

#! Autenticação do usuário
@app.route( '/login', methods=["POST"] )
def login():
    # procura por um usuario com o mesmo nome do usuario na base de dados 'usuarios'
    usu = arq_usuarios.encontrar_um( "usuario", request.form.get("usuario") )

    # verifica se foi encontrado um usuario
    if usu == None:
        template = render_template( "erro.html", status=404, descricao="Usuário Não Encontrado" )
        resposta = make_response( template )
        resposta.status_code = 404

    # verifica se a senha enviada pelo form corresponde com a do usuario
    elif usu.get("senha") != request.form.get("senha"):
        template = render_template( "erro.html", status=403, descricao="Senha Incorreta" )
        resposta = make_response( template )
        resposta.status_code = 403

    # caso esteja tudo certo, ele retorna uma resposta ...
    # que redireciona para a pagina de livros ... e ...
    # um cookie com o id do usuario autenticado
    else:
        resposta = redirect("/livros", code=302)
        resposta.set_cookie( "usuario", usu.get("usuario") )

    return resposta

#! Realiza cadastro de novos usuarios
@app.route( "/cadastre", methods=["POST"] )
def cadastro():
    # Cria um novo objeto de usuario
    novo_usuario = {
        "usuario": request.form.get("usuario"),
        "senha": request.form.get("senha"),
        "admin": False,
        "agendamento": []
    }

    # Adiciona o usuario criado ao arquivo
    arq_usuarios.adicionar( novo_usuario )
    
    # redireciona para a pagina de login
    return redirect( "/", code=302 )

#! Sai do site e apaga os cookies
@app.route( "/sair", methods=["GET"] )
def sair():
    resposta = redirect( "/", code=302 )
    resposta.delete_cookie( "nome_usuario" )
    return resposta

#! Retorna todos os livros
@app.route( "/livros", methods=["GET","POST"] )
def get_livros():    
    usu = arq_usuarios.encontrar_um( "usuario", request.cookies.get("usuario") )

    if not usu:
        template = render_template( "erro.html", status=404, descricao="Usuário Não Encontrado" )
        resposta = make_response( template )
        resposta.status_code = 404

    else:
        procura_data = request.form.get("proc")

        if procura_data == None:
            data = arq_livros.ler()
        else:
            data = arq_livros.encontrar_similares( ["titulo","autor"], procura_data )

        resposta = render_template( "get_livros.html", livros=data, adm=usu.get("admin") )

    return resposta

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
def agendar( id:int ):
    cookie_usuario = request.cookies.get("nome_usuario")
    usuarios = arq_usuarios.ler()

    for usu in usuarios:
        if usu.get("usuario") == cookie_usuario:

            livros = arq_livros.ler()

            for liv in livros:
                if liv.get("id") == id:
                    liv["disponivel"] = ( liv["disponivel"] == False )            

            arq_livros.escrever( livros )

            usu["agendamento"].append( id )
            arq_usuarios.escrever( usuarios )

            return redirect( f"/livros/id/{id}", code=302 )

    return erro_html( "Usuario não encontrado" )

#! Procura livro por seu id
@app.route( "/livros/id/<int:id>", methods=["GET"] )
def get_livros_por_id( id:int ):  

    # verifica se o usuario esta autenticado pelos cookies
    if arq_usuarios.encontrar_um( "usuario", request.cookies.get("nome_usuario") ):

        # redireciona para a pagina inicial
        template = render_template( "erro.html", status=404, descricao="Usuário Não Encontrado" )
        resposta = make_response( template )
        resposta.status_code = 404

    else:
        # procura um livro igual ao parametro id
        data = arq_livros.encontrar_um( "id", id )

        # renderiza a pagina com os dados encontrador
        template = render_template( "unico_livro.html", livro=data )
        resposta = make_response( template )

    return resposta

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
    data = arq_usuarios.ler()

    for usu in data:
        if usu.get("usuario") == cookie_usuario :

            if usu.get("admin") == False:
                return erro_html( "Você não tem permissão para cadastrar livros" )

                        # encontrar o maior numero
            maior = -1
            for d in arq_livros.ler():
                if d.get("id") > maior:
                    maior = d.get("id")

            novo_livro = {
                "id": maior + 1,
                "disponivel": True,
                "titulo": request.form.get("titulo"),
                "autor": request.form.get("autor")
            }

            arq_livros.adicionar( novo_livro )

    return redirect( "/livros", code=302 )

#! Roda toda a aplicaçao
if __name__ == "__main__":
    app.run( host="0.0.0.0", port=3000, debug=True )