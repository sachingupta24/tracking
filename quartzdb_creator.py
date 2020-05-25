# db_creator.py

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///quartzdatabase2.db', echo=True)
Base = declarative_base()


class QuartzSerialNumber(Base):
    __tablename__ = "quartzserialnumber"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


class MicronPart(Base):
    """"""
    __tablename__ = "micronpart"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    quartz_type = Column(String)
    installation_date = Column(String)
    toolname = Column(String)
    quartz_condition_type = Column(String)
    quartzserialnumber_id = Column(Integer, ForeignKey("quartzserialnumber.id"))
    quartzserialnumber = relationship("QuartzSerialNumber", backref=backref(
        "micronpart", order_by=id))




# create tables
Base.metadata.create_all(engine)

