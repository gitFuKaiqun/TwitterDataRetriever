__author__ = 'Kaiqun'

import sys
import copy


def init_pass(T):
	C = {}
	for t in T:
		for i in t:
			if i in C.keys():
				C[i] += 1
			else:
				C[i] = 1
	return C


def candidate_gen(F):
	C = []
	k = len(F[0]) + 1
	for f1 in F:
		for f2 in F:
			if f1[k - 2] < f2[k - 2]:
				c = copy.copy(f1)
				c.append(f2[k - 2])
				flag = True
				for i in range(0, k - 1):
					s = copy.copy(c)
					s.pop(i)
					if s not in F:
						flag = False
						break
				if flag and c not in C:
					C.append(c)
	return C


def compare_list(A, B):
	if len(A) <= len(B):
		for a in A:
			if a not in B:
				return False
	else:
		for b in B:
			if b not in A:
				return False
	return True


def apriori(T, minsup):
	C = []
	SupportList = []
	init = init_pass(T)
	keys = init.keys()
	keys.sort()
	C.append(keys)
	# print C
	n = len(T)
	F = [[]]
	for f in C[0]:
		SupFir = init[f] * 1.0 / n
		if SupFir >= minsup:
			F[0].append([f])
			SupportList.append(SupFir)
	k = 1
	while F[k - 1] != []:
		C.append(candidate_gen(F[k - 1]))
		F.append([])
		for c in C[k]:
			count = 0
			for t in T:
				if compare_list(c, t):
					count += 1
					SupLater = count * 1.0 / n
			if SupLater >= minsup:
				F[k].append(c)
				SupportList.append(SupLater)
		k += 1
	U = []
	for f in F:
		for x in f:
			U.append(x)
		returnVal = []
		for i in range(len(U)):
			returnVal.append((U[i], SupportList[i]))
	return returnVal


def printlist(T):
	for i in range(len(T)):
		for j in range(len(T[i])):
			print T[i][j]