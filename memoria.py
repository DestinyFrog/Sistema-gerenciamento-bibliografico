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

	# encontrar o maior ID
	def maior_id( self ):
		data = self.ler()
		maior_id = data[0].get("id")
		for d in data:
			if d.get("id") > maior_id:
				maior_id = d.get("id")
		return maior_id

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

	def editar( self, chave_para_alterar:str, valor_para_alterar, valor_para_procurar, chave_para_procurar="id" ):
		data = self.ler()
		for d in data:
			if d.get(chave_para_procurar) == valor_para_procurar:
				d[ chave_para_alterar ] = valor_para_alterar
				break

		self.escrever( data )