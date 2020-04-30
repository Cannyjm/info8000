from flask import Flask, flash,escape,request,jsonify,redirect,render_template,url_for,abort, make_response,session,send_from_directory
import sqlite3 as sql
from werkzeug.utils import secure_filename
import argparse
import cv2
import numpy as np
import os
import datetime

UPLOAD_FOLDER = 'upload'

##-- Allowed files to upload
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])
## --Checking if file is in allowed list
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
app = Flask(__name__,template_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = '8e64c48b-8920-4b56-9477-1ddb96ced8db'
app.secret_key = '8e64c48b-8920-4b56-9477-1ddb96ced8db'


## -- Weed Detection method (read the model and draw bounding boxes on weeds in image)
def detect(img_received):
    config='obj.cfg' #configuration file
    weights='obj_90000.weights' #The model
    names='obj.names' #Weed names

    CONF_THRESH, NMS_THRESH = 0.5, 0.5

    # Load the network
    net = cv2.dnn.readNetFromDarknet(config, weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Read and convert the image to blob and perform forward pass to get the bounding boxes with their confidence scores
    img = cv2.imread(img_received)
    height, width = img.shape[:2]

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))
    if(b_boxes !=[]): #if there is weed detection
        # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
        indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

        # Draw the filtered bounding boxes with their class to the image
        with open(names, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        #colors = np.random.uniform(0, 255, size=(len(classes), 3))

        for index in indices:
            x, y, w, h = b_boxes[index]
            box_coords = ((x+5, y), (x-5 + w, y+20))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), 2)
            cv2.rectangle(img, box_coords[0], box_coords[1], (255,255,255), cv2.FILLED)
            cv2.putText(img, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 2)
    return(img)
              

####-- WEED DETECTION ---###########################
        
@app.route("/detect",methods=['GET','POST'])
def detectView():
    if request.method=='GET':
        #Checking if weed detection was requested, so as to display the detected image
        conn=sql.connect("tempdb.db")
        try:
            curr=conn.execute("""
            SELECT id FROM status_img
            """)
            rw=curr.fetchall()
            conn.commit()
        except sql.Error as e:
            print ("Database error: " + str(e))

        finally:
            conn.close()
        if(rw[0][0]==1): #if the system detects weed
            conn=sql.connect("tempdb.db")
            try:
                curr=conn.execute("""
                UPDATE status_img set id=0
                """)
                conn.commit()
            except sql.Error as e:
                print ("Database error: " + str(e))

            finally:
                conn.close()
            #Display the detected image (every detected image is saved as detected.jpg, see below)
            response='detected.jpg'
            return render_template('predict.html',image=response)
        else:
            #if not requested, don't display anything
            response='default.png'
            return render_template('predict.html',image=response)
    else:
        #Post image to detect
        if 'image' not in request.files:
            flash('no image selected')
            return redirect('/detect')
        f = request.files['image']
        if f.filename == '':
            flash('no image selected')
            return redirect('/detect')
        if f and allowed_file(f.filename):
            f.filename='new_img.jpg'
            f.save('static/'+f.filename)
            filename='static/new_img.jpg'
            feedback=detect(filename) #Detect weeds in image
            #Save the detected image as detected.jpg
            res='static/detected.jpg' 
            cv2.imwrite(res,feedback)
            #set status of request to imply weed was detected
            conn=sql.connect("tempdb.db")
            try:
                curr=conn.execute("""
                UPDATE status_img set id=1
                """)
                conn.commit()
            except sql.Error as e:
                print ("Database error: " + str(e))

            finally:
                conn.close()
            return redirect('/detect')
        else:
            flash('File format not allowed')
            return redirect('/detect')
        
###--- UPLOADING IMAGES AND LABELS ----##
        
@app.route("/upload",methods=['GET','POST'])
def uploadImg():
    if request.method=='GET':
        #Get the web interface to upload files
        return render_template('upload.html')
    else:
        #If files are uploaded
        if 'files[]' not in request.files:
            flash('No file selected')
            return redirect('/upload')
        files = request.files.getlist('files[]')
        weed_type=escape(request.form['weed_type'])
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if filename.rsplit('.', 1)[1].lower() != 'txt':
                    uploadDate=datetime.datetime.now()
                    #Updating the database with the new images uploaded
                    conn=sql.connect("tempdb.db")
                    try:
                        conn.execute("""
                        insert into image_uploads values(null,?,?,?)
                        """,(filename,weed_type,uploadDate))
                        conn.commit()
                    except sql.Error as e:
                        return ("Database error: " + str(e))

                    finally:
                        conn.close()
            else:
                flash('File type not allowed')
                return redirect('/upload')   
        
        flash('File(s) successfully uploaded')
        return redirect('/upload')

###--- Downloading the model

@app.route("/downloads",methods=['GET'])
def get_file():
    return send_from_directory(UPLOAD_FOLDER, 'obj_90000.weights', as_attachment=True) 

    
    
    
     
    
    
 #######--- Rest of info8000 assignments -- ##
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