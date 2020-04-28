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
