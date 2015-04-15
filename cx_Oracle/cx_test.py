#!/usr/bin/python

import sys
sys.path.append('/unibss/tstusers/tstchc01/jiawh/python/cx_Oracle-5.1.3/samples');
import cx_Oracle  
def connectDB(str):
	conn = cx_Oracle.connect('uatchusg1c/uatchusg1c@devl10g2_10.1.251.177')
	return conn
def getCursor(conn):
	cursor = conn.cursor()  
	return cursor

def query(cursor):
# method 1
	named_paras = {'fs':1623318, 'ti':'11400172'}
	cursor.execute("""select file_sn, thread_id, src_id 
		from LOG_FTS_PROV where file_sn > :fs and thread_id<:ti 
		order by file_sn""", named_paras)  
# method 2
	cursor.execute("""select file_sn, thread_id, src_id 
		from LOG_FTS_PROV where file_sn > :fs and thread_id<:ti 
		order by file_sn""", fs=1623318, ti='11400172')  
# method 3
	cursor.execute("""select file_sn, thread_id, src_id 
		from LOG_FTS_PROV where file_sn > :1 and thread_id<:2
		order by file_sn""", (1623318, '11400172'))
def prepare(cursor):
	cursor.prepare("""select file_sn, thread_id, src_id 
		from LOG_FTS_PROV where file_sn > :1 and thread_id<:2
		order by file_sn""")
	rows = cursor.execute(None, (1623318, '11400172'))

def fetchOne(cursor):
	while cursor.next():
		row = cursor.fetchone()  
		if row[0]:
			print row[0]  
def fetchAll(cursor):
	rows = cursor.fetchall()
	for row in rows:
		print(row)

conn = connectDB("") 
cursor = getCursor(conn)
prepare(cursor)
fetchAll(cursor)
cursor.close()  
conn.close() 
