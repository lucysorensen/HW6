import tweepy
import time
import csv

class TwitterUser(object):

	def __init__(self, screen_name, filename1, filename2):
		auth = tweepy.OAuthHandler('HT2lRb24tnyJ2THT2iBjmQ', 'sah4nVYDjXUiQPT0tbGwkeOefL2WPQ83hlLShFwioU')
		auth.set_access_token('29498268-YF6JtHJCL5MwwiYwhdaHVKXOmwV98fmIcwllVKOWw', 'BaWMo1ed44RjJ5tyLVC17wbHLMw11R2mnRhbAyLTbkg')
		self.api = tweepy.API(auth)

		self.home_followers = self.api.followers_ids(screen_name = screen_name)
		self.home_friends = self.api.friends_ids(screen_name = screen_name)
		self.originaluser = self.api.get_user(screen_name = screen_name)
		
		self.headers = ['user_id', 'screen_name', 'number followers']
		writeFile = open(filename1, "wb")
		self.csvwriter = csv.writer(writeFile)
		self.csvwriter.writerow(self.headers)
		self.csvwriter.writerow([self.originaluser.id, self.originaluser.screen_name, self.originaluser.followers_count])
		
		self.headers2 = ['starting user_id', 'time initiated']
		writeFile2 = open(filename2, "wb")
		self.csvwriter2 = csv.writer(writeFile2)
		self.csvwriter2.writerow(self.headers2)
		self.csvwriter2.writerow([self.originaluser.id, time.clock()])
		
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
			self.csvwriter.writerow([object.id, object.screen_name, object.followers_count])
			if user_followers > followers_twodegrees:
				most_twodegrees = object
				followers_twodegrees = user_followers
			seconddegree = self.api.followers_ids(user_id = user)
			time.sleep(60)
			for u in seconddegree:
				object = self.api.get_user(user_id = u)
				self.csvwriter.writerow([object.id, object.screen_name, object.followers_count])
				user_followers = object.followers_count
				if user_followers > followers_twodegrees:
					most_twodegrees = object
					followers_twodegrees = user_followers
				time.sleep(5)
		return str(most_twodegrees.screen_name)
	
	def get_mostactive(self):
		#This algorithm defines the most active user as the user whose last (twentieth) tweet on their timeline was created most recently.
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
		#This algorithm defines the most active user as the user whose last (twentieth) tweet on their timeline was created most recently.
		most_active = self.api.get_user(user_id = self.home_followers[0])
		active_count = most_active.statuses_count
		for user in self.home_friends:
			object = self.api.get_user(user_id = user)
			self.csvwriter.writerow([object.id, object.screen_name, object.followers_count])
			if object.statuses_count > active_count:
				most_active = object
				active_count = most_active.statuses_count
		return str(most_active.screen_name)

Lucy = TwitterUser('lucycs36', 'hw6_users.csv', 'hw6_crawls.csv')
print Lucy.get_mostpopular()
print Lucy.get_mostpopular_twodegrees()
print Lucy.get_mostactive()
print Lucy.get_mostactive_friend()
