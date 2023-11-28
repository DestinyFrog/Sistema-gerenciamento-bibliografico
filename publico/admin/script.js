
procurar_emprestimos()

async function procurar_emprestimos() {
	const response = await fetch( "/ler_eventos" )
	var data = await response.text()

	try {
		data = JSON.parse( data )
	} catch {
		document.body.innerHTML = data
	}

	const el_usu = document.getElementById("lista-eventos")

	data.forEach( d => {
		var botao = ""

		switch( d.status ) {
			case "agendado":
				botao = `<td><a href="/emprestar?id=${ d.id }">Emprestar</a></td>`
				break
			case "emprestado":
				botao = `<td><a href="/emprestar?id=${ d.id }">Devolver</a></td>`
				break
			case "atrasado":
				botao = `<td><a href="/emprestar?id=${ d.id }">Notificar</a></td>`
				break
		}

		var datas = `
		<td>${ d["data-inicial"] }</td>
		<td>${ d["data-final"] }</td>`

		if ( d["data-final"] == null ) {
			datas = '<td colspan="2" style="border: none;"></td>'
		}

		const el = `
		<tr>
			<td>${ d.id }</td>
			<td>${ d.status }</td>
			<td>${ d.usuario?.usuario }</td>
			<td>${ d.livro.titulo }</td>
			${ datas }
			${ botao }
		</tr>`

		el_usu.innerHTML += el
	} )
}