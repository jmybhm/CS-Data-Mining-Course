'''
Association Rules Part 1
Laura Colbran and Jimin Yoo
February 3, 2015
'''
import sys
import string

'''Finds association rules, given a list of frequent itemsets size k'''
def assoc_rules(freq):
	print "Need to work out association rules"

'''recursive function that generates candidate itemsets size k from a list of frequent itemsets size 
k-1. Will keep going until it runs out of frequent itemsets.'''
def itemsets(L,k):
	print "this will be the recursive function for finding frequent itemsets size 3 and up"
	
'''Finds frequent itemsets size 1 & 2 independent of recursive function'''
def main():
	t = input("Support Threshold: ")
	c = input("Confidence: ")
	data = open('test.txt', 'r')
	candidates = {}
	num_users = 3 #CHANGE THIS TO 6040 when swap to real file
	if t > num_users:
		t = num_users
	#reads through file, counts # occurences of each movie
	for line in data:
		l = line.split("::")
		movie = l[1]
		if movie in candidates:
			candidates[movie] += 1
		else:
			candidates[movie] = 1
	data.close()
	L = []
	
#	iterates through dictionary of counts, makes list of singlets for those movies with frequencies 
#	that surpass threshold.
	for mov in candidates:
		if candidates[mov] >= t:
			L.append(mov)
	print "Number of singlets = %d" % len(L)
	print L 
#	merging singlets to make hash tree of all possible doublets.   
	c_2 = {}
	num_can_2 = 0
	for i in range(len(L)-1):			
		c_2[L[i]] = {}
		for j in range(i+1,len(L)):
			c_2[L[i]][L[j]] = 0
			num_can_2 +=1
	print "Number of candidates, k=2: %d" % num_can_2
	data = open('test.txt', 'r')
#	read through file, count occurrences of doublets
	current_usr = 0
	movies = []
	for line in data:
		l = line.split("::")
		usr = l[0]
		if usr > current_usr:
			for i in range(len(movies)):
				first = movies[i]
				for j in range(len(movies)):
					if first in c_2:
						if movies[j] in c_2[movies[i]]:
							c_2[movies[i]][movies[j]] += 1				
			current_usr = usr
			movies = [l[1]]
		else:
			movies.append(l[1])
# do this once more-- otherwise it skips the last transaction
	for i in range(len(movies)):
		first = movies[i]
		for j in range(len(movies)):
			if first in c_2:
				if movies[j] in c_2[movies[i]]:
					c_2[movies[i]][movies[j]] += 1		 
	data.close()	
#	New L to store frequent doublets	
	L=[]
	for first in c_2:
		for second in c_2[first]:
			if c_2[first][second] >= t:
				L.append((first,second))
	print "c_2 is", c_2
	print "new L is", L
#	find and print association rules	
	assoc_rules(L)
#	call recursive function to do the rest
	itemsets(L,3)
		
#	  file = open('/tmp/movies.dat', 'r')
#	  data = file.readlines()
#	  titles = {}
#	  for line in data:
#		  l = line.split("::")
#		  titles[l[0]] = l[1]
#	  file.close()
#	  new_file = open('movie_threshold.txt', 'a')
#	  for s in itemsets:
#		  for mov in s:
#			  line = titles[mov]
#			  line = line + "\n"
#			  new_file.write(line)

if __name__ == '__main__':
	main()