from flask_wtf import Form
from wtforms import TextField, SubmitField

class SubjectForm(Form):
  title = TextField("Subject")
  reviewer = TextField("Reviewer")
  review = TextField("Review")
  rating = TextField("Rating")
  submit = SubmitField("Add review")

class ReviewForm(Form):
  reviewer = TextField("Reviewer")
  review = TextField("Review")
  rating = TextField("Rating")
  submit = SubmitField("Add review")
