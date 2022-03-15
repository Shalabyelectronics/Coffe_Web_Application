# Coffe_Web_Application
It's Another Flask Practice where we practice dealing with CSV files to update your table and display it on the page again.

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/57592040/158473688-02bb42ed-40ff-4f1a-91a2-f65df71c714a.gif)

## Install The requirements first:
`pip install -r requirements.txt`
This Flask Practice is part of [Angela course](https://www.udemy.com/course/100-days-of-code/)
So she provide a starter project file you can download it from [here](https://att-c.udemycdn.com/2021-11-09_15-04-03-c23d9b0fce104253993325bba7f3c6cd/original.zip?response-content-disposition=attachment%3B+filename%3DStarting%2BFiles%2B-%2Bcoffee-and-wifi.zip&Expires=1647395278&Signature=araXTjA7Ttp1DV4H2VDf5dJD6TXz9F~BFijhC2ipdJz7eG4oDNE0l7~DZ1vgI3SRvtzDuhylIK9FlnY9dV4eRPeqlcGnOQF~QtAAMcbU~l4cpF5mt6rvPimJnUwDXolhEAVc6Go2Q9oG23s3EAWM8rmgV8Bo0VtDv~F3MC0Swoj5qrKKWchixxDb0Um3yppmxWMXmxLGeDphxp-ozKOJKKxGS3jiQuCi0p4vjFdBcwPVRVIJufWgTX5p6tPThRjSJ6AVQ4~NVY0JX7RS5uSYNSG16CVZjNP9U5ptN90IOUuCAtdhoxYv8-uEYh3Ff0WxeE~eF3SUGgckoHwDgjA9iw__&Key-Pair-Id=APKAITJV77WS5ZT7262A)
## What we aiming to do?
### First Part is to use additional Css file with the Bootstrap Css and to do that without override of the bootstrap Css we need to use super() method inside the styles block like this
```html
{% block styles %}
{{super()}}
<link rel="stylesheet"
      href="{{url_for('static', filename='css/styles.css')}}">
{% endblock %}
```
### Second part was to add the data from the csv file to view it in cafes html page and I did it like this
```python
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)
```
and we need to edit our `cafes.html` as well like this:
```html
{% extends 'bootstrap/base.html' %}
{% block styles %}
{{super()}}
<link rel="stylesheet"
      href="{{url_for('static', filename='css/styles.css')}}">
{% endblock %}
{% block title %}Restaurants{% endblock %}
{% block content %}
<div class="container">
  <div class="row">
    <div class="col-sm-12">
      <h1>All Cafes</h1>
	  <table class="table table-hover table-dark">
          <tbody>
            <tr>
              <th scope="col">{{cafes[0][0]}}</th>
              <th scope="col">{{cafes[0][1]}}</th>
              <th scope="col">{{cafes[0][2]}}</th>
              <th scope="col">{{cafes[0][3]}}</th>
              <th scope="col">{{cafes[0][4]}}</th>
              <th scope="col">{{cafes[0][5]}}</th>
              <th scope="col">{{cafes[0][6]}}</th>
            </tr>
          {% for row in cafes[1:] %}
            <tr>
              <td>{{row[0]}}</td>
              <td><a href="{{row[1]}}", target="_blank">Maps Link</a> </td>
              <td>{{row[2]}}</td>
              <td>{{row[3]}}</td>
              <td>{{row[4]}}</td>
              <td>{{row[5]}}</td>
              <td>{{row[6]}}</td>
              <td>{{row[7]}}</td>
            </tr>
          {% endfor %}
          </tbody>
  	  </table>
      <p><a href="{{ url_for('home') }}">Return to index page</a></p>
    </div>
  </div>
</div>

{% endblock %}
```
I know I could do better than that but it is working just fine for now.. :)
### Thired we need to create our add form and to do that I used wtform , form_wtf and form class that will be inherited form FlaskForm like this:
```python
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
```
### Fourth we need to create our add route functionality:

and we will add our form object that we created from CafeForm class by using `{{ wtf.quick_form(form) }}` and to do so we need first to import the bootstrap wtf by this block of code `{% import "bootstrap/wtf.html" as wtf %}`
Now lets return to our add function and it will look like this 
```python
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
```
and I will explain this code first create a form object from our form class, then created data_row list where we will use it later to add it to our csv data file, Then I checked if the user
post the form by submited it if not it will render our add page with passing the form object normally.
then another check will start and it is if the form data is valid .
if so we will loop throw the form data object and it have a lot of data so instead to get each one I just used enumerate method and I checked that all I need is just first 7 elements
and as I didn't reach that final index I would append that data to our data_row.
#### finally we used context manager to open our csv file with append mode and add the data row on a new line in our csv file and when everythin done we will redirect the user to 
cafes.html page again 
## The End

I think I could do better in this part also but again it's working just fine .
