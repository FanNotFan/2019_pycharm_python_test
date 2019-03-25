from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RoomForm(FlaskForm):
    roomid = StringField('RoomID', render_kw={'readonly': True})
    roomname = StringField('RoomName', render_kw={'readonly': True})
    bedtype = StringField('BedType', render_kw={'readonly': True})
    roomsize = StringField('RoomSize', render_kw={'readonly': True})
    roomclass = StringField('RoomClass', render_kw={'readonly': True})

