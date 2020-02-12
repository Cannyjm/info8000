from flask import Flask, escape,request,jsonify,redirect,render_template,url_for,abort
import sqlite3 as sql

app = Flask(__name__,template_folder='./')

#Example of an API key
appkey="8e64c48b-8920-4b56-9477-1ddb96ced8db"
key_presence='n'

#1. Normal GET request, you can change any of the values in the url
@app.route("/",methods=['GET'])
def profile():
    name=request.args.get("name","Canicius")
    city=request.args.get("city","Athens")
    state=request.args.get("state","Georgia")
    status=request.args.get("status","Student")
    institution=request.args.get("institution","University of Georgia")
    response={"profile":{"name":name,"city": city, "state":state},"status":{"status":"You are a "+status,"institution":institution}}
    return jsonify(response)

#Get field owners and workers from the database (A GET request from the database)
@app.route("/get",methods=['GET'])
def getDB():
    conn=sql.connect("tempdb.db")
    try:

        curr=conn.execute("""
        SELECT people.personId,people.name FROM people JOIN ownerField ON ownerField.personId=people.personId         GROUP BY people.name
        """)
        owners=curr.fetchall()
        curr2=conn.execute("""
        SELECT people.personId,people.name FROM people JOIN workerField ON      workerField.personId=people.personId GROUP BY people.name
        """)
        workers=curr2.fetchall()
        conn.commit()
    except sql.Error as e:
        return ("Database error: " + str(e))

    finally:
        conn.close()
    response={"Owners":{i[0] : i[1] for i in owners},"Workers":{i[0] : i[1] for i in workers}}
        
    return jsonify(response)

#POST to the database (add a city) and see your update as a json. (You can post without API key on URL)
@app.route('/datapost', methods=['GET', 'POST']) 
def datapost():
    if request.args.get('key') and request.args.get('key') == appkey:
        key_presence='y'
    else:
        key_presence='n'
    conn=sql.connect("tempdb.db")
    try:

        curr=conn.execute("""
        SELECT name FROM city
        """)
        cities=curr.fetchall()
        conn.commit()
    except sql.Error as e:
        return ("Database error: " + str(e))

    finally:
        conn.close()
    if request.method == 'POST':
        if key_presence=='y':
            addcity=escape(request.form['city'])
            conn=sql.connect("tempdb.db")
            try:

                conn.execute("""
                insert into city(name) values(?)
                """,(addcity,))
                conn.commit()
            except sql.Error as e:
                return ("Database error: " + str(e))

            finally:
                conn.close()

            conn=sql.connect("tempdb.db")
            try:

                curr=conn.execute("""
                SELECT cityId,name FROM city
                """)
                getcity=curr.fetchall()
                conn.commit()
            except sql.Error as e:
                resp2={"status":"Submission Failure"}
                return jsonify(resp2)

            finally:
                conn.close()
            resp={"status":"Successfully Submitted","cities_in_db":{i[0] : i[1] for i in getcity}}
            return jsonify(resp)
        else:
            resp2={"status":"Submission Failure API Key required"}
            return jsonify(resp2)
    
    return '''<div>Add a Georgia city in the Database:</div><br><form method="POST">
                  City: <input type="text" name="city"><br>
                  
                  <input type="submit" value="Submit"><br>
              </form><div>Current Cities in the Database: '''+str(cities)+'''</div>'''


#Testing the POST functionality to post to the database and view the result as normal html (Protected by API key on POST)
@app.route("/post",methods=['GET','POST'])
def postView():
    if request.args.get('key') and request.args.get('key') == appkey:
        key_presence='y'
    else:
        key_presence='n'

    if request.method=='GET':
        conn=sql.connect("tempdb.db")
        try:

            curr=conn.execute("""
            SELECT * FROM crop
            """)
            crops=curr.fetchall()
            conn.commit()
        except sql.Error as e:
            return ("Database error: " + str(e))

        finally:
            conn.close()
        return render_template('render.html',crops=crops)
    else:
        if key_presence=='y':
            addcrop=escape(request.form['crop'])
            conn=sql.connect("tempdb.db")
            try:

                conn.execute("""
                insert into crop(name) values(?)
                """,(addcrop,))
                conn.commit()
            except sql.Error as e:
                return ("Database error: " + str(e))

            finally:
                conn.close()
            return redirect('/post?key='+appkey)
        else:
            resp2={"status":"Submission Failure API Key required"}
            return jsonify(resp2)


