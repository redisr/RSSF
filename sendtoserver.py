import json
import urllib2
import psycopg2
from datetime import datetime

def getlocaldata():
	con = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='postgres')
	c = con.cursor()
	print 'conexao com banco local realizada'
	c.execute('select idsensor_fk, valor,timestamp,idamostra from amostra ORDER BY timestamp' )
	dados=c.fetchall()
	con.close()
	return dados

def date_handler(obj):
	return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def verificarerro():
	print "not implemented"

def senddata(jsonData):
	req = urllib2.Request('http://www.mdecarvalho.com/RSSF/scripts/setAmostra.php')
	req.add_header('Content-Type', 'application/json')
	try:
		response = urllib2.urlopen(req, json.dumps(jsonData, default=date_handler))
	except urllib2.HTTPError, e:
		print e.code
		exit()
	except urllib2.URLError, e:
		print e.args
		exit()
	string = response.read()
	if( string == ""):
		exit()
	else:
		if( len(json.loads( string )['errors']) > 0 ):
			con = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='postgres')
			c = con.cursor()
			print 'conexao com banco local realizada'
			c.execute("DELETE FROM amostra WHERE idamostra NOT IN "+ str(json.loads( string )['errors']).replace("[", "(").replace("]", ")"))
			dados=c.fetchall()
			con.close()
		else:
			con = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='postgres')
			c = con.cursor()
			print 'conexao com banco local realizada'
			c.execute("DELETE FROM amostra WHERE 1")
			dados=c.fetchall()
			con.close()
		c.execute(sql)

if __name__ == '__main__':
	print "get local data"
	dados = getlocaldata()
	print "send data server"
	senddata(dados)
	print "Done"
	

