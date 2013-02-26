import tweepy
import time

class TwitterUser(object):

    	def __init__(self, screen_name):
		auth = tweepy.OAuthHandler('HT2lRb24tnyJ2THT2iBjmQ', 'sah4nVYDjXUiQPT0tbGwkeOefL2WPQ83hlLShFwioU')
		auth.set_access_token('29498268-YF6JtHJCL5MwwiYwhdaHVKXOmwV98fmIcwllVKOWw', 'BaWMo1ed44RjJ5tyLVC17wbHLMw11R2mnRhbAyLTbkg')
		self.api = tweepy.API(auth)
		#print api.rate_limit_status()
		self.home_followers = self.api.followers_ids(screen_name = screen_name)
		self.home_friends = self.api.friends_ids(screen_name = screen_name)
		
	def __str__(self, screen_name):
		return str(screen_name)

	def get_mostpopular(self):
		most_popular = self.api.get_user(user_id = self.home_followers[0])
		most_followers = most_popular.followers_count
		for user in self.home_followers:			
			object = self.api.get_user(user_id = user)
			number_followers = object.followers_count
			if number_followers > most_followers:
				most_popular = self.api.get_user(user_id = user)
				most_followers = number_followers
		return str(most_popular.screen_name)

	def get_mostpopular_twodegrees(self):
		outlier = self.get_mostpopular()
		modified_followers = self.home_followers
		modified_followers.remove(self.api.get_user(screen_name = outlier).id)
		most_twodegrees = self.api.get_user(user_id = modified_followers[0])
		followers_twodegrees = most_twodegrees.followers_count
		for user in self.home_followers:
			object = self.api.get_user(user_id = user)
			user_followers = object.followers_count
			if user_followers > followers_twodegrees:
				most_twodegrees = object
				followers_twodegrees = user_followers
			seconddegree = self.api.followers_ids(user_id = user)
			time.sleep(60)
			for u in seconddegree:
				object = self.api.get_user(user_id = u)
				user_followers = object.followers_count
				if user_followers > followers_twodegrees:
					most_twodegrees = object
					followers_twodegrees = user_followers
				time.sleep(5)
		return str(most_twodegrees.screen_name)
	
	def get_mostactive(self):
		#This algorithm defines the most active user as the user with the greatest number of status updates / "tweets"
		outlier = self.get_mostpopular()
		modified_followers = self.home_followers
		modified_followers.remove(self.api.get_user(screen_name = outlier).id)
		most_active = self.api.get_user(user_id = modified_followers[0])
		active_count = most_active.statuses_count
		for user in self.home_followers:
			object = self.api.get_user(user_id = user)
			if object.statuses_count > active_count:
				most_active = object
				active_count = most_active.statuses_count
			user_followers = self.api.followers_ids(user_id = user)
			time.sleep(60)
			for u in user_followers:
				object = self.api.get_user(user_id = u)
				if object.statuses_count > active_count:
					most_active = object
					active_count = most_active.statuses_count
				time.sleep(5)
		return str(most_active.screen_name)
		
	def get_mostactive_friend(self):
    	#This algorithm defines the most active user as the user with the greatest number of status updates / "tweets"
		most_active = self.api.get_user(user_id = self.home_followers[0])
		active_count = most_active.statuses_count
		for user in self.home_followers:
			object = self.api.get_user(user_id = user)
			if object.statuses_count > active_count:
				most_active = object
				active_count = most_active.statuses_count
		return str(most_active.screen_name)

Lucy = TwitterUser('lucycs36')
print Lucy.get_mostpopular()
print Lucy.get_mostpopular_twodegrees()
print Lucy.get_mostactive()
print Lucy.get_mostactive_friend()
