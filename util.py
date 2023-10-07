import random
import string

# Gera ID aleatorio
def gerarID( length=9 ):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for _ in range(length))

for i in range( 10 ):
	print( gerarID() )