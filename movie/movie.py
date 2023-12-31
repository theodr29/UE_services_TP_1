from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = "0.0.0.0"

with open("{}/databases/movies.json".format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=["GET"])
def home():
    """Defines the home route of our api"""

    return make_response(
        "<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200
    )


@app.route("/template", methods=["GET"])
def template():
    """Example of route that uses an HTML template"""

    return make_response(
        render_template(
            "index.html", body_text="This is my HTML template for Movie service"
        ),
        200,
    )


@app.route("/json", methods=["GET"])
def get_json():
    """Route that returns the list of all the movies"""

    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieid>", methods=["GET"])
def get_movie_byid(movieid):
    """Route that returns the movie corresponding to movieid"""

    # We check for each movie if the id corresponds to movie id
    # We return th movie wwhen we find it
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res

    # If we don't find it we return an error
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/movies/directors/<director>", methods=["GET"])
def get_movie_by_director(director):
    """Route that returns th list of the movies corresponding to a director"""

    movie_list = []

    # We check for each movie if the director corresponds to the director we want
    for movie in movies:
        if str(movie["director"]) == str(director):
            # We add the movie to the list
            movie_list.append(movie)

    # If we found at least one movie tha corresponds, we return the list
    if len(movie_list) > 0:
        res = make_response(jsonify(movie_list), 200)
        return res
    # else we return an error
    else:
        return make_response(jsonify({"error": "Unknown director"}), 400)


@app.route("/moviesbytitle", methods=["GET"])
def get_movie_bytitle():
    """Route that returns the movie corresponding to a title"""
    json = ""

    # We get the title from the request arguments
    if request.args:
        req = request.args

        # We compare it to the title of each movie in the data
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie
    # If we found the movie, we return it, else we return an error
    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/movies/<movieid>", methods=["POST"])
def create_movie(movieid):
    """Route that posts a new movie in the data"""

    # We get the data from the body of our request
    req = request.get_json()

    # We check if the movieid is not already used
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    # if not we add the movie to the data and return a sucess message
    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res


@app.route("/movies/<movieid>/<rate>", methods=["PUT"])
def update_movie_rating(movieid, rate):
    """Route that permits to update the rate of a movie"""

    # We search the movie in the data
    for movie in movies:
        if str(movieid) == str(movie["id"]):
            # If we found it, we update the rate and return the movie object
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res
    # else we return an error
    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


@app.route("/movies/<movieid>", methods=["DELETE"])
def del_movie(movieid):
    """Route that deletes a movie corresponding to movieid"""

    # We search the movie in the data
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # if we find the movie we remove it
            movies.remove(movie)
            return make_response(jsonify(movie), 200)
    # else we return a response
    res = make_response(jsonify({"error": "Movie ID not found"}), 400)
    return res


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
