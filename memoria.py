from unidecode import unidecode
import json

class Arquivo:

	# Método Construtor
	def __init__( self, caminho ):
		self.arquivo_caminho = caminho

	# Reescreve um arquivo em dicionario/lista python para JSON
	def escrever( self, data:dict ):
		data_arquivo = open( self.arquivo_caminho, "w" )
		texto = json.dumps( data )
		data_arquivo.write( texto )
		data_arquivo.close()

	# Le um arquivo como JSON para dicionario/lista python
	def ler( self ):
		data_arquivo = open( self.arquivo_caminho, "r" )
		texto = data_arquivo.read()
		data_arquivo.close()
		data = json.loads( texto )
		return data

	# Adicionar dicionarios ao arquivo
	def adicionar( self, add_data: dict ):
		data = self.ler()
		data.append( add_data )
		self.escrever( data )

	# encontrar um unico livro pelo valor exato de um atributo
	def encontrar_um( self, chave:str, valor ):
		data = self.ler()
		for d in data:
			if d.get(chave) == valor:
				return d
		return None

	# encontrar varios livros pelo valor exato de um atributo
	def encontrar_varios( self, chave:str, valor ):
		data = self.ler()
		valores = []
		for d in data:
			if d.get(chave) == valor:
				valores.append( d )
		return valores

	# encontrar varios livros por um valor "similar/contido em" de um atributo
	# ignora acentos e letras maiusculas
	def encontrar_similares( self, chaves:list, procurar_por:str ):
		data = self.ler()
		valores = []

		for c in chaves:
			for d in data:
				dado_tratado = unidecode( procurar_por.lower() )
				chave_tratado = unidecode( d.get( c ).lower() )

				if dado_tratado in chave_tratado:
					valores.append( d )
		return valores