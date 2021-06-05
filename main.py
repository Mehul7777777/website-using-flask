from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import Column, Integer, String, Boolean

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# Cafe Database
class Cafe(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    map_url = Column(String(500), nullable=False)
    img_url = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    seats = Column(String(250), nullable=False)
    has_toilet = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    coffee_price = Column(String(250), nullable=True)

    def __init__(self, name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price):
        self.name = name
        self.map_url = map_url
        self.img_url = img_url
        self.location = location
        self.seats = seats
        self.has_toilet = has_toilet
        self.has_wifi = has_wifi
        self.has_sockets = has_sockets
        self.can_take_calls = can_take_calls
        self.coffee_price = coffee_price

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# To get all cafes on page
@app.route("/")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    cafes = []
    for cafe in all_cafes:
        cafes.append(cafe.to_dict())
    return render_template("index.html", cafes=cafes)


# Form to add details
@app.route('/add_detail')
def add_details():
    return render_template("add.html")


# To add details in database from form
@app.route('/add_cafe', methods=['POST'])
def add_cafe():
    cafe = Cafe(
        request.form['Cafe Name'],
        request.form['Map Url'],
        request.form['Image Url'],
        request.form['Location'],
        request.form['Seats'],
        bool(request.form['Has Toilet']),
        bool(request.form['Has WiFi']),
        bool(request.form['Has Sockets']),
        bool(request.form['Can Take Calls']),
        request.form['Coffee Price']
    )
    db.session.add(cafe)
    db.session.commit()
    return redirect(url_for('get_all_cafes'))


# To delete data from database
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete_cafe(id):
    cafe_to_delete = Cafe.query.get(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_cafes'))


if __name__ == '__main__':
    app.run(debug=True)