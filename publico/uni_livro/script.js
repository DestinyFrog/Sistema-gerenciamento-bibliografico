const main = document.querySelector( "main" )

const url = window.location.href
const num = url.split("?")[1]
carregar_livro()

async function carregar_livro() {
	const response = await fetch( `/livros/id/${num}` )
	const txt = await response.text()

	try {
		const data = JSON.parse( txt )

        document.getElementById("in_titulo").innerText = data.titulo
        document.getElementById("in_autor").innerText = data.autor
        document.getElementById("in_autor").innerText = data.autor        
        document.getElementById("in_imagem").src = data.imagem

		if ( data.status == "disponível" ) {
			// main.innerHTML += `<a href="/agendar/${data.id}">Agendar Emprestimo</a>`
		} else {
			// main.innerHTML += `<p>${ data.status }</p>`
		}

		document.querySelector("title").textContent = `Livro - ${data.titulo}`
	} catch {
		document.body.innerHTML = txt
	}

}