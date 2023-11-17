const inp_proc = document.getElementById("inp_proc")
const main = document.querySelector("main")

inp_proc.value = ""
inp_proc.onchange = procurar
procurar()

async function procurar() {
	const val = inp_proc.value
	main.innerHTML = "<p>Loading ...</p>"

	var link = "/livros"

	if ( val !== "" )
		link = `/livros?proc=${inp_proc.value}`

	const response = await fetch( link )
	const txt = await response.text()

	try {
		const data = JSON.parse( txt )
		adicionarLivros( data )
	} catch {
		document.body.innerHTML = txt
	}
}

function adicionarLivros( data ) {
	main.innerHTML = ""
	data.forEach( ({id,imagem,titulo,autor,disponivel}) => {
		const content = `
			<div class="card">
				<img src="${imagem}" alt="capa ${titulo}">
				<p><a href="/uni_livro/index.html?${id}">${titulo}</a></p>
				<p>${autor}</p>
				<p>${disponivel  ? '✅' : '❌'}</p>
			</div>`

		main.innerHTML += content
	} );
}