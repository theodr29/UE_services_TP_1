from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route('/bookings', methods=['GET'])
def get_json():
   res = make_response(jsonify(bookings), 200)
   return res

@app.route('/bookings/<userid>', methods=["GET"])
def get_booking_for_user(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         return make_response(jsonify(booking), 200)
      
   return make_response(jsonify({"error":"User not found"}), 400)

@app.route('/bookings/<userid>', methods=["POST"])
def add_booking_byuser(userid):
   req = request.get_json()

   for booking in bookings:
      if str(userid) == booking["userid"]:

         # Retrieving shows data
         showtime_port = 3202
         showtimes = requests.get(f"http://showtime:{showtime_port}/showmovies/{req['date']}")
         movies = showtimes.json()['movies']

         if movies and str(req["movieid"]) in movies:

            # Adding the new booking
            added = False
            # First checking if the date is not already in use for the user
            for date in booking["dates"]:
               if date["date"] == req["date"]:
                  if req["movieid"] in date["movies"]:
                     return make_response(jsonify({"error": "booking already exists"}),409)
                  added = True
                  date["movies"].append(req["movieid"])
            # If the date was never used, we add it to the user booking
            if (added == False):
               booking["dates"].append({"date": req["date"], "movies": [req["movieid"]]})
            

            return make_response(jsonify(booking), 200)
         else:
            return make_response(jsonify({"error":"This booking does not exists"}), 409)
         
   return make_response(jsonify({"error":"Userid not found"}), 409)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
