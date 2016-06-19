import requests
import HTMLParser

p = HTMLParser.HTMLParser()

site = 'http://twowordreviews.herokuapp.com'

page = '/items?page='
item = '/items/'

def get_text(text, delim):
  length = len(delim) + 2
  a = text.find('<' + delim + '>')
  b = text.find('</' + delim + '>')
  return text[a+length:b].strip()

def get_links(pagenumber):
  r = requests.get(site + page + str(pagenumber))
  table = get_text(r.text, 'table')
  links = get_links_list(table)
  return links

def get_links_list(text):
  tag = '<a href="/items/'
  length = len(tag)
  links = []
  i = text.find(tag)
  while i >= 0:
    j = text.find('"', i + length)
    links.append(int(text[i + length:j]))
    i = text.find(tag, i + length)
  return links


def iterate_tags(text, tags):
  values = []
  i = 0
  while i >= 0:
    value = get_text(text[i:], tags)
    values.append(value)
    i = text.find('<' + tags, i+1)
  return values

def get_page(number):
  r = requests.get(site + item + str(number))
  title = get_text(r.text, 'strong')
  page = [p.unescape(title)]
  table = get_text(r.text, 'table')
  rows = iterate_tags(table, 'tr')
  for row in rows[1:]:
    ds = iterate_tags(row, 'td')
    for d in ds[:-1]:
      page.append(p.unescape(d))
  return '###'.join(page)


f = open('data', 'w')

links = []

for i in range(1, 8):
  links += get_links(i)

for link in links:
  string = get_page(link) + '\n'
  f.write(string.encode('utf8', 'replace'))

f.close()
