create table  if not exists mainmenu (
id integer primary key autoincrement,
title text not null,
url text not null
);

create table  if not exists posts (
id integer primary key autoincrement,
name text not null,
post text not null,
url text not null,
time integer not null
);

