# -*- coding: utf-8 -*-
from icalendar import Calendar
from collections import namedtuple
from urllib import request

Vevent = namedtuple('Vevent', ['dtstart','dtend','summary','location'])
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
    
    
    def get_events(self,mode=None):
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
                ev=Vevent(dtstart=event.get('dtstart').dt,dtend=event.get('dtend').dt,summary=event.get('summary'),location=event.get('location'))
                if(ev.summary!="Férié" and ev.summary!="Vacances" ): events.append(ev)
        sort(events)
        self.events = events



def dic_search(events,i,j,e):
    if e>events[j].dtstart:
        return j+1
    while i!=j:
        k=(i+j)//2
        if e<=events[k].dtstart:
            j=k
        else:
            i=k+1
    return i
 
def sort(events):
    for i in range(1,len(events)):
        if events[i].dtstart<events[i-1].dtstart:
            k=dic_search(events,0,i-1,events[i].dtstart)
            e=events.pop(i)
            events.insert(k,e)

bainfo = IcalFetcher("https://hplanning2016.umons.ac.be/Telechargements/ical/EdT_BAB1_en_sc__informatiques.ics?version=14.0.2.5&idICal=0761D18EE9E46515176D24076096B534&param=643d5b312e2e36325d2666683d3126663d3131303030")
bainfo.get_events()
bainfo.mod_url("https://hplanning2016.umons.ac.be/Telechargements/ical/EdT_BAB1_en_sc__informatiques.ics?version=14.0.2.5&idICal=0761D18EE9E46515176D24076096B534&param=643d5b312e2e36325d2666683d3126663d3131303030")
bainfo.get_events()
for i in bainfo:
    print(i.summary)

