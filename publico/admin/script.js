
const main = document.getElementById("lista-livros")

async function procurar() {
	main.innerHTML = "<p>Loading ...</p>"

	const response = await fetch( "/todos-livros" )
	const data = await response.text()
	main.innerHTML = data
}

procurar()