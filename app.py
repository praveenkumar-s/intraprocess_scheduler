import sys
from datetime import datetime
from flask import Flask , jsonify
from flask import request
from jsonschema import validate
import json
import requests
import APS_Scheduling_Helper
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
sched = BackgroundScheduler()
sched.start()


@app.route('/')
def hello():
    print(str(request))
    return 'Flask Based Task Scheduler Docs: https://warped-trinity-9166.postman.co/collections/1523598-f5920ac0-0ab3-469b-99a5-c274fc49ad3a?version=latest&workspace=772a3856-cf0a-41e9-84da-1ea7d06a5ab6'


@app.route('/vm/bring_offline/<VM>')
def bring_offline(VM):
    return "{0} brought offline successfully @ {1}".format(VM, str(datetime.now()))


@app.route('/vm/bring_online/<VM>')
def bring_online(VM):
    return "{0} brought online successfully @ {1}".format(VM, str(datetime.now()))


@app.route('/schedules/reload')
def reload_schedules():
    sched.remove_all_jobs()
    load_schedules()
    return "Done!"


@app.route('/schedules/', methods =['GET'])
def get_schedules():
    js = json.load(open('schedule_config.json'))
    return jsonify(js)

@app.route("/schedules/", methods = ['POST'])
def load_schedules_request():
    incoming_data = request.get_json()
    try:
        validate(instance = incoming_data , schema = json.load(open('schedule_schema.json')))
    except:
        msg ={
            "error":"Bad Request , Schema does not Match",
            "detail":str(sys.exc_info())
        }
        return jsonify(msg),400
    json.dump(incoming_data, open('schedule_config.json','w+'))
    sched.remove_all_jobs()
    load_schedules()
    msg = {
        "message":"Data updated successfully",
        "location":"/debug/scheduler/view_jobs"
    }
    return jsonify(msg)

def load_schedules():
    json_data = json.load(open('schedule_config.json'))
    if(json_data["scheduler_enabled"]):
        sch_data = json_data["schedules"]
        for items in sch_data:
            print(str(APS_Scheduling_Helper.perform_scheduling(sched, items)))

# ============================DEBUGGER METHODS================
@app.route('/debug_injection')
def debugger():
    print("inside debugger")
    print("outside debugger")
    return "thankyou, please visit again for debugging!!"


@app.route('/debug/scheduler/view_jobs')
def viewjobs():
    jobs = sched.get_jobs()
    str_jobs = ""
    for job in jobs:
        str_jobs = str_jobs+"\n {0} : {1}".format("job_id", str(job.id))
        str_jobs = str_jobs+"\n {0} : {1}".format("args", str(job.args))
        str_jobs = str_jobs+"\n {0} : {1}".format("func_ref", str(job.func_ref))
        str_jobs = str_jobs+"\n {0} : {1}".format("next_run_time", job.next_run_time.strftime("%m/%d/%Y, %H:%M:%S"))
        str_jobs = str_jobs+"==============================="

    return str_jobs

# ===============================================================


if __name__ == '__main__':
    load_schedules()
    app.run()
