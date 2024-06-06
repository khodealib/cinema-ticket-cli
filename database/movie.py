from sqlalchemy import (CheckConstraint, Column, ForeignKey, Integer,
                        SmallInteger, String, orm)

from utils.exceptions import InvalidRateValueError

from .base import Base


class Movie(Base):
    """
    a mapping class for Movie table, subclasses Base class
    each object represents a row in Movie table
    Columns:
        -id
        -name
        -age_limit
        -rate {between 0 and 5}
    """

    __tablename__ = 'movies'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(length=100), nullable=False, unique=True)
    age_limit = Column("age_limit", SmallInteger, nullable=False, default=1)
    rate = Column("rate", SmallInteger, CheckConstraint('rate >= 0 AND rate <=5'), default=None)


    def __repr__(self): 
        return f"<Movie(name='{self.name}', age_limit='{self.age_limit}', rate='{self.rate}'>"
    

    @orm.validates('rate')
    def validate_rate(self,value):
        if not 0 <= value <=5 :
            raise InvalidRateValueError(f'Invalid rate {value}')
        return value
    
