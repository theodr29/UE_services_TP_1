from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import time
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = "0.0.0.0"

with open("{}/databases/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=["GET"])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=["GET"])
def get_users():
    return make_response(jsonify(users))


@app.route("/users/<userid>", methods=["GET"])
def get_user_by_id(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify(user))
    return make_response(jsonify({"error": "User not found"}), 400)

@app.route("/users/<userid>/movies", methods=["GET"])
def get_user_movies_by_id(userid):
    req_bookings = requests.get(f"http://booking:3201/bookings/{userid}")
    bookings = req_bookings.json()
    if (req_bookings.status_code == 400):
        return make_response(jsonify(bookings), 400)

    movies = []
    for date in bookings["dates"]:
        for movie in date["movies"]:
            req_movie = requests.get(f"http://movie:3200/movies/{movie}")
            if req_movie.status_code == 200:
                movies.append(req_movie.json())
    return make_response(jsonify(movies), 200)


@app.route("/users/<userid>", methods=["POST"])
def add_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User already exists"}), 400)
        
    # We confirmed that the user does not exist already
    user = request.json
    user["id"] = userid
    user['last_active'] = int(time.time())
    users.append(request.json)

    # Before rendering the response, we need to update the database of bookings
    booking_port = 3201
    requests.post(f"http://booking:{booking_port}/bookings/users/{userid}")

    return make_response(jsonify(request.json), 200)


@app.route("/users/editLastUpdated/<userid>", methods=["PUT"])
def edit_lastupdated(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            user["last_active"] = int(time.time())
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>", methods=["DELETE"])
def delete_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
