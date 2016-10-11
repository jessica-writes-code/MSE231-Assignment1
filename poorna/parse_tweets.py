import sys
import json
import pprint
import pytz
from datetime import datetime, timedelta

def process_date_time(utc_timestamp):
    '''Read in UTC (ms) timestamp, convert to PT, round off to nearest 15 minute mark.'''
    pacific = pytz.timezone('US/Pacific')
    utc = pytz.timezone('utc')
    utc_dt = utc.localize(datetime.utcfromtimestamp(utc_timestamp))
    pt_dt = utc_dt.astimezone(pacific)
    pt_rounded = pt_dt + timedelta(minutes = 7.5) 
    pt_rounded = pt_rounded - timedelta(minutes=pt_rounded.minute % 15,\
                                        seconds=pt_rounded.second,\
                                        microseconds=pt_rounded.microsecond)
    return str(pt_rounded.date()), str(pt_rounded.time())
    
if __name__=='__main__':
    US_timezones = ['Pacific Time (US & Canada)',\
                    'Mountain Time (US & Canada)',\
                    'Central Time (US & Canada)', \
                    'Eastern Time (US & Canada)'] #define timezones of interest
    count = 0
    f = open('unfiltered_tweets.tsv', 'w')
    for line in sys.stdin:
        count = count + 1
        try:
            tweet = json.loads(line)
        except ValueError:
            continue
        try:                
            timezone = tweet['user']['time_zone']
            if timezone in US_timezones:
                utc_timestamp = int(tweet['timestamp_ms'])/1000
                rounded_date_pt, rounded_time_pt = process_date_time(utc_timestamp)
                f.write(rounded_date_pt + '\t' + rounded_time_pt + '\t' + \
                    timezone + '\n')
        except KeyError:
            continue
        if count % 50000==0: print count
    f.close()
        
