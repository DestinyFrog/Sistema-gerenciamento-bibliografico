import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from datetime import date
from fpdf import FPDF

class PDFer:
	def __init__( self ):
		self.origem = "pedro.calisto.sesisenaisp@gmail.com"
		self.senha = "usib cdvb jjtp rrij"
		pass

	def criarEmail( self, tema:str, destino:str, conteudo:str ):
		msg = MIMEMultipart()
		msg['Subject'] = tema
		msg['From'] = "Biblioteca SENAI"
		msg['To'] = destino
		msg.attach(MIMEText(conteudo, 'plain'))
		return msg

	def enviarEmail( self, mensagem ):
		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
			smtp.login( self.origem, self.senha )
			smtp.send_message( mensagem )

	def AnexarArquivo( self, nomeArquivo, msg:MIMEMultipart ):
		part = MIMEBase('application', 'octet-stream')
		with open( "doc.pdf", "rb" ) as file:
			part.set_payload( file.read() )

		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % nomeArquivo )
		msg.attach(part)

	def ComprovanteAgendamento( self, livro, usuario, evento ):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font('Courier', 'B', 12)

		intros = [
			"SENAI - SP",
			"Recibo de Agendamento",
			f"Usuário:{usuario.get('id')} - {usuario.get('usuario')}",
			"",
			f"{livro.get('id')} - {livro.get('titulo')}",
			# "Número de chamada: 821(81) A994c 2012/8.Ed.",
			"",
			"Normal",
			f"Agendado em: { evento.get('data-inicial') }",
			# f"Emprestado em: { evento.get('data-inicial') }",
			# f"Devolver até: { evento.get('data-final') }",
			# "Devolvido em: 08/11/2023 11:51:32",
			f"{evento.get('id')}",
			"",
			f"Impresso em: { date.today().strftime('%d/%m/%Y') }",
		]

		[ pdf.cell(40, 10, txt, ln=1 ) for txt in intros ]
		pdf.output('doc.pdf', 'F')

	def ComprovanteEmprestimo( self, livro, usuario, evento ):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font('Courier', 'B', 12)

		intros = [
			"SENAI - SP",
			"Recibo de Empréstimo",
			f"Usuário:{usuario.get('id')} - {usuario.get('usuario')}",
			"",
			f"{livro.get('id')} - {livro.get('titulo')}",
			# "Número de chamada: 821(81) A994c 2012/8.Ed.",
			"",
			"Normal",
			f"Emprestado em: { evento.get('data-inicial') }",
			f"Devolver até: { evento.get('data-final') }",
			# "Devolvido em: 08/11/2023 11:51:32",
			f"{evento.get('id')}",
			"",
			f"Impresso em: { date.today().strftime('%d/%m/%Y') }",
		]

		[ pdf.cell(40, 10, txt, ln=1 ) for txt in intros ]
		pdf.output('doc.pdf', 'F')

	def ComprovanteDevolucao( self, livro, usuario, evento ):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font('Courier', 'B', 12)

		intros = [
			"SENAI - SP",
			"Recibo de Devolução",
			f"Usuário:{usuario.get('id')} - {usuario.get('usuario')}",
			"",
			f"{livro.get('id')} - {livro.get('titulo')}",
			# "Número de chamada: 821(81) A994c 2012/8.Ed.",
			"",
			"Normal",
			f"Emprestado em: { evento.get('data-inicial') }",
			f"Devolver até: { evento.get('data-final') }",
			f"Devolvido em: { date.today().strftime('%d/%m/%Y') }",
			f"{evento.get('id')}",
			"",
			f"Impresso em: { date.today().strftime('%d/%m/%Y') }",
		]

		[ pdf.cell(40, 10, txt, ln=1 ) for txt in intros ]
		pdf.output('doc.pdf', 'F')

	def RelatorioLivros( self, livros ):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font('Courier', 'B', 12)

		intros = []
		espacos = [ 24, 20, 12, 6 ]

		txt = ""
		for idx, campo in enumerate( [ "TÍTULO", "AUTOR", "STATUS", "ACESSOS" ] ):
			txt += campo + ( " " * ( espacos[idx] - len( campo ) ) )
		pdf.cell(w=0, h=7, txt=txt, ln=1, border='B' )

		for livro in livros:
			txt = ""

			campos = [ livro.get("titulo"), livro.get("autor"), livro.get("status"), str( livro.get("acessos") ) ]

			for idx, campo in enumerate( campos ):
				if len( campo ) >= espacos[idx]:
					campo = campo[: espacos[idx] - 4 ] + "..."
				txt += campo + ( " " * ( espacos[idx] - len( campo ) ) )

			intros.append( txt )

		[ pdf.cell(w=0, h=7, txt=txt, ln=1, border='B' ) for txt in intros ]

		pdf.output( "doc.pdf", 'F' )