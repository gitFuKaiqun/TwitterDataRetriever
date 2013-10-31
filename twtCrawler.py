__author__ = 'Kaiqun'

import twitter
import time
import DB_Connection
import json
from time import gmtime, strftime
from TwtSummation import twtStaScoreCalcu


TwitterAccountPool = [line.strip() for line in open('res/AccountsLists/TwitterAccountList', 'r')]
KeyWordsList = open('res/Kwds/TargetKey', 'r').read().split('\t')

OverAllCount = 0


class StatusRecorder:
	def __init__(self):
		self.AccountToken = 0
		self.KeywordToken = 0

	def NextAcc(self):
		self.AccountToken = (self.AccountToken + 1) % AccCount()

	def NextKey(self):
		self.KeywordToken = (self.KeywordToken + 1) % len(KeyWordsList)


ApiMonitor = StatusRecorder()


def NextAccount(AccNum):
	api = twitter.Api(
		consumer_key = TwitterAccountPool[AccNum].split('\t')[0],
		consumer_secret = TwitterAccountPool[AccNum].split('\t')[1],
		access_token_key = TwitterAccountPool[AccNum].split('\t')[2],
		access_token_secret = TwitterAccountPool[AccNum].split('\t')[3]
	)
	return api


def AccCount():
	count = 0
	thefile = open('res/AccountsLists/TwitterAccountList', 'rb')
	while 1:
		buffer = thefile.read(65536)
		if not buffer:
			break
		count += buffer.count('\n')
	return count + 1


def outputDataBase(MethodIndex, ApiResult):
	"""

	:param MethodIndex: set to '0' connect to Microsoft SQL Server; set to '1' connect to MySQL Server
	"""
	if MethodIndex is 0:
		DB_Connection.MS_SqlServer_Method(ApiResult)
	elif MethodIndex is 1:
		DB_Connection.MY_SQL_Method(ApiResult)
	else:
		print 'DB connection doesn\'t exist'


def TwitterCrawling():
	"""
	This function enables crawling Tweets with a list of Twitter application accounts and a keywords list.

	"""
	global OverAllCount
	global ApiMonitor
	while True:
		try:
			TwitterApiInstance = NextAccount(ApiMonitor.AccountToken)
			OverAllCount = 0
			Xcordi = 38.907265
			Ycordi = -77.03649
			while True:
				#temp = TwitterApiInstance.GetSearch(term = KeyWordsList[ApiMonitor.KeywordToken], lang = 'en',
				#                                    count = 100, geocode = (Xcordi, Ycordi, '20mi'))
				temp = TwitterApiInstance.GetSearch(term = 'crash AND lane AND right', lang = 'en',
				                                    count = 100, geocode = (Xcordi, Ycordi, '20mi'))
				word = KeyWordsList[ApiMonitor.KeywordToken]
				ApiMonitor.NextKey()
				time.sleep(0.05)
				DB_Connection.MongoDB_Insertion(temp)
				OverAllCount += 1
				pass

		except Exception, e:
			global OverAllCount
			if e.__class__.__name__ is 'TwitterError':
				Errotype = e.message[0]['code']
				if Errotype is 88:
					ApiMonitor.NextAcc()
					print 'Switch Account! Next Account:' + str(
						ApiMonitor.AccountToken) + '  Total queries sent:' + str(OverAllCount) + '    ' + strftime(
						"%Y-%m-%d %H:%M:%S", gmtime())
				else:
					print str(e)
			else:
				print "SERIOUS ERROR! ======> " + str(e)


if __name__ == '__main__':
	print TwitterCrawling()