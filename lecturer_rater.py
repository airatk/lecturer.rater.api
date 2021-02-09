from hashlib import sha256

from flask import Flask
from flask import request
from flask import jsonify

from peewee import ModelSelect

from models.user import User
from models.rating import Rating

from utilities.helpers import setup_database_tables


setup_database_tables()

app: Flask = Flask(__name__)


@app.route("/sign-up", methods=[ "POST" ])
def sign_up():
    username: str = request.form.get("username", "")
    password: str = request.form.get("password", "")
    
    if password == "":
        return (jsonify({ "message": "Password cannot be empty string." }), 406)

    if User.select().where(User.username == username).exists():
        return (jsonify({ "message": "User with given username already exists." }), 409)

    token: str = sha256("-".join([ username, password ]).encode()).hexdigest()

    _ = User.create(username=username, password=password, token=token)

    return (jsonify({ "message": "User was successfully created.", "token": token }), 201)

@app.route("/sign-in", methods=[ "POST" ])
def sign_in():
    username: str = request.form.get("username", "")
    password: str = request.form.get("password", "")

    possible_users: ModelSelect = User.select().where(User.username == username)

    if not possible_users.exists():
        return (jsonify({ "message": "User with given credentials doesn't exist." }), 406)
    
    possible_users: ModelSelect = possible_users.select().where(User.password == password)
    
    if not possible_users.exists():
        return (jsonify({ "message": "Password is incorrect." }), 406)

    authorised_user: User = possible_users[0]

    return (jsonify({ "message": "User was successfully authorised.", "token": authorised_user.token }), 200)


@app.route("/ratings", methods=[ "GET" ])
def ratings():
    ratings: ModelSelect = Rating.select().order_by(Rating.id.desc())

    if "lecturer" in request.args:
        ratings = ratings.where(Rating.lecturer ** request.args["lecturer"])

    return (
        jsonify({ "message": "Ratings were successfully fetched.", "ratings": [ {
            "id": str(rating.id),
            "user_id": str(rating.user_id),
            "lecturer": str(rating.lecturer),
            "value": str(rating.value),
            "text": str(rating.text)
        } for rating in ratings ] }),
        200
    )


@app.route("/my-ratings", methods=[ "POST" ])
def my_ratings():
    token: str = request.form.get("token", "")

    possible_users: ModelSelect = User.select().where(User.token == token)

    if not possible_users.exists():
        return (jsonify({ "message": "User is not authorised." }), 401)

    authorised_user: User = possible_users[0]

    ratings: ModelSelect = Rating.select().where(Rating.user_id == authorised_user.id).order_by(Rating.id.desc())

    return (
        jsonify({ "message": "User's ratings were successfully fetched.", "ratings": [ {
            "id": str(rating.id),
            "user_id": str(rating.user_id),
            "lecturer": str(rating.lecturer),
            "value": str(rating.value),
            "text": str(rating.text)
        } for rating in ratings ] }),
        200
    )

@app.route("/create-rating", methods=[ "POST" ])
def create_rating():
    token: str = request.form.get("token", "")

    possible_users: ModelSelect = User.select().where(User.token == token)

    if not possible_users.exists():
        return (jsonify({ "message": "User is not authorised." }), 401)

    authorised_user: User = possible_users[0]

    rating_lecturer: str = request.form.get("lecturer", "")
    rating_value: str = request.form.get("value", "")
    rating_text: str = request.form.get("text", "")

    if rating_lecturer == "":
        return (jsonify({ "message": "Lecturer's rating should have lecturer's name." }), 401)

    if rating_value not in map(str, range(1, 6)):
        return (jsonify({ "message": "Rating value should be between 1 and 6 inclusively." }), 401)
    
    _ = Rating.create(user_id=authorised_user.id, lecturer=rating_lecturer, value=int(rating_value), text=rating_text)

    return (jsonify({ "message": "New rating was created." }), 201)

@app.route("/remove-rating", methods=[ "POST" ])
def remove_rating():
    token: str = request.form.get("token", "")

    possible_users: ModelSelect = User.select().where(User.token == token)

    if not possible_users.exists():
        return (jsonify({ "message": "User is not authorised." }), 401)

    authorised_user: User = possible_users[0]

    possible_rating_id: str = request.form.get("rating-id", "")

    if not possible_rating_id.isdigit() or possible_rating_id < "1":
        return (jsonify({ "message": "Rating ID should be a number which is greater than 0." }), 400)

    rating_id: int = int(possible_rating_id)

    if not Rating.select().where(Rating.user_id == authorised_user.id, Rating.id == rating_id).exists():
        return (jsonify({ "message": "Rating was not found." }), 404)

    Rating.delete().where(Rating.user_id == authorised_user.id, Rating.id == rating_id).execute()

    return (jsonify({ "message": "Rating was successfully deleted." }), 200)
