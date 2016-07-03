from flask import Flask, render_template, g, request, url_for, abort, redirect
import sqlite3 as lite
from pagination import pagination
from forms import SubjectForm, ReviewForm

PER_PAGE = 25

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
  return lite.connect(app.config['DATABASE'])

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/', defaults={'page':1})
@app.route('/reviews/<int:page>')
def home(page):
  count = count_pages()
  reviews = get_reviews_for_page(page)
  if not reviews and page != 1:
    abort(404)
  p = pagination(page, PER_PAGE, count)
  return render_template('reviews.html', pagination=p, reviews=reviews)

@app.route('/review/<int:subject>')
def review(subject):
  reviews = get_reviews_for_subject(subject)
  if not reviews:
    abort(404)
  title = reviews[0][0]
  return render_template('review.html', title=title, subject=subject, reviews=reviews)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
  form = SubjectForm()
  if request.method == 'GET':
    return render_template('add_subject.html', form=form)
  elif request.method == 'POST':
    subject = insert_subject(form.title.data, form.reviewer.data, form.review.data, form.rating.data)
    return redirect(url_for('review', subject=subject))

@app.route('/review/<int:subject>/add_review', methods=['GET', 'POST'])
def add_review(subject):
  form = ReviewForm()
  subject_title = get_title(subject)[0]
  if request.method == 'GET':
    return render_template('add_review.html', form=form, subject=subject, subject_title=subject_title)
  elif request.method == 'POST':
    insert_review(None, subject, form.reviewer.data, form.review.data, form.rating.data) 
    return redirect(url_for('review', subject=subject))

def count_pages():
  query = 'select count(*) from subject;'
  return g.db.execute(query).fetchone()[0]

def get_title(subject):
  query = 'select s.title from subject s where s.id = ?;'
  result = g.db.execute(query, (subject,)).fetchone()
  return result

def get_reviews_for_page(page):
  query = 'select s.id, s.title, count(r.id) from subject s, review r where r.subjectFk = s.id group by s.id order by s.title limit ? offset ?;'
  reviews = g.db.execute(query, (PER_PAGE, (page-1)*PER_PAGE)).fetchall()
  return reviews

def get_reviews_for_subject(subject):
  query = 'select s.title, r.reviewer, r.review, r.rating from subject s, review r where r.subjectFk = s.id and s.id = ?;'
  reviews = g.db.execute(query, (subject,)).fetchall()
  return reviews

def insert_review(cursor, subject_id, reviewer, review, rating):
  commit = False
  if cursor is None:
    cursor = g.db.cursor()
    commit = True
  query = 'insert into review (subjectFk, reviewer, review, rating) values (?, ?, ?, ?);'
  cursor.execute(query, (subject_id, reviewer, review, rating))
  if commit:
    g.db.commit()


def insert_subject(title, reviewer, review, rating):
  cursor = g.db.cursor()
  query = 'insert into subject (title) values (?);'
  cursor.execute(query, (title,))
  subject = cursor.lastrowid
  insert_review(cursor, subject, reviewer, review, rating)
  g.db.commit()
  return subject

if __name__ == '__main__':
  app.run(host='0.0.0.0')
