# Traditional Herbs 

Traditional Herbs is a website that encourages the use of some simple yet effective
 herbs to cure some mild infections or mild pains 

#### As a user l want 

* to know what each herb cures 

* to know how to prepaire the herbs

* to know the effectiveness rating of the herbs 

* to read reviews about the herbs 

* to add my own herbs

* to edit my own herbs

* to delete my own herbs

* to add a picture of the herb 

* to see the images of what the herb looks like 

### Features

* Navigation bar - A link that takes you to home page 

* My Herbs - A link that takes you to page that displays all herbs in the data base

* Add Herbs - A link that takes you to page that display a form to fill about your herb information

* Log in - A link that takes you to page that display a form were a user fill in about their registered information

* Log out - A link that takes takes the user out of session and direct the user to the log in page 

* Sign up - A link that takes you to a page that display a form for a user register to fill in their information 

### Future Features

* A rating feature will be put on after a user add a reviews

* An add video feature wiill be added were a user who know moe about any herbs will upload 

* Herbs with most rating will appear first on featured herbs 

### Wireframes

[https://github.com/chasakara/Traditional-Herbs/blob/master/static/herbsimages/wireframes] Wireframes

### Technologies Used 

[https://www.gitpod.io/] - an online IDE for developing this project.

#### Front End

[https://developer.mozilla.org/en-US/docs/Web/HTML] - to build the foundation of the project.

[https://developer.mozilla.org/en-US/docs/Web/CSS] - to create custom styles.

#### Back End

[https://www.python.org/] - back-end programming language used in this project.

[https://flask.palletsprojects.com/en/1.1.x/] - microframework for building and rendering pages.

[https://www.mongodb.com/] -  NoSQL database for storing back-end data.

[https://jquery.com/] - to simplify DOM manipulation

[https://developer.mozilla.org/en-US/docs/Web/JavaScript] - to create and control dynamic website content

[https://pymongo.readthedocs.io/en/stable/] - for Python to get access the MongoDB database.

[https://www.heroku.com/] - to host the project.

#### Libraries 

[https://fonts.google.com/] (to import font).

[https://fontawesome.com/] - to provide icons used across the project.

[https://getbootstrap.com/] - Is a framework to help you design websites faster and easier. It includes HTML and CSS based design templates

# Testing

### Validation Services

HTML Placeholder tag not allowed when the input type is time - Placeholder removed All other errors are from Jinja not being reconised in the validator

CSS No Errors Found

JavaScript No Errors found

Python No Errors found

### Manual Testing

Logo:
The logo is working as expected, when clicked it will take you to the home page

All herbs:
The all herbs link is working as expected, when clicked it will take you to the page displaying all herbs in data base

My Herbs:
The my herbs link is working as expected, when clicked it will take the user to the page with his/her herbs he/she have created 

Add herb:
The add herb link is working as expected, when clicked it will take you to the page were the user will add a herb 

Delete herb:
The delete herb button is working as expected, when clicked it will delete the useer's herb 

Edit herb:
The edit herb button is working as expected, when clicked it will take the user to the herb to edit it

Add review:
The add review button is working as expected, when clicked it will take the user to a page to add a review for that particular herb


Log in:
Log in is working as expected, when clicked it will take the user to a log in page

Log out:
Log out is working as expected, when clicked it log out the user from that current session 

Sign up:
Sign up linnk is working as expected, when click it will take the user to a sign up page 


### Problems encountered

* The images of the herbs could not aling well on smaller screens  

* The add review future was not adding the review to the actuall herb it was added to 

* The code to display 8 on 8 herbs cards on page was not working 

* The diffult herb images that has to be displayed if a user does not add the herb image was not working displaying 

## Compatibility and Responsiveness

This website had been being tested during the development across multiple browsers (Chrome, Safary, Opera, FireFox, Internet Explorer) and on multiple devices: mobile (iPhone 5, 6, 8, Samsung Galaxy 8, 9, ), tabletsand laptops (with HiDPI and MDPI and touch screens).
As well as on Google Chrome's developer tools to see how it looks across all the different device screen sizes to ensure compatibility and responsiveness.
I also used Am I Responsive online tool for checking responsiveness on different devices.
Plenty of changes were made and necessary media queries added to make the website fully responsive.
The one issue was found that website renders poorly on Internet Explorer browser (as it is outdated). However, the website renders well as expected on the other browsers.

# Deployed on Heroku at { website URL HERE Traditional Herbs].

* Clone the repository by copying the clone url

* In the terminal type git clone followed by the      copied url cd into Traditional Herbs

* In the terminal type pip3 install -r requirements.txt to install all the dependencies

* Create an account on Heroku if you don't have one yet and create a new app

* In the terminal, type echo "web: python herbapp.py" > Procfile

* Create a new folder inside the apps directory called secret_settings and in it a .env file or change path in 
app_setup.py and create the .env file anywhere you'd like

* In the .env file set DBNAME, URI and SECRET_KEY

* In the terminal, heroku login

* git init to create a new repository

* heroku git:remote -a Traditional-Herbs

* git add .

* git commit -m "Initial commit"

* git push heroku master

* heroku ps:scale web=1

* In your heroku app navigate to settings and reveal config vars, set IP = 0.0.0.0, PORT = 5000, DBNAME, URI and SECRET_KEY

* restart all dynos and open your heroku app

## Local


This project can be ran locally by going to this Repository link and clicking on the Clone or Download button and copying the link provided.

In your IDE, open a Terminal window and change to the directory where you want to clone this project and type Git clone "your copied link".

After pressing Enter the project will be created and cloned locally.

Alternatively you can download the zipped file, decompress it and use your IDE of choice to access it.

Github Repo: 

# Credits

### Media

The photos used on the home page were taken from google 

### Acknowdgements

Precious_Mentor, mentor.

code-institute-room.slack.com.

#### This website is for educational purpose only 

