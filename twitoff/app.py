"""Main app.routing file for TwitOff"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, insert_example_users


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    # ... TODO make the app!
    @app.route('/')
    def root():
        return render_template('base.html', title='Home',
                               users=User.query.all())
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)
    
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, 
                                      request.values['tweet_text'])
            tweet = request.values['tweet_text']
            speaker = user2 if prediction[0] == 0.0 else user1
            not_speaker = user1 if prediction[0] == 0.0 else user 2
            message = f'"{tweet}" is more likely to be said by {speaker} than by {not_speaker}'
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/update')
    def update():
        # Reset the database
        insert_example_users()
        return render_template('base.html', title='Users updated!',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    return app