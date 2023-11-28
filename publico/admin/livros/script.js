const inp_procura = document.getElementById("inp-procura")
const lista_livros = document.getElementById("lista-livros")
const editar_dialog = document.getElementById("editar-box")

var dados = undefined

fetch( "/souadmin" )
.then( resp => resp.text() )
.then( d => {
	if ( d == "" ) {
		inp_procura.value = ""
		inp_procura.onchange = proc_livros
		proc_livros()
	} else {
		document.body.innerHTML = d
	}
} )

function deletar( id, titulo ) {
	res = confirm( `Deseja deletar o livro: ${titulo}` )

	if ( res == true )
		window.location.href = `/del_livros?id=${id}`
}

function editarDialog( i ) {
	editar_dialog.showModal()
	const d = dados[i]

	document.getElementById("inp_id").value = d.id
	document.getElementById("inp_titulo").value = d.titulo
	document.getElementById("inp_autor").value = d.autor
	document.getElementById("inp_imagem").value = d.imagem
	document.getElementById("inp_generos").value = d.generos.join("\n")
}

function proc_livros() {

	var link = "/ler_livros"

	if ( inp_procura.value != "" )
		link = "/ler_livros?proc=" + inp_procura.value

	fetch( link )
	.then( resp => resp.text() )
	.then( data_cru => {

		try {
			dados = JSON.parse( data_cru )
			desenharTabela()
		} catch {
			document.body.innerHTML = data_cru
		}

	} )
}

function desenharTabela() {
	lista_livros.innerHTML = ""
	dados.forEach( (d,idx) => {
		const el = `<tr>
			<td>${d.id}</td>
			<td><img class="capa" src="${d.imagem}" alt="capa ${d.titulo}"></td>
			<td>${d.titulo}</td>
			<td>${d.autor}</td>
			<td>
				<img onclick="editarDialog(${idx})" width="20" src="https://cdn-icons-png.flaticon.com/512/700/700291.png" />
			</td>
			<td>
				<img onclick="deletar(${d.id},'${d.titulo}')" width="20" src="https://cdn-icons-png.flaticon.com/512/3096/3096673.png" alt="deletar" />
			</td>
		</tr>`
		lista_livros.innerHTML += el
	} )
}