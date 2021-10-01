import sqlite3
import json

fname = 'where.js'
fhandle = open(fname, 'w', encoding = 'utf-8')

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()
cur.execute('SELECT name, data FROM Locations')
data = [row[1].decode() for row in cur.fetchall()]
#print(data[0])

fhandle.write('myData = [\n')

count = 0

for json_str in data:
    js = json.loads(json_str)
    
    try:
        lat = js['results'][0]['geometry']['location']['lat'] 
        lng = js['results'][0]['geometry']['location']['lng'] 
        f_addr = js['results'][0]['formatted_address']
    except:
        print('Some data is missing')
        continue
    
    f_addr = f_addr.replace("\'",'')
    print(str(count+1)+')', '; '.join([str(lat),str(lng),f_addr]))
    
    if count == 0:
        s = '['+str(lat)+','+str(lng)+',\''+f_addr+'\']'
    else:
        s = ',\n'+'['+str(lat)+','+str(lng)+',\''+f_addr+'\']'
    
    #print(s)
    fhandle.write(s)
    count = count + 1

fhandle.write('\n];')
print(str(count),'records were written in a my_where.js file')
fhandle.close()

cur.close()
conn.close()