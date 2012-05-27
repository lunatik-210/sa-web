
bin_path = './bin'
sacparse = bin_path + '/sacparse'
sacg2dot = bin_path + '/sacg2dot'
dot      = 'dot'

def execute(file, input):
	from subprocess import Popen, PIPE, STDOUT

	p = Popen(file, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	return p.communicate(input=input)[0]

def make_call_graph(filename):
	f = open(filename, 'r')
	stream = f.read()
	f.close()

	output = execute(sacparse, stream)
	output = execute(sacg2dot, output)
	output = execute([dot, '-Tsvg', '-o', 'out.svg'], output)

def send_email(to, name, file):
	import smtplib, os
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEBase import MIMEBase
	from email.MIMEText import MIMEText
	from email.Utils import COMMASPACE, formatdate
	from email import Encoders

	msg = MIMEMultipart()
	msg['Subject'] = 'Your task is processed'
	msg['From'] = 'poddy.org'
	msg['To'] = to

	msg.attach( MIMEText("Dear %s, thank you for using SourceAnalyzer Web!" % name) )
	msg.attach( MIMEText("See in attachment.") )

	part = MIMEBase('application', "octet-stream")
	
	f = open(file,"rb")
	part.set_payload( f.read() )
	f.close()

	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
	msg.attach(part)

	s = smtplib.SMTP('localhost')
	s.sendmail('poddy@poddy.org', [to], msg.as_string())
	s.quit()


def db_execute(handler, request):
	handler.execute(request)
	return handler.fetchall()

if __name__ == '__main__':
	import MySQLdb as mysql

	db = mysql.connect(host='localhost', user='saweb', passwd='passSaWeb')
	handler = db.cursor()

	db_execute(handler, 'use saweb')

	while True:
		results = db_execute(handler, 'SELECT requests.date, requests.id, requests.user_id, requests.source_path FROM requests LIMIT 0,1')
		if len(results) == 0:
			# have to sleep(1000) really
			break
		date_st, id, user_id, source_path = results[0]

		make_call_graph(source_path)
		
		handler.execute('DELETE FROM requests WHERE id = %s' % id)
		db.commit()

		results = db_execute(handler, 'SELECT users.email, users.name FROM users where users.id = %s' % user_id)
		if len(results) != 0:
			email, name = results[0]
			send_email(email, name, 'out.svg')

		print date_st
		print date_st.date()
		print datetime.fromtimestamp(date_st)

		handler.execute("INSERT into history (user_id, graph_path, resolution, request_id, date_st) VALUES(%s, '%s', '%s', %s, %s)"  % (user_id, './', 'done', id, datetime.fromtimestamp(date_st) ))
		db.commit()

		#just for testing
		break

	db.close()
