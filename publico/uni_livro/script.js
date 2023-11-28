const main = document.querySelector( "main" )

const url = window.location.href
const num = url.split("?")[1]
carregar_livro()

async function carregar_livro() {
	const response = await fetch( `/ler_livros?id=${num}` )
	const txt = await response.text()

	try {
		const data = JSON.parse( txt )

		document.querySelector("title").textContent = `Livro - ${data.titulo}`

		document.getElementById("in_titulo").innerHTML = `${data.titulo}`
		document.getElementById("in_autor").innerText = data.autor
		document.getElementById("in_imagem").src = data.imagem
		document.getElementById("in_descricao").textContent = data.descricao

		if ( data.status == "disponível" ) {
			document.getElementById("in_but_empres").textContent = 'Agendar'
			document.getElementById("in_but_empres").href = `/agendar?id=${data.id}`
		} else {
			document.getElementById("in_but_empres").textContent = data.status
		}
	} catch {
		document.body.innerHTML = txt
	}

}