import cx_Oracle

try:
	con = cx_Oracle.connect('') # The example had this 'tiger/scott@localhost:1521/xe'

except cx_Oracle.DatabaseError as er:
	print('There is an error in the Oracle database:', er)

else:
	try:
		cur = con.cursor()

		# fetchall() is used to fetch all records from result set
		cur.execute('select * from walks')
		rows = cur.fetchall()
		print(rows)

	except cx_Oracle.DatabaseError as er:
		print('There is an error in the Oracle database:', er)

	except Exception as er:
		print('Error:'+str(er))

	finally:
		if cur:
			cur.close()

finally:
	if con:
		con.close()
