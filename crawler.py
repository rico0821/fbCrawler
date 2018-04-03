# -*- coding: utf-8 -*-

import requests, sys, time
import pandas as pd

from datetime import datetime, timedelta

from logger import Log


class Crawler: 
    
    def __init__(self, token, version):
        """Crawler instance takes version and token as parameters."""
        
        self.version = version        
        self.token = token
        Log.info('New Crawler: ver. %s' % version)
    
    def setTarget(self, target):
        """Set target FB page for Crawler instance."""
        
        self.target = target
        Log.info('Target: %s' % target)
        
    def setTimeInterval(self, time_delta=1):
        """
        Set time interval in days for data extraction.
        DEFAULT: 1 day
        """
        
        self.time_delta = timedelta(days=time_delta)
        Log.info('Time delta: %i day(s)' % time_delta)
    
    def init(self):
        """Start crawling."""
        
        Log.info('Crawling initiated...')
        data = self._getTarget()
        
        df = pd.DataFrame(data)
        df.to_json('data/data.json')
        
        Log.info('Crawling finished!')

        
    def _getTarget(self):
        """Get data from target."""
        
        # Log task start time
        start_time = time.time()
        Log.info('Task started.')
        
        # Set time interval
        since = datetime.strftime(datetime.now()-self.time_delta, '%Y-%m-%d')
        until = datetime.strftime(datetime.now(), '%Y-%m-%d')

        # Get list of feed id from target
        feeds_url = 'https://graph.facebook.com/v%s/' % self.version + self.target + '/?fields=feed.since(' + since + ').until(' + until + '){id,message,link,shares,created_time,comments.summary(true), reactions.summary(true)}&' + self.token 
        feed_list = _getFeeds(_getRequest(feeds_url), [])

        # Get message, comments and reactions from feed
        data = []
        if feed_list:
            data = [_processFeed(feed) for feed in feed_list]

        # Get time cost
        cost_time = time.time() - start_time

        # Log task end time and time cost
        Log.info('Task finished.')
        Log.info('Time Cost:  ' + str(cost_time))

        return data
    
    
def _getRequest(url):
    """Send HTTP request to url and return the response."""

    try:
        request_result = requests.get(url, headers={'Connection':'close'}).json()
        Log.info('Sent request to: %s' % url)
        time.sleep(0.01) 

    except:
        Log.error('URL not found!')
        sys.exit()

    return request_result

def _getFeeds(feeds, feed_list):
    """Collect feed data from request response."""

    # If feeds exist
    feeds = feeds['feed'] if 'feed' in feeds else feeds

    if 'data' in feeds:

        for feed in feeds['data']:

            Log.info('Extracting feed data: ' + feed['id'])

            message = feed['message'] if 'message' in feed else ''
            link = feed['link'] if 'link' in feed else ''         
            shares = _getShares(feed)
            comments_count = _getComments(feed)
            reactions_count = _getReactions(feed)

            feed_list.append((feed['id'], message, link, shares, feed['created_time'], comments_count, reactions_count))

        # Check if feed has next or not
        if 'paging' in feeds and 'next' in feeds['paging']:
            feeds_url = feeds['paging']['next']
            feed_list = _getFeeds(_getRequest(feeds_url), feed_list)

        return feed_list

def _processFeed(feed):
    """Turns feed content into dictionary."""

    # Log process
    Log.info('Processing feed: ' + feed[0])

    # Create feed content dictionary
    feed_content = {
        'id' : feed[0],
        'message' : feed[1],
        'link' : feed[2],
        'shares' : feed[3],
        'created_time' : feed[4],
        'comments_count' : feed[5],
        'reactions_count' : feed[6]
    }

    return feed_content

def _getShares(feed):

    # If shares exist
    shares = feed['shares'] if 'shares' in feed else feed
    shares = shares['count'] if 'count' in shares else 0

    return shares

def _getComments(feed):

    # If comments exist
    comments = feed['comments'] if 'comments' in feed else feed
    comments = comments['data'] if 'data' in comments else comments
    comments = comments['summary'] if 'summary' in comments else comments
    comments_count = comments['total_count'] if 'total_count' in comments else 0

    return comments_count

def _getReactions(feed):

    # If reactions exist
    reactions = feed['reactions'] if 'reactions' in feed else feed
    reactions = reactions['data'] if 'data' in reactions else reactions
    reactions = reactions['summary'] if 'summary' in reactions else reactions
    reactions_count = reactions['total_count'] if 'total_count' in reactions else 0

    return reactions_count


##########################################################################################################
def fbQuery(self, query_term, query_type):

    search_url = 'https://graph.facebook.com/v%s/' % self.version + 'search?q='+query_term+'&type='+query_type+'&' + self.token

    return search_url

def getQueryID(self, url, item_list=[]):

    query_result = _getRequest(url)
    if 'data' in query_result:
        for item in query_result['data']:
            item_list.append(item['id'])

    if 'paging' in query_result and 'next' in query_result['paging']:
        results_url = query_result['paging']['next']
        item_list = self.getQueryID(results_url, item_list)

    return item_list


        
        
        
        
        
        
        
        
        