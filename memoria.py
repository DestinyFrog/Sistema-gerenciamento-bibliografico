from unidecode import unidecode
from copy import deepcopy
import json

class Arquivo:

	# Método Construtor
	def __init__( self, caminho ):
		with open(caminho,'r') as arquivo:
			data = json.loads( arquivo.read() )
		self._pasta = data

	# Le um arquivo como JSON para dicionario/lista python
	def ler( self ):
		return deepcopy( self._pasta )

	# Adicionar dicionarios ao arquivo
	def adicionar( self, add_pasta: dict ):
		self._pasta.append( add_pasta )

	# encontrar o maior ID
	def maior_id( self ):
		data = self._pasta
		maior_id = 0
		for d in data:
			if d.get("id") > maior_id:
				maior_id = d.get("id")
		return maior_id

	# encontrar um unico livro pelo valor exato de um atributo
	def encontrar_um( self, chave:str, valor ):
		data = self._pasta
		for d in data:
			if d.get(chave) == valor:
				return d
		return None

	# encontrar varios livros pelo valor exato de um atributo
	def encontrar_varios( self, chave:str, valor ):
		data = self._pasta
		similares = []
		for d in data:
			if d.get(chave) == valor:
				similares.append( d )
		return similares

	# encontrar varios livros por um valor "similar/contido em" de um atributo
	# ignora acentos e letras maiusculas
	def encontrar_similares( self, chaves:list, procurar_por:str ):
		similares = []
		dado_tratado = unidecode( procurar_por.lower() )

		for arquivo in self._pasta:
			for chave in chaves:
				if type( arquivo.get( chave ) ) is list :
					for elem in arquivo.get( chave ):
						elem_tratado = unidecode( elem.lower() )

						if dado_tratado in elem_tratado:
							similares.append( arquivo )
							break
				else:
					chave_tratado = unidecode( arquivo.get( chave ).lower() )

					if dado_tratado in chave_tratado:
						similares.append( arquivo )
						break
		return similares

	def adicionar( self, novos_dados ):
		novos_dados["id"] = self.maior_id()+1
		self._pasta.append( novos_dados )

	def remover( self, id ):
		for idx,v in enumerate( self._pasta ):
			if v.get("id") == id:
				self._pasta.pop( idx )
				break

	def editar( self, chave_para_alterar:str, valor_para_alterar, valor_para_procurar, chave_para_procurar="id" ):
		for d in self._pasta:
			if d.get(chave_para_procurar) == valor_para_procurar:
				d[chave_para_alterar] = valor_para_alterar
				break