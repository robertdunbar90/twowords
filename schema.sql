drop table if exists subject;
drop table if exists review;
create table subject (
  id integer primary key autoincrement,
  title text not null
);
create table review (
  id integer primary key autoincrement,
  subjectFk integer not null,
  reviewer text not null,
  review text not null,
  rating integer not null
);
