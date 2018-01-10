#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def date_job():
    print "{}: date job".format(datetime.now())


def add_asp_scheduler(dt, id):
    scheduler = BackgroundScheduler()

    scheduler.add_job(date_job, trigger='date', run_date=dt, id=id)
    print "scheduler add job."

    try:
        scheduler.start()
    except Exception as err:
        print "clear job."
        scheduler.remove_all_jobs()

