from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///coasters.db"

db = SQLAlchemy(app)

class Park(db.Model):
    park_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    address = db.Column(db.String(150), nullable = False)


class Ride(db.Model):
    ride_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    park_id = db.Column(
        db.Integer, db.ForeignKey("park.park_id"), nullable = False
    )
    park = db.relationship("Park", backref = "rides")

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)


class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.Text, nullable = False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), nullable = False
    )
    ride_id = db.Column(
        db.Integer, db.ForeignKey("ride.ride_id"), nullable = False
    )
    user = db.relationship("User", backref = "reviews")
    ride = db.relationship("Ride", backref = "reviews")

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name = "valid_rating"),
    )

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created.")

@app.route("/")
def helloWorld():
    return "Hello World!"

if __name__ == "__main__":
    app.run()