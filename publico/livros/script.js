
const inp_proc = document.getElementById("inp_proc")
const main = document.querySelector("main")

inp_proc.value = ""

async function procurar() {
	const val = inp_proc.value
	
	main.innerHTML = "<p>Loading ...</p>"

	if ( val === "" ) {
		const response = await fetch( "/todos-livros" )
		const data = await response.text()
		main.innerHTML = data
		return
	}

	const link = `/todos-livros?proc=${val}`
	const response = await fetch( link )
	const data = await response.text()
	main.innerHTML = data
}

inp_proc.onchange = procurar
procurar()