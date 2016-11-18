'''Locality Sensitivy Hashing Part I
Laura Colbran and Jimin Yoo
Computes and prints the Jaccard similarity both exactly and by approximating it from a 
signature matrix. Prompts the user for the number of documents to read from a file, and 
for the ids of the two documents in question, and for the number of permutations to 
make for the signature matrix.
When naming doc ids, please make sure they're within the number of documents read!
We have much larger Jaccard similiarty estimation than the actual Jaccard similarity even with large permutation number
We ran some tests and suspect that is is because a and n are not relative primes (we still coded to take out some a/n  that are definitely not relative primes/
which made our results only slightly better)
data file name can be found in line 65.''' 

import random 
import string

def jaccard(docs,doc1,doc2):
    '''Computes and prints the exact Jaccard similarity between 2 documents.'''
    n = len(docs)
    sim = float(len(docs[doc2-1].intersection(docs[doc1-1])))/len(docs[doc2-1].union(docs[doc1-1]))
    print "Exact Jaccard Similarity between docs %d and %d is: %.3f" %\
        (doc1,doc2,sim)

def sigmatrix(docs,doc1,doc2):
    '''Computes signature matrix d documents by m permutations and prints estimate of 
        Jaccard similarity based on matrix.'''
    # need to find top row in d docs for m permutations
    # ~sim = (num matched in both)/(num in both or one)
    # = num matches/(len(1)+len(2)-num matches)
    m = input("Number of permutations:")
    words = set()
    for doc in docs:
        words = words.union(doc)
    n = len(words) # number of unique words in all docs read
    random.seed(1914474)
    hashes = []
    for i in range(m):
        hashes.append([])
        lowest = 4000000
        a = random.randint(1,n-1)
        while a%n ==0 or n%a == 0 or a%2 == 0:
            a = random.randint(1,n-1)
        b = random.randint(0,n-1)
        for doc in docs:
            for word in doc:
                row = (a*word + b)%n
                if row < lowest:
                    lowest = row
            hashes[-1].append(lowest)
    count = 0
    for function in hashes:
        if function[doßc1-1] == function[doc2-1]:
            count+=1
    J_sim = float(count)/m
    print n,count
    print "Estimated Jaccard Similarity between docs %d and %d is: %.3f" %\
        (doc1,doc2,J_sim)
        
    
def main():
    specs = input("Give [num. docs to read],[doc1 id],[doc2 id] (separated by commas):")
    id_1 = specs[1]
    id_2 = specs[2]
    N = specs[0]
    
    data = open('/tmp/docword.enron.txt','r')
    data.next()
    data.next()
    data.next()
    doc = 0
    sets = []
    for i in range(N):
        sets.append(set())
    while doc <=N:
        line = data.next()
        line = line.split(' ')
        doc = eval(line[0])
        if doc <= N:
            sets[doc-1].add(eval(line[1]))
    data.close()
    
    jaccard(sets,id_1,id_2)
    sigmatrix(sets, id_1, id_2)

if __name__ == '__main__':
    main()