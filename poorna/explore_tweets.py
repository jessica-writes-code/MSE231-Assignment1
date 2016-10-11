import json
import sys

'''Script to obtain some (basic) summary statistics about different time zones in the data.

Usage:

zcat <filename> | python explore_tweets.py

'''

if __name__ == '__main__':
    tweetCount = 0 
    keyErrorsCount = 0
    USCount = 0
    noneCount = 0
    USCityCount = 0
    otherTimeZones = set()
    for line in sys.stdin:
        try:
            tweet = json.loads(line)
        except ValueError: #signals EOF (script was killed, hence file abruptly terminates)
            continue
        tweetCount = tweetCount + 1
        if tweetCount % 50000 == 0:
            print "Tweets counted:", tweetCount
        try:
            content = tweet['text']
        except KeyError:
            keyErrorsCount += 1
            continue
        timezone = tweet['user']['time_zone']
        US_timezones = ['Pacific Time (US & Canada)',\
                        'Mountain Time (US & Canada)',\
                        'Central Time (US & Canada)',\
                        'Eastern Time (US & Canada)']
        if timezone in US_timezones:
            USCount += 1
        elif timezone == None:
            noneCount += 1
        elif timezone in ['America/Chicago', 'America/Denver', \
                        'America/New_York', 'America/Los_Angeles', \
                        'America/Detroit', 'Hawaii']:
            USCityCount += 1
        else:
            otherTimeZones.add(timezone)
             

    print "------SUMMARY------"
    print "Total number of tweets scraped:", tweetCount
    print "Number of tweets in four US-normalized time zones of interest:", USCount
    print "Number of key errors (no data of interest in tweet):", keyErrorsCount
    print "Number of time zones set to None:", noneCount
    print "Number of tweets from other US time zones:", USCityCount
    print "-------------------"
    print "Other timezones:"
    for tz in otherTimeZones:
        print tz
    print "--------------------"
