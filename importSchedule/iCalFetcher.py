# -*- coding: utf-8 -*-
from icalendar import Calendar
from collections import namedtuple
from urllib import request
import csv
import psycopg2

Vevent = namedtuple('Vevent', ['dtstart','dtend','summary','location','description'])
class IcalFetcher:
    """
    Retrieves the iCal data from a url.
    """
    def __init__(self,url):
        self.url = url
        
    def mod_url(self,url):
        """
        Modifies iCal file url
        """
        self.url = url
    
    
    def __iter__(self):
        """
        Iterator for every event in the iCallFetcher
        """
        for ev in self.events:
            yield ev
    
    
    def get_events(self):
        """
        Download the iCal file and puts all data in a list
        """
        events=[]
        if(self.url!=None):
            gcal=Calendar.from_ical((request.urlopen(self.url)).read())
        else:
            raise ValueError("URL missing")
        for event in gcal.walk():
            if event.name=="VEVENT":
                if event.get('location')==None:
                    ev = Vevent(dtstart=event.get('dtstart').dt, dtend=event.get('dtend').dt, summary=event.get('summary'), location='',description=event.get('description'))
                else:
                    ev=Vevent(dtstart=event.get('dtstart').dt,dtend=event.get('dtend').dt,summary=event.get('summary'),location=event.get('location'),description=event.get('description'))
                if(ev.summary!="Férié" and ev.summary!="Vacances" and ev.description!=None):
                    events.append(ev)
        self.events = events
    
    def to_course(self,cursor,unit):
        for i in self:
            c = Course()
            if(i.description!=None):
                for desc in i.description.split("\n"):
                    print(desc)
                    if (desc.split(" : ")[0] == "Matière" and len(desc.split(" : "))>1):
                        if (len(desc.split(" : ")[1].split(" - "))>1):
                            c.cid=desc.split(" : ")[1].split(" - ")[0]
                            c.coursename=desc.split(" : ")[1].split(" - ")[1]

                    if (desc.split(" : ")[0] == "Enseignant" or desc.split(" : ")[0] == "Enseignants"):
                        c.profs=desc.split(" : ")[1].split(", ")

                    if (desc.split(" : ")[0] == "Type"):
                        c.ctype=desc.split(" : ")[1]

                    if (desc.split(" : ")[0] == "Motif d'annulation"):
                        c.canceled=True

                    if (desc.split(" : ")[0] == "Mémo"):
                        c.memo=desc.split(" : ")[1]
                c.unit=unit.replace("'", " ")
                if(i.location!=None):
                    c.loca=i.location.split(", ")
                c.start=i.dtstart
                c.end=i.dtend
                c.completeCourse()
                c.add_to_db(cursor)


class Course:
    def __init__(self):
        self.cid=None
        self.coursename=None
        self.profs=None
        self.ctype=None
        self.start=None
        self.end=None
        self.loca=None
        self.canceled=False
        self.unit=None


    def completeCourse(self):
        if(self.coursename!=None): self.coursename = self.coursename.replace("'", " ")
        if (self.cid!=None):self.cid = self.cid.replace("'", " ")
        if(self.profs!=None):
            for prof in range(len(self.profs)):
                self.profs[prof] = self.profs[prof].replace("'", " ")
        if(self.ctype!=None):self.ctype = self.ctype.replace("'", " ")
        if(self.loca!=None):
            for loc in range(len(self.loca)):
                self.loca[loc] = self.loca[loc].replace("'", " ")


    def add_to_db(self, cursor):
        #course table
        if(self.cid!=None):
            str="select * from superplanning.course where (small_name='"+self.cid+"')"
            cursor.execute(str)
            a=cursor.fetchall()
            if(len(a)==0):
                str2="insert into superplanning.course (small_name) values('"+self.cid+"')"
                cursor.execute(str2)

        #type table
        if(self.ctype!=None):
            str = "select * from superplanning.type where (name='" + self.ctype + "')"
            cursor.execute(str)
            a = cursor.fetchall()
            if (len(a) == 0):
                str2 = "insert into superplanning.type (name) values('" + self.ctype + "')"
                cursor.execute(str2)

        #teacher table
        if(self.profs!=None):
            for prof in self.profs:
                str = "select * from superplanning.teacher where (name='" + prof + "')"
                cursor.execute(str)
                a = cursor.fetchall()
                if (len(a) == 0):
                    str2 = "insert into superplanning.teacher (name) values('" + prof + "')"
                    cursor.execute(str2)

        #location table
        if(self.loca!=None):
            for loc in self.loca:
                str = "select * from superplanning.location where (location='" + loc + "')"
                cursor.execute(str)
                a = cursor.fetchall()
                if (len(a) == 0):
                    str2 = "insert into superplanning.location (location) values('" + loc + "')"
                    cursor.execute(str2)
        # unit table
        if (self.unit != None):
            str = "select * from superplanning.unit where (name='" + self.unit + "')"
            cursor.execute(str)
            a = cursor.fetchall()
            if (len(a) == 0):
                str2 = "insert into superplanning.unit (name) values('" + self.unit + "')"
                cursor.execute(str2)
        # schedule_unit table
        # schedule table
        # schedule_location table
        # schedule_teacher table
    

connexion =psycopg2.connect("dbname='superplanning' user='superplanning' host='localhost' password='superplanning' port='3000'")
cursor = connexion.cursor()

with open("icalendar.csv") as csvfile:
    csvread =csv.reader(csvfile,delimiter=",")
    cpt = 5
    for raw in csvread:
            iCalFile = IcalFetcher(raw[1])
            iCalFile.get_events()
            iCalFile.to_course(cursor,raw[0])
"""
bainfo = IcalFetcher("https://hplanning2016.umons.ac.be/Telechargements/ical/EdT_BAB1_en_sc__informatiques.ics?version=14.0.2.5&idICal=0761D18EE9E46515176D24076096B534&param=643d5b312e2e36325d2666683d3126663d3131303030")
bainfo.get_events()
bainfo.to_course(cursor,"InfoTest")
"""
connexion.commit()
connexion.close()