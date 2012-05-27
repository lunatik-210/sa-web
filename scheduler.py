
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

def send_email(to, file):
	import smtplib
	from email.mime.image import MIMEImage
	from email.mime.multipart import MIMEMultipart
	
	msg = MIMEMultipart()
	msg['Subject'] = 'Your task is processed'
	msg['From'] = 'poddy.org'
	msg['To'] = to
    
    fp = open(file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

	s = smtplib.SMTP('localhost')
	s.sendmail('noreply@sourceanalyzer.org', [to], msg.as_string())
	s.quit()


if __name__ == '__main__':
	import MySQLdb as mysql

	db = mysql.connect(host='localhost', user='saweb', passwd='passSaWeb')
	handler = db.cursor()
	handler.execute('use saweb')

	while True:
		handler.execute('SELECT * FROM requests LIMIT 0,1')
		results = handler.fetchall()
		if len(results) == 0:
			break
		make_call_graph(results[0][2])
		handler.execute('DELETE FROM requests WHERE id = %s' % results[0][0])
		db.commit()

		send_email('andrew.d.lapin@gmail.com', 'out.svg')

		#just for testing
		break

	db.close()
