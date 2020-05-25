# models.py

from quartzapp import db


class QuartzSerialNumber(db.Model):
    __tablename__ = "quartzserialnumber"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return " {} ".format(self.name)


class MicronPart(db.Model):
    """"""
    __tablename__ = "micronpart"

    id = db.Column(db.Integer, primary_key=True)
    quartz_type = db.Column(db.String)
    title = db.Column(db.String)
    toolname = db.Column(db.String)
    installation_date = db.Column(db.String)
    quartz_condition_type = db.Column(db.String)
    quartzserialnumber_id = db.Column(db.Integer, db.ForeignKey("quartzserialnumber.id"))
    quartzserialnumber = db.relationship("QuartzSerialNumber", backref=db.backref(
        "micronpart", order_by=id), lazy=True)

class User(db.Model):
    __tablename__ = "usersmanagement"
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(15), unique=True)
    email= db.Column(db.String(50), unique=True)
    password= db.Column(db.String(80))