from config import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema



class UserTable(db.Model):
    __tablename__ = "UserTable"
    __table_args__ = {"schema":"CW2"}

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmailAddress = db.Column(db.String(255), unique=True, nullable=False)
    Role = db.Column(db.String(50), nullable=False)

    trails = db.relationship("Trail", back_populates="owner", cascade="all, delete-orphan")


class Feature(db.Model):
    __tablename__ = "Feature"
    __table_args__ = {"schema":"CW2"}

    TrailFeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailFeature = db.Column(db.String(100), nullable=False)

    

class TrailFeature(db.Model):
    __tablename__ = "TrailFeature"
    __table_args__ = {"schema":"CW2"}

    TrailID = db.Column(db.Integer, db.ForeignKey("CW2.Trail.TrailID"), primary_key=True)
    TrailFeatureID = db.Column(db.Integer, db.ForeignKey("CW2.Feature.TrailFeatureID"), primary_key=True, nullable=False)



class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {"schema":"CW2"}

    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailName = db.Column(db.String(100), nullable=False)
    TrailSummary = db.Column(db.String(255))
    TrailDescription = db.Column(db.Text)
    Difficulty = db.Column(db.String(50))
    Location = db.Column(db.String(255))
    Length = db.Column(db.Float)
    ElevationGain = db.Column(db.Float)
    RouteType = db.Column(db.String(50))
    OwnerID = db.Column(db.Integer, db.ForeignKey('CW2.UserTable.UserID'), nullable=False)
    LocationPt1 = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.Location_Point'))
    LocationPt2 = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.Location_Point'))
    LocationPt3 = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.Location_Point'))
    LocationPt4 = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.Location_Point'))
    LocationPt5 = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.Location_Point'))

    owner = db.relationship("UserTable", back_populates="trails")

    location_pt1 = db.relationship("LocationPoint", foreign_keys=[LocationPt1])
    location_pt2 = db.relationship("LocationPoint", foreign_keys=[LocationPt2])
    location_pt3 = db.relationship("LocationPoint", foreign_keys=[LocationPt3])
    location_pt4 = db.relationship("LocationPoint", foreign_keys=[LocationPt4])
    location_pt5 = db.relationship("LocationPoint", foreign_keys=[LocationPt5])


class LocationPoint(db.Model):
    __tablename__ = "LocationPoint"
    __table_args__ = {"schema":"CW2"}

    Location_Point = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Description = db.Column(db.String(255))



class UserTableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserTable
        load_instance = True
        sqla_session = db.session
        include_fk = True

 



    
class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_relationships = False

    OwnerID = fields.Integer()
    LocationPt1 = fields.Integer(allow_none=True)  
    LocationPt2 = fields.Integer(allow_none=True)
    LocationPt3 = fields.Integer(allow_none=True)
    LocationPt4 = fields.Integer(allow_none=True)
    LocationPt5 = fields.Integer(allow_none=True)

    RouteType = fields.String(allow_none=True)
    

    

    
class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session
        include_fk = True

    trail = fields.Nested("TrailSchema")
    feature = fields.Nested("FeatureSchema")



class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session
        include_fk = True





class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session
        include_fk = True







    
    
