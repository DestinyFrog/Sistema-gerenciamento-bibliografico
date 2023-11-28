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
	if ( id == 0 ) {
		alert("Não é possível deletar o administrador principal")
		return
	}

	res = confirm( `Deseja deletar o usuario: ${titulo}` )

	if ( res == true )
		window.location.href = `/del_usuarios?id=${id}`
}

function editarDialog( i ) {
	editar_dialog.showModal()
	const d = dados[i]

	document.getElementById("inp_id").value = d.id
	document.getElementById("inp_usuario").value = d.usuario
	document.getElementById("inp_senha").value = d.senha
	document.getElementById("inp_admin").checked = d.admin
	document.getElementById("inp_email").value = d.email
}

function proc_livros() {

	var link = "/ler_usuarios"

	if ( inp_procura.value != "" )
		link = "/ler_usuarios?proc=" + inp_procura.value

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
			<td>${d.usuario}</td>
			<td>${d.senha}</td>
			<td>${d.email}</td>
			<td>${d.admin}</td>
			<td>
				<img onclick="editarDialog(${idx})" width="20" src="https://cdn-icons-png.flaticon.com/512/700/700291.png" />
			</td>
			<td>
				<img onclick="deletar(${d.id},'${d.usuario}')" width="20" src="https://cdn-icons-png.flaticon.com/512/3096/3096673.png" alt="deletar" />
			</td>
		</tr>`
		lista_livros.innerHTML += el
	} )
}