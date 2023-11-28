from unidecode import unidecode
from copy import deepcopy

class Sequelier():
	def __init__( self ):
		self.id_minimo = 0

	def campos( self, lista:list ):
		return dict.keys( lista[0] )

	def ler( self, lista:list ):
		return lista

	def encontrar_um( self, lista:list, valor, chaves=["id"] ):
		for i in lista:
			for chave in chaves:
				if i.get(chave) == valor:
					return i
		return None

	def encontrar_varios( self, lista:list, valor, chaves=["id"] ):
		nova_lista = []
		for i in lista:
			for chave in chaves:
				if i.get(chave) == valor:
					nova_lista.append( i )
					break
		return nova_lista

	def tratar_string( self, texto:str ):
		texto = texto.lower()
		texto = unidecode( texto )
		return texto

	def checar_similaridade( self, valor1, valor2:str ):
		if type(valor1) == str and type(valor2) == str:
			valor1 = self.tratar_string( valor1 )
			valor2 = self.tratar_string( valor2 )
			return valor2 in valor1 or valor1 in valor2
		elif type(valor1) == list and type(valor2) == str:
			for i in valor1:
				if self.checar_similaridade( i, valor2 ):
					return True
			return False

	def encontrar_similares( self, lista:list, valor, chaves=[] ):
		nova_lista = []

		for i in lista:
			for chave in chaves:
				if self.checar_similaridade( i.get(chave), valor ):
					nova_lista.append( i )
					break
		return nova_lista

	def maior_id( self, lista:list ):
		maior = self.id_minimo
		for i in lista:
			if i.get("id") > maior:
				maior = i.get("id")
		return maior

	def adicionar( self, lista:list, item:dict ):
		id = self.maior_id( lista ) + 1
		novo_item = item
		novo_item["id"] = id
		lista.append( novo_item )
		return novo_item

	def editar( self, lista:list, id:int, valor:dict ):
		item = self.encontrar_um( lista, id )

		for campo in valor.keys():
			if valor.get(campo) != None:
				item[campo] = valor.get(campo)
		return item

	def deletar( self, lista:list, id:int ):
		for idx,i in enumerate(lista):
			if i.get("id") == id:
				lista.pop( idx )

	def conectar( self, lista1:list, lista2:list, cabo ):
		nova_lista = self.copy( lista1 )
		for i in nova_lista:
			i[cabo] = self.copy( self.encontrar_um( lista2, i.get(cabo) ) )
		return nova_lista

	def copy( self, lista:list ):
		return deepcopy( lista )