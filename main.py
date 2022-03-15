from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Length

import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(), Length(min=5, max=30)])
    location = StringField('Location url link eg: google map location link', validators=[DataRequired(), URL()])
    open_time = StringField("Open Time", validators=[DataRequired()])
    closing_time = StringField("Closing Time eg: 8AM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating eg: 8PM", validators=[DataRequired()],
                                choices=['☕', '☕' * 2, '☕' * 3, '☕' * 4, '☕' * 5, '✘'])
    wifi_rating = SelectField("Wifi Rating", validators=[DataRequired()],
                              choices=['💪', '💪' * 2, '💪' * 3, '💪' * 4, '💪' * 5, '✘'])
    power_outlet_rating = SelectField("Power Outlet Rating", validators=[DataRequired()],
                                      choices=['🔌', '🔌' * 2, '🔌' * 3, '🔌' * 4, '🔌' * 5, '✘'])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    data_row = []
    if request.method == "POST":
        if form.validate_on_submit():
            for index, data in enumerate(form.data):
                if index == 7:
                    break
                else:
                    data_row.append(form.data.get(data))
            with open('cafe-data.csv', 'a', encoding='UTF8', newline="\n") as f:
                writer = csv.writer(f)
                writer.writerow(data_row)
            return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
