from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = "0.0.0.0"

# We read the data from the bookings.json file
with open("{}/databases/bookings.json".format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=["GET"])
def home():
    """Defines the home route of our api"""

    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=["GET"])
def get_json():
    """Definition of the route that returns the list of all the bookings"""

    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=["GET"])
def get_booking_for_user(userid):
    """Route that returns the bookings of the user corresponding to userid"""

    # We iterate on all the bookings to find the user we are
    # searching for and we return its bookings
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify(booking), 200)

    # If we don't find the user we return an error
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/bookings/users/<userid>", methods=["POST"])
def add_user(userid):
    """Route that posts a new user in the booking service"""

    # We check if the user we want to add already exists in the data
    # if yes we return an error
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 409)

    # else we add the new user
    user = {"userid": userid, "dates": []}
    bookings.append(user)
    return make_response(jsonify(user), 200)


@app.route("/bookings/<userid>", methods=["POST"])
def add_booking_byuser(userid):
    """Route that posts a new booking for the specified user"""

    # We get the data of the booking we want to add from the request
    req = request.get_json()

    for booking in bookings:
        # We check if the user exists
        if str(userid) == booking["userid"]:
            # We retriev the show data from the showtime service
            showtime_port = 3202
            showtimes = requests.get(
                f"http://showtime:{showtime_port}/showmovies/{req['date']}"
            )
            movies = showtimes.json()["movies"]

            # We check if the movie and the date of the new booking correspond to the data of the showtime servicce
            if movies and str(req["movieid"]) in movies:
                # Adding the new booking
                added = False
                # First checking if the user already has bookings on this date
                for date in booking["dates"]:
                    if date["date"] == req["date"]:
                        # Checking if the user already has a booking for this movie on this date
                        if req["movieid"] in date["movies"]:
                            return make_response(
                                jsonify({"error": "booking already exists"}), 409
                            )
                        # if not we add the new booking
                        added = True
                        date["movies"].append(req["movieid"])
                # If the date was never used, we add it to the user booking
                if added == False:
                    booking["dates"].append(
                        {"date": req["date"], "movies": [req["movieid"]]}
                    )

                return make_response(jsonify(booking), 200)
            else:
                return make_response(
                    jsonify({"error": "This booking already exists"}), 409
                )

    return make_response(jsonify({"error": "Userid not found"}), 409)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
