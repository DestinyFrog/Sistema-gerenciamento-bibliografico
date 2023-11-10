from unidecode import unidecode
import json

class Arquivo:

	# Método Construtor
	def __init__( self, caminho ):
		with open(caminho,'r') as arquivo:
			data = json.loads( arquivo.read() )
		self._livros = data

	# Le um arquivo como JSON para dicionario/lista python
	def ler( self ):
		return self._livros

	# Adicionar dicionarios ao arquivo
	def adicionar( self, add_data: dict ):
		self._livros.append( add_data )

	# encontrar o maior ID
	def maior_id( self ):
		data = self._livros
		maior_id = data[0].get("id")
		for d in data:
			if d.get("id") > maior_id:
				maior_id = d.get("id")
		return maior_id

	# encontrar um unico livro pelo valor exato de um atributo
	def encontrar_um( self, chave:str, valor ):
		data = self._livros
		for d in data:
			if d.get(chave) == valor:
				return d
		return None

	# encontrar varios livros pelo valor exato de um atributo
	def encontrar_varios( self, chave:str, valor ):
		data = self._livros
		valores = []
		for d in data:
			if d.get(chave) == valor:
				valores.append( d )
		return valores

	# encontrar varios livros por um valor "similar/contido em" de um atributo
	# ignora acentos e letras maiusculas
	def encontrar_similares( self, chaves:list, procurar_por:str ):
		valores = []

		for d in self._livros:
			for c in chaves:
				dado_tratado = unidecode( procurar_por.lower() )
				chave_tratado = unidecode( d.get( c ).lower() )

				if dado_tratado in chave_tratado:
					valores.append( d )
					break
		return valores

	def editar( self, chave_para_alterar:str, valor_para_alterar, valor_para_procurar, chave_para_procurar="id" ):
		for d in self._livros:
			if d.get(chave_para_procurar) == valor_para_procurar:
				d[chave_para_alterar] = valor_para_alterar
				break