import urllib.request, urllib.parse, urllib.error
import sqlite3
import ssl
import json
import hidden

#Ignore certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

service_url = 'https://maps.googleapis.com/maps/api/geocode/json'
secrets = hidden.oauth()
api_key = secrets['api_key']

if api_key is None:
    api_key = 42
    service_url = 'http://py4e-data.dr-chuck.net/json'

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS Locations')
cur.execute('''CREATE TABLE IF NOT EXISTS Locations(
                                            id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            name  TEXT UNIQUE,
                                            data  BLOB
               )''')
        
fname = 'where.data'    #Added extra Karaganda and Cherepovets at the end of a .data file for a sanity checking
fhandle = open(fname, 'r')
fhandle = [line.strip() for line in fhandle.readlines()]

count = 0
cnt_correct = 0
for loc_name in fhandle:
    cur.execute('SELECT id, name FROM Locations WHERE name = ?', (loc_name,))
    flag_val = cur.fetchone()
    if flag_val is not None:
        print(loc_name, 'is already in a database')
        print(flag_val)
        continue
    
    params = {'address': loc_name, 'key' : api_key}
    url = service_url + '?' + urllib.parse.urlencode(params)
    print(str(count+1)+') Retrieving', loc_name+'...')
    count = count + 1
    
    urlhandle = urllib.request.urlopen(url, context=ctx)
    data = urlhandle.read()
    
    try:
        js = json.loads(data)
    except:
        print('Syntactically bad json:\n'+data)
        js = None
    
    if (js is None) or ('status' not in js) or (js['status'] != 'OK'): 
        print('===FAILURE TO RETRIEVE===')
        print(data)
        continue
    
    #print(json.dumps(js, indent = 3))
    cur.execute('INSERT INTO Locations(name, data) VALUES ( ?, ? )', (loc_name, data))
    
    cnt_correct = cnt_correct + 1
    if count == 100:
        conn.commit()
        break

print(cnt_correct,'new locations has been retrieved and put in a database geodata.sqlite\nRestart to get more!')
conn.commit()
cur.close()
conn.close()