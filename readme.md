# Project 4 - Movie-App

##### What does it do and what need does it fulfil?
This project uses skills learnt to build a Flask Website that uses a Mongo backend. It is for people to view recipes, register as users and create, update and delete their own recipes. Users can also search for recipes that contain for the searched word in its tags, title or ingredients. The project can be viewed [https://.herokuapp.com/](https://.herokuapp.com/)

##### Functionality of project
The Website is fully responsive and uses Mongo DB to hold users collection and a movie-app collection. The user is able to register and login and view movies. Logged in users are able to Create, update (edit) and delete their own movies. Any user (logged in or not) can search for movies using the search box. A user can also log out.   

The movies page shows all movies in order of the amount of views each movie has. The movies are paginated.  This pagination is done the proper way, that is by the database. I have not done it the easy/wrong way which is to use jQuery as if there was 5,000 recipes it would load all of them in one time and would not be fast and affect the user-experience. 
  
Each movie on the recipes page can be clicked onto and that will load the single movie page which shows the entire entry. If the user created the recipe on this page they will be able to edit and delete the movie. 

The add movie allows the logged in user to create a movie and enter it onto the database.

##### Technologies Used

- Python
- HTML5
- CSS / Bootstrap 4
- JS / JQuery
- Mongo
- Flask

##### Deployment

Website was coded in PyCharm, a local GIT directory was used for version control and then uploaded to GITHUB. 

A MongoDB database was used and setup inside Heroku.The details of the database connection are found inside the requirements.txt - it uses the os class environ method to point Heroku to its own config variable (MONGOBD_URI) in order to keep the production database connection string secret.

A Procfile is also used to help Heroku know what commands are run by the application's dynos and how to run various pieces of the app including the starting point app.py

Heroku's deployment from Github repository function was used to deploy. On first deployment I forgot the Procfile so locally installed the Heroku CLI in order to read the deployment logs. This, along with Google, helped me realise I forgot to add the Procfile.  

Upon the app running I then manually loaded the database using the 'add recipe' functionality.

##### Testing

My tests check the page loading as well as the business logic of the views. They are in the tests.py.

The index page and recipes page is tested that they loads correctly.

The registration page and logic are tested. I test for mismatched passwords, duplicate user names, as well as successful registration.

The login page is tested throughout my tests as a number of my test operations require a logged in user. 

The create movie page is tested by checking that a movie is entered, the page redirects and the new movie is present on the index page.

The movies to movie page is tested by searching for any movies on the movie page, getting its id number and going to that recipe details page and checking the contents are there.  

The update movie page is tested by going to a logged in users edit movie page and changing some data and committing it. This the redirects the user to teh index page and that it tested that the information has changed on that movie. 
  
The delete recipe page is tested by going to it's recipe detail page and deleting it, then checking the redirect has happened and that the recipe does not appear on the index page.

It is impossible to test at 100% coverage so I followed the Pareto principle (80/20 rule) which I believe I achieved. All of my testing is done in the tests.py.

I concentrated on logic and functionality with the project, I have no desire to be a designer! That said I kept my design to be usable and simple to navigate with readable font faces and breathable spacing (i.e. negative space).  

As the site is built with a responsive design it works for mobiles and I have checked it on iPhones 6 to X, Samsung Galaxys, iPads (mini to pro), Google's Pixel 2 and 3. I also tested it on various browsers. 
