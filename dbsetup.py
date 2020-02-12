import sqlite3 as sql

#Creating tables in the database to track herbicide spray in the field
conn=sql.connect("tempdb.db")
try:
    conn.execute("""
    DROP TABLE IF EXISTS people
    """)
    conn.execute("""
    CREATE TABLE if not exists people (personId INT, name TEXT, phone TEXT, PRIMARY KEY ('personId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS city
    """)
    conn.execute("""
    CREATE TABLE if not exists city (cityId INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)
    """)
    conn.execute("""
    DROP TABLE IF EXISTS field
    """)
    conn.execute("""
    CREATE TABLE if not exists field (fieldId INT, name TEXT, cityId INT, PRIMARY KEY ('fieldId'),
    FOREIGN KEY ('cityId') REFERENCES city('cityId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS crop
    """)
    conn.execute("""
    CREATE TABLE if not exists crop (cropId INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT)
    """)
    conn.execute("""
    DROP TABLE IF EXISTS herbicide
    """)
    conn.execute("""
    CREATE TABLE if not exists herbicide (herbId INT, name TEXT, PRIMARY KEY ('herbId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS ownerField
    """)
    conn.execute("""
    CREATE TABLE if not exists ownerField (personId INT, fieldId INT, PRIMARY KEY ('personId','fieldId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS workerField
    """)
    conn.execute("""
    CREATE TABLE if not exists workerField (personId INT, fieldId INT, PRIMARY KEY ('personId','fieldId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS fieldCrop
    """)
    conn.execute("""
    CREATE TABLE if not exists fieldCrop (fieldId INT, cropId INT, PRIMARY KEY ('cropId','fieldId'))
    """)
    conn.execute("""
    DROP TABLE IF EXISTS spray
    """)
    conn.execute("""
    CREATE TABLE if not exists spray (id INTEGER PRIMARY KEY AUTOINCREMENT, herbId INT, fieldId INT, personId INT, sprayDate TEXT)
    """)
    
    conn.commit()
except sql.Error as e:
    print("Query error: " + str(e))
    
finally:
    conn.close()
    
#Populating the database

conn=sql.connect("tempdb.db")
try:
    conn.executemany("""
    insert into people values(?,?,?)
    """,[(1,'Edison Mai','0998844'),(2,'Bianca U','9887744'),(3,'Canny Jod','637733'),(4,'Eddie Y','97774'),(5,'John Magu','234555'),(6,'Ana John','96655'),(7,'Barry John','966551'),(8,'Deo Mon','396655'),(9,'Neo DAi','65944')])
    
    conn.executemany("""
    insert into city values(?,?)
    """,[(1,'Tifton'),(2,'Athens'),(3,'Madison'),(4,'Atlanta'),(5,'Auburn'),(6,'Fitzgerald'),(7,'Savanna')])
    
    conn.executemany("""
    insert into field values(?,?,?)
    """,[(1,'UG1',1),(2,'UG2',1),(3,'AT3',3),(4,'AGEE4',4),(5,'UG8',1),(6,'UG5',5),(7,'AT3',3),(8,'AGEE8',2),(9,'AGE56',7),(10,'RTY54',7),(11,'HGE7',6),(12,'THH',5),(13,'AGEE8',6)])
    
    conn.executemany("""
    insert into crop values(?,?)
    """,[(1,'Corn'),(2,'Beans'),(3,'Cotton'),(4,'Peanut'),(5,'Cabbage')])
    
    conn.executemany("""
    insert into herbicide values(?,?)
    """,[(1,'Clopyralid'),(2,'Dicamba'),(3,'Imazapic'),(4,'Hexazinone'),(5,'Duirun')])
    
    conn.executemany("""
    insert into ownerField values(?,?)
    """,[(1,2),(1,3),(1,4),(2,1),(3,2),(3,5),(3,8),(2,7),(2,6),(9,7),(9,8),(8,9),(7,10),(9,11),(7,12),(9,13)])
    
    conn.executemany("""
    insert into workerField values(?,?)
    """,[(4,2),(5,3),(6,4),(4,1),(5,2),(6,5),(4,8),(5,7),(6,6),(2,7),(2,6),(9,7),(9,8),(8,9),(7,10),(9,11),(7,12),(9,13)])
    
    conn.executemany("""
    insert into fieldCrop values(?,?)
    """,[(1,1),(2,1),(3,3),(4,2),(5,2),(6,4),(7,5),(8,3),(1,2),(9,5),(10,3),(11,3),(12,4),(13,5)])
    conn.executemany("""
    insert into spray values(?,?,?,?,?)
    """,[(1,1,2,2,'01-03-2020'),(2,1,3,2,'01-04-2020'),(3,1,4,2,'01-03-2020'),(4,1,6,2,'01-07-2020'),(5,2,13,4,'01-07-2020'),(6,3,11,9,'01-09-2020')])

    conn.commit()
except sql.Error as e:
    print("Query error: " + str(e))
    
finally:
    conn.close()
