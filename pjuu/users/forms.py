# -*- coding: utf8 -*-

"""Web forms.

:license: AGPL v3, see LICENSE for more details
:copyright: 2014-2015 Joe Doherty

"""

# 3rd party imports
from flask_wtf import Form
from wtforms import BooleanField, TextAreaField, SelectField, StringField
from wtforms.validators import Length
# Pjuu imports
from pjuu.posts.backend import MAX_POST_LENGTH


class ChangeProfileForm(Form):
    """
    This is the form used to update your about information
    """
    hide_feed_images = BooleanField('Hide images in feeds')

    choices = [('25', '25'), ('50', '50'), ('100', '100')]

    feed_pagination_size = SelectField('Number of feed items to show',
                                       choices=choices, default=25)
    replies_pagination_size = SelectField('Number of replies to show',
                                          choices=choices, default=25)
    alerts_pagination_size = SelectField('Number of alerts to show',
                                         choices=choices, default=50)

    about = TextAreaField('About', [
        Length(max=MAX_POST_LENGTH,
               message='About can not be larger than '
                       '{} characters'.format(MAX_POST_LENGTH))
    ])


class SearchForm(Form):
    """
    This form is really simple. It is here to keep all forms at WTFroms
    """
    query = StringField("Query")
