import sys
import json
import datetime
import csv

def round_time_15(initial_time):
	"""
	Description
	-----------
	Rounds a datetime to the nearest 15 minute interval

	Parameters
	----------
	initial_time, time, required
		Unrounded time

	Returns
	-------
	rounded time, time
		Time rounded to nearest 15 minute interval
	"""
	rounded_time = initial_time
	rounded_time = rounded_time + datetime.timedelta(minutes=7.5)
	rounded_time = rounded_time - datetime.timedelta(minutes=rounded_time.minute % 15,
                         							 seconds=rounded_time.second,
                         							 microseconds=rounded_time.microsecond)
	return(rounded_time)

# Read each line in STDIN file
for line in sys.stdin:
	# Load JSON to dictionary
	try:
		tweet = json.loads(line)
	except ValueError:
		continue

	# Timezone
	valid_tz = ["Eastern Time (US & Canada)","Central Time (US & Canada)","Mountain Time (US & Canada)","Pacific Time (US & Canada)"]
	## Filter to US timezones
	if tweet.get("user",{}).get("time_zone", None) in valid_tz:
		tweet_tz = tweet["user"]["time_zone"]
	else:
		continue

	# Date/Time
	if tweet.get("timestamp_ms",None) != None:
		utc_ms = float(tweet["timestamp_ms"])
		tweet_date_time = datetime.datetime.fromtimestamp(utc_ms/1000.0)
		tweet_date_time_rd = round_time_15(tweet_date_time)
		tweet_date = tweet_date_time_rd.date()
		tweet_time = tweet_date_time_rd.time()
	else:
		continue

	# Write data to stdout
	print "\t".join([str(tweet_date), str(tweet_time), tweet_tz])