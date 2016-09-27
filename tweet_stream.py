from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import argparse
import gzip
import signal
import sys

# set up ctrl-c handling
def sigint_handler(signum, frame):
	print('')
	sys.exit()

if __name__ == "__main__":
	
	# exit gracefull with ctrl-c
	signal.signal(signal.SIGINT, sigint_handler)
	
	# set up the argument parser
	parser = argparse.ArgumentParser(description='Fetch data with Twitter Streaming API')
	parser.add_argument('--keyfile', help='file with user credentials', required=True)
	parser.add_argument('--gzip', metavar='OUTPUT_FILE', help='file to write compressed results to')
	parser.add_argument('--filter', metavar='W', nargs='*', 
		help='space-separated list of words; tweets are returned that match any word in the list')
	args = parser.parse_args()

	# read twitter app credentials and set up authentication
	creds = {}
	for line in open(args.keyfile, 'r'):
		row = line.strip()
		if row:
			key, value = row.split()
			creds[key] = value

	auth = OAuthHandler(creds['api_key'], creds['api_secret'])
	auth.set_access_token(creds['token'], creds['token_secret'])
	
	# write tweets to stdout or a gzipped file, as requested
	if args.gzip:
		# write to gzipped file
		f_out = gzip.open(args.gzip, 'w')
		print('Writing gzipped output to %s' % args.gzip)
		
		class listener(StreamListener):
			def on_data(self, tweet):
				f_out.write(tweet)
	
			def on_error(self, status):
				print status
	
	else:
		# write to stdout
		class listener(StreamListener):
			def on_data(self, tweet):
				print tweet
	
			def on_error(self, status):
				print status
	
	# start streaming
	twitterStream = Stream(auth, listener())
	
	if args.filter:
	  # track specific tweets  
	  twitterStream.filter(track=args.filter)
	else:
	  # get random sample of tweets
	  twitterStream.sample()

