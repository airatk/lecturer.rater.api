# Lecturer Rater API
_web app API to manage ratings written by students about their lecturers_

### Stack
* Python, flask
* PostgreSQL, peewee

## Features
* `/ratings` - returns ratings given by all the registered students.
* `/my-ratings` - return ratings written by currently authorised student.
* `/sign-up` - registers new user using provided username & password, and returns authorised user token.
* `/sign-in` - authorises user using provided username & password, and returns authorised user token.
* `/creating-rating` - creates new rating record in database using provided token of an authorised user.
* `/remove-rating` - removes existing rating record from database using provided token of an authorised user & rating id of the rating for removal.
