import sqlite3 as lite
import sys

rows = []

f = open('data', 'r')

i = 1
for line in f:
  p = line.strip().decode('utf8', 'replace').split('###')
  print p
  reviews = [[i, p[0]]]
  for j in range(1, len(p), 3):
    review = [i, p[j], p[j+1]]
    rating = p[j+2]
    review.append(int(rating.split('/')[0]))
    reviews.append(review)
  rows.append(reviews)
  i += 1

insert_subject = u'insert into subject (id, title) values (?, ?);'
insert_review = u'insert into review (subjectFk, reviewer, review, rating) values (?, ?, ?, ?);'

con = lite.connect('twowords.db')

with con:
  cur = con.cursor()

  for line in rows:
    print line
    subject = line[0]
    cur.execute(insert_subject, subject)
    for r in line[1:]:
      cur.execute(insert_review, r)
