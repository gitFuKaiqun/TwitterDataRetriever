__author__ = 'Kaiqun'

import twitter
from OutputFuncs import outputConsole, outputFile

# This module includes all functions that retrieve the specified twitter data.

# Store all the account information need in the "TwitterAccountList" file.
TwitterAccountPool = [line.strip() for line in open('res/AccountsLists/TwitterAccountList', 'r')]
# Set the keywords list
KeyWordsList = open('res/Kwds/TargetKey', 'r').read().split('\t')


class StatusRecorder:
	"""
	This class will be used as the Monitor for the rate limiting.
	"""

	def __init__(self):
		self.AccountToken = 0
		self.KeywordToken = 0

	def NextAcc(self):
		self.AccountToken = (self.AccountToken + 1) % AccCount()

	def NextKey(self):
		self.KeywordToken = (self.KeywordToken + 1) % len(KeyWordsList)


# This function assigns account for the current job that is on going.
def NextAccount(AccNum):
	"""

	:param AccNum: the index for the selected account
	:return: an api object that can do the job
	"""
	api = twitter.Api(
		consumer_key=TwitterAccountPool[AccNum].split('\t')[0],
		consumer_secret=TwitterAccountPool[AccNum].split('\t')[1],
		access_token_key=TwitterAccountPool[AccNum].split('\t')[2],
		access_token_secret=TwitterAccountPool[AccNum].split('\t')[3]
	)
	return api

# Support function for counting the accounts numbers in the "TwitterAccountList" file.
def AccCount():
	count = 0
	thefile = open('res/AccountsLists/TwitterAccountList', 'rb')
	while 1:
		buffer = thefile.read(65536)
		if not buffer:
			break
		count += buffer.count('\n')
	return count + 1


def ExtractRecentTweets(api, User_id, since_twtId = 0, RetrieveTotal = True):
	"""
	This function extracts the target user's recent tweets
	:param api: an api object
	:param User_id: the user ID for the target user
	:param since_twtId: the start tweet id for the future tweets list
	:return: a tuple object contains the indicator and the resulted tweets list
	"""
	TwtStatusList = []
	while True:
		TempRslt = api.GetUserTimeline(user_id = User_id, count = 200, max_id = since_twtId)
		if not TempRslt:
			return ('Done', TwtStatusList)
		for item in TempRslt:
			TwtStatusList.append(item)
		if RetrieveTotal is False:
			return ('Done', TwtStatusList)
		since_twtId = TempRslt[len(TempRslt) - 1].id - 1

# This function convert the user's screen_name to user id
def ScreenName2Id(api, userScreenName):
	"""

	:param api: an api object
	:param userScreenName: the screen_name for the target user
	:return: the id number for the target user
	"""
	return api.GetUser(screen_name = userScreenName).id