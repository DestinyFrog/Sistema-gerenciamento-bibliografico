const main = document.querySelector( "main" )

const url = window.location.href
const num = url.split("?")[1]
carregar_livro()

async function carregar_livro() {
	const response = await fetch( `/livros/id/${num}` )
	const txt = await response.text()

	try {
		const data = JSON.parse( txt )

		main.innerHTML += `
		<img width="200px" src="${data.imagem}" alt="capa ${data.titulo}">
		<h1>${data.titulo} - ${data.autor}</h1>`

		document.querySelector("title").textContent = data.titulo
	} catch {
		document.body.innerHTML = txt
	}

}