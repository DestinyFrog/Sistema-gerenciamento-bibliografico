from memoria import Arquivo
from datetime import date, timedelta

class Eventos:
	def __init__( self, arq_liv, aut ):
		self.livros = arq_liv
		self.usuarios = aut

		self.arquivo = Arquivo("./data/eventos.json")

	def completar_dado( self, data ):
		data["livro"] = self.livros.encontrar_um( "id", data.get("livro") )
		data["usuario"] = self.usuarios.base.encontrar_um( "id", data.get("usuario") )
		return data

	def ler( self ):
		data = self.arquivo.ler()

		for i in data:
			self.completar_dado( i )
		return data

	def encontrar_por_livro( self, livro ):
		livro["status"] = "disponível"

		for i in self.arquivo.ler():
			if livro.get("id") == i.get("livro"):
				livro["status"] = i.get("status")

	def agendar_emprestimo( self, id_livro, id_usuario ):  
		novo_empres = {
			"usuario": id_usuario,
			"livro": id_livro,
			"data_de_emprestimo": None,
			"data_de_devolucao": None,
			"status": "agendado"
		}

		self.arquivo.adicionar( novo_empres )

	def realizar_emprestimo( self, id ):
		hoje = date.today()
		emprestimo = hoje.strftime("%d/%m/%Y")
		devolucao = hoje + timedelta( days=7 )
		devolucao = devolucao.strftime("%d/%m/%Y")

		emp = self.arquivo.encontrar_um( "id", id )
		emp["data_de_emprestimo"] = emprestimo
		emp["data_de_devolucao"] = devolucao
		emp["status"] = "emprestado"

	def excluir_evento( self, id ):
		self.arquivo.remover( id )