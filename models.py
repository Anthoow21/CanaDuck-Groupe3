from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    private = db.Column(db.Boolean, default=False)
    topic = db.Column(db.String(255), default="")
    owner = db.Column(db.String(50), nullable=False)
    modes = db.relationship('ChannelMode', backref='channel', cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    moderators = db.relationship('ChannelModerator', backref='channel', cascade="all, delete-orphan")
    banned = db.relationship('ChannelBan', backref='channel', cascade="all, delete-orphan")
    invited = db.relationship('ChannelInvite', backref='channel', cascade="all, delete-orphan")
    members = db.relationship('ChannelMember', backref='channel', cascade="all, delete-orphan")

class ChannelModerator(db.Model):
    __tablename__ = 'channel_moderators'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    pseudo = db.Column(db.String(50), nullable=False)

class ChannelBan(db.Model):
    __tablename__ = 'channel_bans'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    pseudo = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(255), default="")

class ChannelInvite(db.Model):
    __tablename__ = 'channel_invites'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    pseudo = db.Column(db.String(50), nullable=False)

class ChannelMember(db.Model):
    __tablename__ = 'channel_members'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    pseudo = db.Column(db.String(50), nullable=False)

class ChannelMode(db.Model):
    __tablename__ = 'channel_modes'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    mode = db.Column(db.String(5), nullable=False)  # Exemple : '+r', '+m'
