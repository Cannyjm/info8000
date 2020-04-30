### SEMESTER PROJECT
#### Weed detection
The project deals with detecting 13 types of weed (purple_nutsage, yellow_nutsage, pig_weed, goosegrass, crowfoot grass, crabgrass, texaspanicum, florida_beggaweed, florida_pusley, ivyleaf_moningglory, pitted_morningglory, sicklepod, smallflower_morningglory) in images. It uses API for acquiring and store new images (uploading), and detection of weeds.
The detection model used was YOLOv3. The training was done under darknet YOLO framework

#### File:
* **test_app.py** : Script for the PROJECT
* **Model file** : Since its size is bigger than github upload limit, it can be downloaded at http://104.198.216.197/downloads

* **predict.html** : HTML rendering of prediction page
* **upload.html** : HTML rendering of upload page
* **obj.names** : Contain names of weeds (used as a reference to name weeds on bounding boxes)
* **obj.cfg** : Configuration file for training, testing, and detection
* **tempdb.db** : Sqlite3 database
* **Sample weed images** : Folder containing sample images that can be used to test the model



* **Data Acquisition and storage**
Weed images are collected and saved in the the server using the API.
### URLs for the API
* The server address is: http://104.198.216.197/upload

* **Weed detection**
You can upload an image with weeds inside, and the model will indicate the types of weeds from the weed classes above by drawing a bounding box around the weed.
### URLs for the API
* The server address is: http://104.198.216.197/detect

* **Training process**
I had about 1600 labelled images for the 13 classes of weeds, Using CLoDSA augmentation library I was able to increase the labelled images to 47,7760.
This dataset was divided into training(80%) and testing(20%). Training was done using YOLOv3 darknet environment on the training dataset while validating with the testing dataset.

* **Model Evaluation**
Running the model against the testing dataset (about 10,000 images), at a 0.5 detecting threshold, using NVDIA GTX 2080 gpu:

* **calculation mAP (mean average precision)**

Number of images = 9552

detections_count = 11916, unique_truth_count = 10346  

class_id = 0, name = purple_nutsage, ap = 90.42%   	 (TP = 373, FP = 6)

class_id = 1, name = yellow_nutsage, ap = 93.32%   	 (TP = 331, FP = 10)

class_id = 2, name = pig_weed, ap = 93.31%   	 (TP = 1153, FP = 52)

class_id = 3, name = goosegrass, ap = 93.73%   	 (TP = 631, FP = 1)

class_id = 4, name = crowfootgrass, ap = 95.75%   	 (TP = 533, FP = 2)

class_id = 5, name = crabgrass, ap = 94.23%   	 (TP = 1010, FP = 5)

class_id = 6, name = texaspanicum, ap = 93.45%   	 (TP = 876, FP = 18)

class_id = 7, name = florida_beggaweed, ap = 94.56%   	 (TP = 869, FP = 10)

class_id = 8, name = florida_pusley, ap = 93.07%   	 (TP = 648, FP = 6)

class_id = 9, name = ivyleaf_morningglory, ap = 93.43%   	 (TP = 980, FP = 21)

class_id = 10, name = pitted_morningglory, ap = 94.98%   	 (TP = 653, FP = 18)

class_id = 11, name = sicklepod, ap = 94.88%   	 (TP = 581, FP = 11)

class_id = 12, name = smallflower_morningglory, ap = 94.43%   	 (TP = 864, FP = 27)


for conf_thresh = 0.50, precision = 0.98, recall = 0.92, F1-score = 0.95

for conf_thresh = 0.50, TP = 9502, FP = 187, FN = 844, average IoU = 83.26 %

IoU threshold = 50 %, used Area-Under-Curve for each unique Recall

mean average precision (mAP@0.50) = 0.938125, or 93.81 %

Total Detection Time: 128.000000 Seconds



## INFO8000_Assignment 5

#### File:
* **Assignment5_INFO8000.ipynb** : The notebook for assignment 5

## INFO8000 Assignment 4

#### Files:
* **INFO8000_Assignment4.ipynb** : The notebook file for assignment 4



## INFO8000 Assignment 3

#### Files:

* **test_app.py** : the main Flask application with all the paths

* **dbsetup.py** : code used to create and populate the database

* **render.html** : html file used by the main application to render database results

### URLs for the API

* The server address is: http://104.198.216.197

* **Main Link (/):**

A GET link Where you can change the values of parameters in the url, gives out a json formated text. (Changeable parameters - name, city, state, institution, status)


Examples:

http://104.198.216.197/?name=Anord&city=Savannah

http://104.198.216.197/?name=Grace&city=Atlanta&state=Georgia&status=Instructor


* **A GET link (/get) to get data from database**

The data about owners and workers in the field is queried from the database and the output is the resulting json formatted text


Examples:

http://104.198.216.197/get




* **A POST link (/datapost) where you can post to the database.**

This is protected by the **API key = '8e64c48b-8920-4b56-9477-1ddb96ced8db'**. You can see a list the current cities in the database, and if you include your API key in your url you can add another cities in the database.

If submission is successfull you get a json result with status of your submission and all the cities in the database (including the one you submitted)

Examples:

With API key

http://104.198.216.197/datapost?key=8e64c48b-8920-4b56-9477-1ddb96ced8db


Without API key

http://104.198.216.197/datapost

**Note:** without the key you get a json with failure status when trying to post


* **A POST link (/post) where you add new crops to the database**

The POST process is also protected by the API key. This has an html rendering of the current crops in the database. You can add another crop and see the html result immediately

Without the API key you can only view, not post.

Examples:

With API key

http://104.198.216.197/post?key=8e64c48b-8920-4b56-9477-1ddb96ced8db

Without API key

<<<<<<< HEAD
http://104.198.216.197/post
=======
http://104.198.216.197/post
>>>>>>> f92dd9e55193263a0904782747b5385c6b8fb7ea
