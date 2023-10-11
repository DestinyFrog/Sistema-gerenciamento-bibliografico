
def generator( con ):
    yield 1
    if con == True:
        yield 2
    yield 3

gen = generator( True )

print( next( gen ) )
print( next( gen ) )
print( next( gen ) )

gen2 = generator( False )

print( next( gen2 ) )
print( next( gen2 ) )
print( next( gen2 ) )