#Shelters for puppies
This is a webapp written in python with the flask framework. It provides a system to manage a number of puppy shelters!

###Features
 - Puppy 'profiles'
 - reccomendation on alternate shelters


###Instructions
####Bower Modules
The project uses Bootstrap, jQuery and a few other modules for the clientside UI. These can be downloaded via bower by running 

~~~python
$ bower install
~~~
 or manually from this [link](http://google.com).
The downloaded modules need to be extracted to the **/static** directory.

####Other dependencies####
 - Flask
 - SQLite
 - WTForms extension

These need to be installed on the server before running **main.py**