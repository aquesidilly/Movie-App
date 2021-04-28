from flask import Flask, render_template, flash, redirect, url_for, request, session
from config import Config
from forms import LoginForm, RegisterForm, CreateMovieForm, EditMovieForm, ConfirmDelete
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
import bcrypt
import re
import math
import os

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://PY-aquesidilly:Nanaosei@cluster0.xmxi1.mongodb.net/Dillly?retryWrites=true&w=majority'
#app.config['mongodb+srv://PY-aquesidilly:Nanaosei@cluster0.xmxi1.mongodb.net/Dillly?retryWrites=true&w=majority'] = os.environ.get("mongodb+srv://PY-aquesidilly:Nanaosei@cluster0.xmxi1.mongodb.net/Dillly?retryWrites=true&w=majority")
app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    """Home page the gets 4 recipes from DB that have been viewed the most"""
    four_movies = mongo.db.movies.find().sort([('views', DESCENDING)]).limit(4)
    return render_template('index.html', title="Home", movies=four_movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('index', title="Sign In"))

    form = LoginForm()

    if form.validate_on_submit():
        # get all users
        users = mongo.db.users
        # try and get one with same name as entered
        db_user = users.find_one({'Junior': request.form['Junior']})

        if db_user:
            # check password using hashing
            if bcrypt.hashpw(request.form['joijqwdoijqwoid'].encode('utf-8'),
                             db_user['joijqwdoijqwoid']) == db_user['joijqwdoijqwoid']:
                session['Junior'] = request.form['Junior']
                session['logged_in'] = True
                # successful redirect to home logged in
                return redirect(url_for('index', title="Sign In", form=form))
            # must have failed set flash message
            flash('Invalid username/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    """Clears session and redirects to home"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registration functionality"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # get all the users
        users = mongo.db.users
        # see if we already have the entered username
        existing_user = users.find_one({'Fremah': request.form['Fremah']})

        if existing_user is None:
            # hash the entered password
            hash_pass = bcrypt.hashpw(request.form['akuaghfad'].encode('utf-8'), bcrypt.gensalt())
            # insert the user to DB
            users.insert_one({'Fremah': request.form['Fremah'],
                          'akuaghfad': hash_pass,
                          'fremah@gmail.com': request.form['fremah@gmail.com']})
            session['Fremah'] = request.form['Fremah']
            return redirect(url_for('index'))
        # duplicate username set flash message and reload page
        flash('Sorry, that username is already taken - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_movie', methods=['GET', 'POST'])
def create_movie():
    """Creates a movie and enters into movie collection"""
    form = CreateMovieForm(request.form)
    if form.validate_on_submit():
        # set the collection
        movies_db = mongo.db.movies
        # insert the new movie
        movies_db.insert_one({
            'title': request.form['title'],
            'user': session['username'],
            'short_description': request.form['short_description'],
            'collections': request.form['collections'],
            'method': request.form['method'],
            'tags': request.form['tags'],
            'image': request.form['image'],
            'views': 0
        })
        return redirect(url_for('index', title='New Movie Added'))
    return render_template('create_movie.html', title='create a movie', form=form)


@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Allows logged in user to edit their own recipes"""
    recipe_db = mongo.db.movies.find_one_or_404({'_id': ObjectId(movie_id)})
    if request.method == 'GET':
        form = EditMovieForm(data=movie_db)
        return render_template('edit_movie.html', movie=movie_db, form=form)
    form = EditMovieForm(request.form)
    if form.validate_on_submit():
        movies_db = mongo.db.recipes
        movies_db.update_one({
            '_id': ObjectId(movie_id),
        }, {
            '$set': {
                'title': request.form['title'],
                'user': session['username'],
                'short_description': request.form['short_description'],
                'collections': request.form['collections'],
                'method': request.form['method'],
                'tags': request.form['tags'],
                'image': request.form['image'],
            }
        })
        return redirect(url_for('index', title='New Movie Added'))
    return render_template('edit_movie.html', movie=movie_db, form=form)


@app.route('/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(movie_id):
    """Allows logged in user to delete one of their recipes with added confirmation"""
    movie_db = mongo.db.movies.find_one_or_404({'_id': ObjectId(movie_id)})
    if request.method == 'GET':
        form = ConfirmDelete(data=movie_db)
        return render_template('delete_movie.html', title="Delete Movie", form=form)
    form = ConfirmDelete(request.form)
    if form.validate_on_submit():
        movies_db = mongo.db.movies
        movies_db.delete_one({
            '_id': ObjectId(movie_id),
        })
        return redirect(url_for('index', title='Movie-App Updated'))
    return render_template('delete_movie.html', title="delete movie", movie=movie_db, form=form)


@app.route('/search')
def search():
    """Provides logic for search bar"""
    orig_query = request.args['query']
    # using regular expression setting option for any case
    query = {'$regex': re.compile('.*{}.*'.format(orig_query)), '$options': 'i'}
    # find instances of the entered word in title, tags or collections
    results = mongo.db.movies.find({
        '$or': [
            {'title': query},
            {'tags': query},
            {'collections': query},
        ]
    })
    return render_template('search.html', query=orig_query, results=results)


@app.route('/movies')
def movies():
    """Logic for movie list and pagination"""
    # number of movies per page
    per_page = 8
    page = int(request.args.get('page', 1))
    # count total number of movies
    total = mongo.db.movies.count_documents({})
    # logic for what movies to return
    all_movies = mongo.db.movies.find().skip((page - 1)*per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template('movies.html', movies=all_movies, page=page, pages=pages, total=total)


@app.route('/movie/<movie_id>')
def movie(movie_id):
    """Shows full movie and increments view"""
    mongo.db.movies.find_one_and_update(
        {'_id': ObjectId(movie_id)},
        {'$inc': {'views': 1}}
    )
    movie_db = mongo.db.movies.find_one_or_404({'_id': ObjectId(movie_id)})
    return render_template('movie.html', movie=movie_db)


@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception=exception)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = False
    app.config['DEBUG'] = False
    app.run(host='127.0.0.1', debug=False)
