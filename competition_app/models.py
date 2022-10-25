from sqlalchemy.dialects.mysql import INTEGER
from competition_app import db
from competition_app.constants import roles


# Only GitHub users.
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(INTEGER(unsigned=True), primary_key=True, unique=True)
    avatar_url = db.Column(db.String(64))
    login = db.Column(db.String(32))
    name = db.Column(db.String(64))
    access_token = db.Column(db.String(64))

    role = db.Column(db.Enum(*roles), nullable=False, server_default=roles[-1])
    token = db.Column(db.String(36), unique=True)
    last_seen = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    joined_since = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    team = db.relationship("Team", back_populates="user", uselist=False)

class Team(db.Model):
    __tablename__ = 'teams'
    team_id = db.Column(INTEGER(unsigned=True), primary_key=True, unique=True)
    name = db.Column(db.String(32))
    contact_email = db.Column(db.String(64))

    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.user_id'))
    user = db.relationship('User', back_populates="team")

    members = db.relationship("TeamsMembers", backref="teams")


class TeamsMembers(db.Model):
    __tablename__ = 'members'
    member_id = db.Column(INTEGER(unsigned=True), primary_key=True, unique=True)
    name = db.Column(db.String(64))
    affiliation = db.Column(db.String(64))
    country = db.Column(db.String(32))
    city = db.Column(db.String(32))
    member_idx = db.Column(INTEGER(unsigned=True))

    team_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('teams.team_id'))
    #team = db.relationship('Team', backref=db.backref('members', order_by='TeamsMembers.member_idx'))

db.create_all()
db.session.commit()