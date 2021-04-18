from flask import Flask, render_template, request, redirect, url_for
from api import get_jokes
from flask_sqlalchemy import SQLAlchemy
import conf


app = Flask(__name__, static_url_path='/static')

#  browser will not cache static assets
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# prod heroku, dev localhost
ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = conf.DEV_URI
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = conf.PROD_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)


#  Model
class JokesModel(db.Model):
  __tablename__ = 'jokes'
  id = db.Column(db.Integer, primary_key=True)
  joke = db.Column(db.Text())
  name = db.Column(db.String(200))

  # Represent data 
  def __repr__(self):
     return f"<id={self.id}, joke={self.joke}, name={self.name}>"

  def __init__(self, joke, name):
    self.joke = joke
    self.name = name


# Call api, pass data, load page
@app.route('/')
def index():
  joke = get_jokes().json()['value']
  return render_template('index.html', joke = joke)


# post get joke from hidden input
@app.route('/post-joke', methods=['POST'])
def post_joke():
  if(request.method) == 'POST':
    joke = request.form['joke-input']
    name = request.form['name']

    # validate 
    if name == '':
      return render_template('index.html', message='Please enter your name', joke=joke)
    else:
      # save to db and display success
      data = JokesModel(joke, name)
      db.session.add(data)
      db.session.commit()
      return render_template('success.html', joke = joke, name=name)
    
# Get all Jokes 
@app.route('/saved', methods=['GET'])
def get_saved():
  db_jokes = JokesModel.query.all()
  return render_template('saved.html', jokes=db_jokes) 

# Delete Joke from db
@app.route('/delete/<id>')
def delete_joke(id):
  # find by id and delete joke
  saved_joke = JokesModel.query.filter_by(id=id).first()
  db.session.delete(saved_joke)
  db.session.commit()

  # Get db data 
  db_jokes = JokesModel.query.all()
  return render_template('saved.html', jokes=db_jokes) 
  # return redirect(url_for('/'))


if __name__ == '__main__':
  app.debug = True
  app.run()