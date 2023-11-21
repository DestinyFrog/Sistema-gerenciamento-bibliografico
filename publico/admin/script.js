
procurar_usuarios()
procurar_emprestimos()

async function procurar_usuarios() {
	const response = await fetch( "/usuarios" )
	const data_cru = await response.text()

	var data = undefined

	try {
		data = JSON.parse( data_cru )
	} catch {
		document.body.innerHTML = data_cru
		return
	}

	const el_usu = document.getElementById("lista-usuarios")

	data.forEach( d => {
		const el = `
		<tr>
			<td>${ d.usuario }</td>
			<td>${ d.senha }</td>
			<td>${ d.admin }</td>
		</tr>`

		el_usu.innerHTML += el
	} )
}

async function procurar_emprestimos() {
	const response = await fetch( "/eventos" )
	const data = await response.json()

	const el_usu = document.getElementById("lista-eventos")

	data.forEach( d => {
		var botao = ""

		switch( d.status ) {
			case "agendado":
				botao = `<td><a href="/emprestimo/${ d.id }">Emprestar</a></td>`
				break
			case "emprestado":
				botao = `<td><a href="/devolucao/${ d.id }">Devolver</a></td>`
				break
			case "atrasado":
				botao = `<td><a href="/emprestimo/${ d.id }">Notificar</a></td>`
				break
		}

		const el = `
		<tr>
			<td>${ d.id }</td>
			<td>${ d.data_de_emprestimo }</td>
			<td>${ d.data_de_devolucao }</td>
			<td>${ d.usuario?.usuario }</td>
			<td>${ d.livro.titulo }</td>
			<td>${ d.status }</td>
			${ botao }
		</tr>`

		el_usu.innerHTML += el
	} )
}