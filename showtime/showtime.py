from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=["GET"])
def get_showtimes():
   return make_response(jsonify(schedule), 200)

@app.route("/showmovies/<date>", methods=["GET"])
def get_schedule_by_date(date):
   for time in schedule:
      if str(date) == str(time["date"]):
         return make_response(jsonify(time), 200)
   return make_response("Schedule not found for this date", 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT, debug=True)
