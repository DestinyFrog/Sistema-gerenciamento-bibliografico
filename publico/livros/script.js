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
	data.forEach( (d) => {
		var emoji = "🟢"

		switch ( d.status ) {
			case "agendado":
			case "emprestado":
				emoji = "🔴"
				break
			case "indisponível":
				emoji = "⚪"
				break
		}

		const content = `
			<div class="card">
				<figure>
					<img onclick="window.location.href='/uni_livro/index.html?${d.id}'" src="${d.imagem}" alt="capa ${d.titulo}">
					<figcaption>${emoji} ${d.status}</figcaption>
				</figure>
				<p>${d.titulo} - <i>${d.autor}</i></p>
			</div>`

		main.innerHTML += content
	} );
}