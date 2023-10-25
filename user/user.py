from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import time
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = "0.0.0.0"

# we get the data from the users.json file
with open("{}/databases/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=["GET"])
def home():
    """Defines the home route of the api"""
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=["GET"])
def get_users():
    """Route that returns the list of all the users"""
    return make_response(jsonify(users))


@app.route("/users/<userid>", methods=["GET"])
def get_user_by_id(userid):
    """Route that returns the user corresponding to userid"""

    # We search the user in all users
    for user in users:
        if str(user["id"]) == str(userid):
            # if we find the user we return it
            return make_response(jsonify(user))
    # else we return an error
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>/movies", methods=["GET"])
def get_user_movies_by_id(userid):
    """Route that returns the list of the movies booked by a user"""

    # we get the list of the bookings of the user with the booking service
    req_bookings = requests.get(f"http://booking:3201/bookings/{userid}")
    bookings = req_bookings.json()
    if req_bookings.status_code == 400:
        return make_response(jsonify(bookings), 400)

    movies = []
    # for each movie id in the bookings, we get the data of the movie from the movie service
    for date in bookings["dates"]:
        for movie in date["movies"]:
            req_movie = requests.get(f"http://movie:3200/movies/{movie}")
            if req_movie.status_code == 200:
                movies.append(req_movie.json())
    # We return the movies that we found
    return make_response(jsonify(movies), 200)


@app.route("/users/<userid>", methods=["POST"])
def add_user(userid):
    """Route tht posts a new user"""

    # We check if the user doesn't already exists
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User already exists"}), 400)

    # If not we add the new user to the data
    user = request.json
    user["id"] = userid
    user["last_active"] = int(time.time())
    users.append(request.json)

    # Before rendering the response, we need to add the user to the booking service
    booking_port = 3201
    requests.post(f"http://booking:{booking_port}/bookings/users/{userid}")

    # We return the new user
    return make_response(jsonify(request.json), 200)


@app.route("/users/editLastUpdated/<userid>", methods=["PUT"])
def edit_lastupdated(userid):
    """Route that updates the last_active field to the current timestamp"""

    # We search the user we want to update
    for user in users:
        if str(user["id"]) == str(userid):
            # If we find it, we update the last_active field and returns the user
            user["last_active"] = int(time.time())
            return make_response(jsonify(user), 200)
    # else we return an error
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>", methods=["DELETE"])
def delete_user(userid):
    """Route that delete the user corresponding to userid"""

    # We search the user
    for user in users:
        if str(user["id"]) == str(userid):
            # If we find it, we remove it from the data and returns it
            users.remove(user)
            return make_response(jsonify(user), 200)
    # else we return an error
    return make_response(jsonify({"error": "User not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
