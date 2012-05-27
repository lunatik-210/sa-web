from subprocess import Popen, PIPE, STDOUT
import MySQLdb as mysql

bin_path = './bin'
sacparse = bin_path + '/sacparse'
sacg2dot = bin_path + '/sacg2dot'
dot      = 'dot'

def execute(file, input):
	p = Popen(file, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	return p.communicate(input=input)[0]

def make_call_graph(filename):
	f = open(filename, 'r')
	stream = f.read()
	f.close()

	output = execute(sacparse, stream)
	output = execute(sacg2dot, output)
	output = execute([dot, '-Tsvg', '-o', 'out.svg'], output)

if __name__ == '__main__':
	db = mysql.connect(host='localhost', user='root', passwd='rfkmrekznjh')
	handler = db.cursor()
	handler.execute('use sa')

	while True:
		handler.execute('SELECT * FROM queue LIMIT 0,1')
		results = handler.fetchall()
		if len(results) == 0:
			break
		make_call_graph(results[0][3])
		print results[0][0]
		handler.execute('DELETE FROM queue WHERE id = %s' % results[0][0])
		db.commit()
		break

	db.close()
