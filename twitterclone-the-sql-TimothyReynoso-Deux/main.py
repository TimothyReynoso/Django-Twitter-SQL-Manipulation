#!/bin/env python

import sqlite3

import mimesis

from mimesis import Person

import random

person = Person('en')

print(person.full_name())

conn = sqlite3.connect('timothyreynoso.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS twitterusers
            (
            id INTEGER PRIMARY KEY,
            username VARCHAR(40) NOT NULL,
            password VARCHAR(250),
            displayname VARCHAR(50)
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS tweets
            (
            id INTEGER PRIMARY KEY,
            created_by VARCHAR(250),
            text VARCHAR(250),
            date_made DEFAULT CURRENT_TIMESTAMP
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS notifications
            (
            id INTEGER PRIMARY KEY,
            notified_by VARCHAR(250),
            notified VARCHAR(250),
            tweet_text VARCHAR(250),
            date_made DEFAULT CURRENT_TIMESTAMP
            );''')

for num in range(500):
    c.execute('''
                INSERT INTO twitterusers
                (username, password, displayname)
                VALUES
                (?,?,?);
                ''', (person.name(), person.password(), person.username()))

for num in range(1000):
    twitteruser = c.execute("SELECT username FROM twitterusers WHERE id=:1;", (random.randrange(1,500),))
    content = mimesis.Text()
    c.execute('''INSERT INTO tweets
                (created_by, text)
                VALUES
                (?,?)
                ''', (twitteruser.fetchone()[0], content.text(quantity=3),))

for num in range(200):
    namesoftweeters = [user[0] for user in c.execute("SELECT created_by FROM tweets;")]
    user_id_list = [_id[0] for _id in c.execute("SELECT id FROM twitterusers;").fetchall()]

    twitteruser = c.execute(
        "SELECT username FROM twitterusers WHERE username=:1;", (
            random.choice(namesoftweeters),)).fetchone()[0]

    twitteruser_notified = c.execute(
        "SELECT username FROM twitterusers WHERE id=:1;", (
            random.choice(user_id_list),)).fetchone()[0]

    if twitteruser and twitteruser_notified != '':
        tweet_text = c.execute(
            "SELECT text FROM tweets WHERE created_by=?;", (
                twitteruser,))

        text = tweet_text.fetchone()
        if text is not None:
            # content = mimesis.Text()
            c.execute('''INSERT INTO notifications
                        (notified_by, notified, tweet_text)
                        VALUES
                        (:1,:2,:3)
                        ''', (
                            twitteruser, twitteruser_notified, text[0]))

conn.commit()

conn.close()
