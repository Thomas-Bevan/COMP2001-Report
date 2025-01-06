from config import db
from models import Trail, TrailSchema, Feature, FeatureSchema, UserTable, UserTableSchema, LocationPoint, LocationPointSchema, TrailFeature, TrailFeatureSchema
import json
from flask import abort, make_response, request, Request, jsonify
import requests

URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"



def read_all():
    try:
        trails = Trail.query.all()
        schema = TrailSchema(many=True)
        serialized_data = schema.dump(trails)
        return jsonify(serialized_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_trail_by_id(TrailID):
    trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if trail is None:
        abort(404, "Could not find trail with that ID")

    schema = TrailSchema()
    serialized_data = schema.dump(trail)
    
    return jsonify(serialized_data), 200

def check_if_user_exists(request):

    email = request.headers.get("user_email")
    password = request.headers.get("user_password")

    if email is None or password is None:
        return False

    body = {"email": email, "password": password}
    response = requests.post(URL, json=body)
    response = response.json()

    if response[1] == "True":
        return True
    else:
        return False
    
    
def get_user(request):
    email = request.headers.get("user_email")
    user = UserTable.query.filter(UserTable.EmailAddress == email).one_or_none()

    return user

def create_trail():
    if check_if_user_exists(request) == False:
        abort(401, "Unauthorised credentials")

    user = get_user(request)
    if user.Role != "admin":
        abort(401, "Unauthorized credentials")
    
    try:
        trail_data = request.get_json()

        owner = UserTable.query.get(trail_data["OwnerID"])
        if not owner:
            return {"error": f"Owner with ID {trail_data['OwnerID']} does not exist."}, 400

        location_points = {f"LocationPt{i}": trail_data.get(f"LocationPt{i}") for i in range(1, 6)}
        invalid_locations = [lp for key, lp in location_points.items() if lp and not LocationPoint.query.get(lp)]
        if invalid_locations:
            return {"error": f"Invalid LocationPoint IDs: {invalid_locations}"}, 400

        trail_data.pop("TrailID", None)

        new_trail = TrailSchema().load(trail_data, session=db.session)
        db.session.add(new_trail)
        db.session.commit()

        return TrailSchema().dump(new_trail), 201

    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        return {"message": str(e)}, 500

def update_trail(TrailID):
    if check_if_user_exists(request) == False:
        abort(401, "Unauthorised credentials")

    user = get_user(request)
    if user.Role != "admin":
        abort(401, "Unauthorized credentials")
        
    trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    
    if trail is None:
        abort(404, "Trail with that ID not found")

    
    new_trail = request.get_json()
    new_trail['TrailID'] = TrailID

    new_trail = TrailSchema().load(new_trail, session=db.session)

    db.session.merge(new_trail)
    db.session.commit()

    return TrailSchema().dump(new_trail), 201

def delete_trail(TrailID):
    if check_if_user_exists(request) == False:
        abort(401, "Unauthorised credentials")

    user = get_user(request)
    if user.Role != "admin":
        abort(401, "Unauthorized credentials")
        
    trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if trail is None:
        abort(404, "Trail with that ID not found")


    db.session.delete(trail)
    db.session.commit()

    return make_response(f"Trail with ID {TrailID} deleted", 200)
