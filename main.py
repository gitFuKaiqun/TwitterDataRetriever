__author__ = 'Kaiqun'

from RetrieveUsers import *
from Freqencycounting import frequencountingFile, FrequencyCalcuDictInput, recentDoc2Dic
from OutputFuncs import outputFile
from TwtSummation import *
import String2KwdList
from Apriori import apriori

userList = ['drgridlock', 'DCPoliceDept']

# Monitor instance
ApiMonitor = StatusRecorder()

def MainFunc1(UserScreenName):
	"""

	:param UserScreenName: enter the user screen Name here for extracting the recent tweets the user has just posted
	"""
	Flagging = 'NotDone'
	while Flagging is 'NotDone':
		try:
			TwitterApiInstance = NextAccount(ApiMonitor.AccountToken)
			(Flagging, StaList) = ExtractRecentTweets(api=TwitterApiInstance, User_id=ScreenName2Id(TwitterApiInstance, UserScreenName))
			# frequencounting(StaList)
			outputFile(StaList, '131009/WTOPrecent.txt')

		except Exception, e:
			if e.__class__.__name__ is 'TwitterError':
				Errotype = e.message[0]['code']
				if Errotype is 88:
					ApiMonitor.NextAcc()
					print 'Switch Account! Next Account:' + str(ApiMonitor.AccountToken)
				else:
					print e
			else:
				print "SERIOUS ERROR! ======> " + str(e)

def MainFunc2(userNames):
	TwitterApiInstance = NextAccount(ApiMonitor.AccountToken)

	outputRslt = []

	for user in userNames:
		(Flagging, StaList) = ExtractRecentTweets(api=TwitterApiInstance, User_id=ScreenName2Id(TwitterApiInstance, user), RetrieveTotal=False)
		for item in StaList:
			outputRslt.append((item.text, tweetScoreCalcu(item.text), user))

	return outputRslt

def MainFunc3():
	outputRslt = []
	for line in open('D:\General.txt', 'r'):
		try:
			tmp = line.strip().replace('\n', ' ').replace('\r', ' ').split('\t')
			outputRslt.append((tmp[1], tweetScoreCalcu(tmp[1]), tmp[0]))
		except:
			pass

	return outputRslt

def MainFunc4():
	outputRslt = []
	for line in open('Results/131009/WTOPrecent.txt', 'r'):
		try:
			tmp = line.strip().replace('\n', ' ').replace('\r', ' ').split('\t')
			outputRslt.append(String2KwdList.Str2KList(tmp[2]))
		except:
			pass

	return outputRslt

def MainFunc5():
	frequencountingFile(Listings=open('Results/131009/WTOPrecent.txt', 'r'))

def TestingFunc(inputTweet, minScore):
	if tweetScoreCalcu(inputTweet)[0] >= minScore:
		return 'POS'
	else:
		return 'NEG'

def RunningExpr01():
	for i in range(40):
		CountA = 0
		CountB = 0
		CountC = 0
		CountD = 0
		for line in open('res/TestingSets/Pos', 'r'):
			if TestingFunc(line.strip(), float(i)/10) == 'POS':
				CountA += 1
			else:
				CountB += 1
				# print 'False Neg: ' + line.strip()
		for line in open('res/TestingSets/Neg', 'r'):
			if TestingFunc(line.strip(), float(i)/10) == 'NEG':
				CountD += 1
			else:
				CountC += 1
				# print 'False Pos: ' + line.strip()
		print 'Expr: ' + str(float(i)/10)
		print 'Accurcy: ' + str(float((CountA + CountD))/(CountA + CountB + CountC + CountD))
		print 'FP Rate: ' + str(float(CountC) / (CountA + CountC))
		print 'FN Rate: ' + str(float(CountB) / (CountA + CountB))
		print '--------------'

def RunningExpr02():
	OurputRslt = apriori(MainFunc4(), 0.02)
	from operator import itemgetter
	for item in sorted(OurputRslt, key=itemgetter(1, 0), reverse=True):
		if len(item[0]) > 1:
			print str(item[0]).replace('[', '').replace(']', '').replace('\'', '') + '\t' + str(item[1])

if __name__ == '__main__':
	# RunningExpr01()
	# RunningExpr02()
	FrequencyCalcuDictInput(recentDoc2Dic('Results/131009/WordsCounting.txt'))