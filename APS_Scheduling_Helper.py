
import sys

def perform_scheduling(sched, config):
    
    try:
        function=config["action"]
        params = config["params"]
        day_of_week=config["schedule"]["day_of_week"]
        hour= config["schedule"]["hour"]
        minute=config["schedule"]["minute"]
        second=config["schedule"]["second"]
    except:
        print("key error: "+ str(sys.exc_info()))
        return None
    try:
        sched.add_job(function , 'cron', params,
        day_of_week = day_of_week , hour = hour , minute = minute,
        second = second)
        return sched
    except:
        print("Error While Scheduling! :"+ str( sys.exc_info()))
        return None

