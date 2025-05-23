from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association table for setlist_songs (many-to-many relationship)
setlist_songs = db.Table('setlist_songs',
    db.Column('setlist_id', db.Integer, db.ForeignKey('setlist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('position', db.Integer)
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    
    # Song parameters
    tempo = db.Column(db.Integer)  # Actual BPM
    tempo_category = db.Column(db.String(20))  # slow, medium, fast
    intensity = db.Column(db.String(20))  # low, medium, high
    lead_vocalist = db.Column(db.String(50))
    key = db.Column(db.String(20))  # e.g., A Minor, B Major
    is_minor = db.Column(db.Boolean, default=False)  # True if minor, False if major
    is_original = db.Column(db.Boolean, default=True)  # True if original, False if cover
    is_hit = db.Column(db.Boolean, default=False)  # True if it's a "hit" song to be included in every setlist
    duration = db.Column(db.Integer)  # Duration in seconds
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'tempo': self.tempo,
            'tempo_category': self.tempo_category,
            'intensity': self.intensity,
            'lead_vocalist': self.lead_vocalist,
            'key': self.key,
            'is_minor': self.is_minor,
            'is_original': self.is_original,
            'is_hit': self.is_hit,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Setlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    venue = db.Column(db.String(100))
    total_duration = db.Column(db.Integer)  # Total duration in seconds
    
    # Many-to-many relationship with songs
    songs = db.relationship('Song', secondary=setlist_songs, 
                           backref=db.backref('setlists', lazy='dynamic'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
            'venue': self.venue,
            'total_duration': self.total_duration,
            'songs': [song.to_dict() for song in self.songs],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
