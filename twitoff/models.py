"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users coresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        return'-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300)) # Allows for text + links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    """Example data to play with."""
    austen = User(id=1, name='austen')
    elon = User(id=2, name='elonmusk')
    jill = User(id=3, name='jillz')
    karen = User(id=4, name='AngryMama')
    steven = User(id=5, name='BossMan')
    
    DB.session.add(austen)
    DB.session.add(elon)
    DB.session.add(jill)
    DB.session.add(karen)
    DB.session.add(steven)
    DB.session.commit()


def insert_example_tweets():
    """Example tweets to play with."""
    austen_tweet = Tweet(id=1, text='Lambda FTW!', user_id=1, user=austen)
    elon_tweet = Tweet(id=2, text='No, SpaceX! @austen', user_id=2, user=elon)
    jill_tweet = Tweet(id=3, text='Youz guyz, check out this AWESOME link I found! www.lambdachool.com', user_id=3, user=jill)
    karen_tweet = Tweet(id=4, text='WHY MASKS? NO SENSE! I AM FROTHING AT THE MOUTH I AM SO MAD!!!!', user_id=4, user=karen)
    steven_tweet = Tweet(id=5, text='Another productive day! #lambdaschool #gettingitdone #datascience', user_id=5, user=steven)
    austen_tweet2 = Tweet(id=6, text='@elonmusk What? No way.', user_id=1, user=austen)

    DB.session.add(austen_tweet)
    DB.session.add(elon_tweet)
    DB.session.add(jill_tweet)
    DB.session.add(karen_tweet)
    DB.session.add(steven_tweet)
    DB.session.add(austen_tweet2)
    DB.session.commit()