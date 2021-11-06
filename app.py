from flask import Flask, render_template, send_from_directory, redirect, session, request, escape, jsonify
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from flask_sqlalchemy import SQLAlchemy 
import os
from addict import Dict
import json
from datetime import datetime
app = Flask(__name__)

#app.config['SECRET_KEY'] = 'QuyylPshMfZdediqCAboDfCyPr1BfZ1z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = os.environ.get("API_KEY")
apiKey = os.environ.get("API_KEY")

db = SQLAlchemy(app)

class Userpoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    points = db.Column(db.Integer)

class IgnoreUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    host = db.Column(db.String(50))
    event_type = db.Column(db.String(50))
    date = db.Column(db.DateTime)

db.create_all()
db.session.commit()

@app.route("/")
def redirMain():
    return "<script>location.replace('https://zt-e.tech/')</script>"


@app.route("/user/addpoints", methods=['POST'])
def apiLog():
    req_data = request.get_json()
    username = req_data['USERNAME']
    api_key = req_data['API_KEY']
    target_points = req_data['POINTS']
    print(username)
    print(target_points)
    if api_key == apiKey:
    #return request.data['username']
        user = Userpoints.query.filter_by(username=username).first()
        if user is not None:
            original_points = int(user.points)
            print(original_points)
            target_points = int(target_points)
            print(original_points+target_points)
            user.points = original_points+target_points
            targ = original_points+target_points
        else:
            data = Userpoints(username=username, points=target_points)
            db.session.add(data)
            targ = target_points
        db.session.commit()
        return str(targ),200
    else:
        return '401', 401

@app.route("/user/deductpoints", methods=['POST'])
def apiReduct():
    return request.data['username']
    
@app.route("/user/viewpoints", methods=['POST'])
def apiView():
    req_data = request.get_json()
    api_key = req_data['API_KEY']
    if api_key == apiKey:
        if req_data['req_type']  == "Singular":
            username = req_data['USERNAME']
            print(username)
            user = Userpoints.query.filter_by(username=username).first()
            if user is None:
                return '569', 569
            return str(user.points)
        elif req_data['req_type'] == "Batch":
            users = Userpoints.query.order_by(Userpoints.id.desc()).all()
            targdict = Dict()
            for x in users:
                targdict['__'].setdefault(x.username,x.points)
            resp = app.response_class(
                response=json.dumps(targdict),
                status = 200,
                mimetype = "application/json"
            )
            return resp
    else:
        return '401', 401
    
@app.route("/user/ignore", methods=['POST'])
def userIgnore():
    req_data = request.get_json()
    userid = req_data['USERID']
    api_key = req_data['API_KEY']
    req_type = req_data['REQ_TYPE']
    if req_type == "ADD":
        user = IgnoreUser.query.filter_by(userid=userid).first()
        if user is None:
            data = IgnoreUser(userid=userid)
            db.session.add(data)
            db.session.commit()
            return '200',200
        else:
            return '569',569
    elif req_type == "CHECK":
        user = IgnoreUser.query.filter_by(userid=userid).first()
        if user is None:
            return "not found",569
        else:
            return str(user.userid),200
    elif req_type == "REMOVE":
        user = IgnoreUser.query.filter_by(userid=userid).first()
        if user is None:
            return "569",569
        else:
            db.session.delete(user)
            db.session.commit()
            return "200", 200 


@app.route("/user/setpoints", methods=['POST'])
def apiPointsSet():
    req_data = request.get_json()
    username = req_data['USERNAME']
    api_key = req_data['API_KEY']
    target_points = req_data['POINTS']
    print(username)
    print(target_points)
    if api_key == apiKey:
    #return request.data['username']
        user = Userpoints.query.filter_by(username=username).first()
        if user is not None:
            user.points = target_points
        else:
            data = Userpoints(username=username, points=target_points)
            db.session.add(data)
        db.session.commit()
        return '200',200
    else:
        return '401', 401

@app.route("/schedule", methods=['POST'])
def apiSchedule():
    req_data = request.get_json()
    api_key = req_data['API_KEY']
    req_type = req_data['req_type']
    if api_key == apiKey:
        if req_type == "ViewNext":
            event = Schedule.query.order_by(Schedule.date.asc()).first()
            if event is None:
                return '569', 569
            
            event_host_id = str(event.host)
            event_host_name = str(event.username)
            event_date = str(event.date)
            event_type = str(event.event_type)
            event_id = str(event.id)
            #return("Data Recieved:" + ' ' + event_date + ' ' + event_type + ' ' + event_host_name + ' ' + event_host_id),200
            data = {
            "EVENT_HOST_NAME":event_host_name,
            "EVENT_HOST_ID":event_host_id,
            "EVENT_DATE":event_date,
            "EVENT_TYPE":event_type,
            "EVENT_ID":event_id
            }
            response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )
            return response
        if req_type == "Counter":
            Number = Schedule.query.count()
            return str(Number)
        if req_type == "ViewNextNum":
            idnumber = req_data['EVENT_ID']
            event = db.session.query(Schedule).get(idnumber)
            if event is None:
                return '569', 569        
            event_host_id = str(event.host)
            event_host_name = str(event.username)
            event_date = str(event.date)
            event_type = str(event.event_type)
            event_id = str(event.id)
            #return("Data Recieved:" + ' ' + event_date + ' ' + event_type + ' ' + event_host_name + ' ' + event_host_id),200
            data = {
            "EVENT_HOST_NAME":event_host_name,
            "EVENT_HOST_ID":event_host_id,
            "EVENT_DATE":event_date,
            "EVENT_TYPE":event_type,
            "EVENT_ID":event_id
            }
            response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )
            return response
        if req_type == "New":
            event_host_name = req_data['EVENT_HOST_NAME']
            event_host_id = req_data['EVENT_HOST_ID']
            event_date = req_data['EVENT_DATE']
            event_type = req_data['EVENT_TYPE']
            event_date = event_date+":00"
            event_date = datetime.strptime(event_date, '%m/%d/%y %H:%M:%S')
            event_host_id = str(event_host_id)
            #event_date = str(event_date)
            #event_host_id = str(event_host_id)
            #return("Data Sent:" + ' ' + event_date + ' ' + event_type + ' ' + event_host_name + ' ' + event_host_id),200
            event = Schedule.query.filter_by(date=event_date).first()
            if event is not None:
                return "Event Already Exists!", 568
            else:
                data = Schedule(host=event_host_id,username=event_host_name, date=event_date, event_type=event_type)
                db.session.add(data)
                db.session.commit()
                return "200",200
        if req_type == "Remove":
            event_id = req_data['EVENT_ID']
            target = db.session.query(Schedule).get(event_id)
            if target is None:
                return "No Event with selected ID", 569
            event_date = str(target.date)
            event_host_name = str(target.username)
            event_host_id = str(target.host)
            event_type = str(target.event_type)
            db.session.delete(target) 
            db.session.commit()
            data = {
            "EVENT_HOST_NAME":event_host_name,
            "EVENT_HOST_ID":event_host_id,
            "EVENT_DATE":event_date,
            "EVENT_TYPE":event_type,
            }
            response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )
            return response
    else:
        return '401', 401

@app.errorhandler(404)
def notfound(error):
    return redirMain()