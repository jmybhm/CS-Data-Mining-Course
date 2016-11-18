'''
Part 2 LSH homework.
Laura Colbran and Jimin Yoo
Prints the average similarity of k nearest neighbours and times it for the brute force 
approach and for LSH. 
'''

import random 
import string
import time
from heapq import *

def jaccard(docs,doc1,doc2):
    '''Computes and prints the exact Jaccard similarity between 2 documents.'''
    n = len(docs)
    sim = float(len(docs[doc2].intersection(docs[doc1])))/len(docs[doc2].union(docs[doc1]))
    return sim

def sigmatrix(docs,m):
    '''Computes signature matrix d documents by m permutations.'''
    print ("Building Signature Matrix for LSH")
    print
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
    return hashes
         
def bruteForce(docs, id, k):
    """Calculates Jaccard Similarity between one doc and all others, returns average."""
    neighbors = []
    for i in range(k):
        heappush(neighbors,0)
    count = 1
    for doc in docs:
        if count != id:
            sim = jaccard(docs, (id-1), (count-1))
            heappushpop(neighbors,sim)
        count += 1
    sum = 0
    for j in range(k):
        sum += heappop(neighbors)
    averageSim = sum/k
    return averageSim

def lsh(matrix,docs,k,rows):
    '''returns the average of the average similarity of each doc for k neighbours.
        If #hashes is not evenly divisible by r, the last band has the leftovers.'''
    bands = len(matrix)/rows
    if len(matrix)%rows != 0:
        bands += 1
    num_docs = len(matrix[0])
    dicts = []
    for i in range(bands):
        dicts.append({})
    print ("Comparing tuples for LSH")
    for i in range(num_docs):
        band = 0
        tuple = ()
        for j in range(len(matrix)):
            tuple += (matrix[j][i],)
            if j%rows == (rows-1) or j == (len(matrix)-1):
                if tuple in dicts[band]:
                    dicts[band][tuple].append(i)
                else:
                    dicts[band][tuple] = [i]
                tuple = ()
                band += 1
    random.seed(19283)
    avg_sum = 0
    candidates = []
    for id in range(num_docs):
        candidates.append(set())
    for d in dicts:
        for tup,v in d.iteritems():
            for i in v:
                for j in v:
                    candidates[i].add(j)
    for id in range(len(candidates)): 
        candidates[id].remove(id)
        neighbors = []
        for i in range(k):
            heappush(neighbors,0)
        count = 0
        for c in candidates[id]:
            sim = jaccard(docs, id, c)
            heappushpop(neighbors,sim)
            count += 1
        sum = 0
        if count < k:
            for f in range(k-count):
                rand = random.randint(0,num_docs-1)
                sim = jaccard(docs, id, rand)
                heappushpop(neighbors,sim)                        
        for j in range(k):
            sum += heappop(neighbors)
        avg_sum += sum/k 
        if id%100== 0 and id !=0:
            print ("Done with LSH for 100!")
    average = avg_sum/num_docs
    return average
    
def main():
    N = input("Number of Documents to read: ")
    k = input("Number of Nearest Neighbors: ")
    print
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
    t1 = time.clock()
    id = 1
    sum_brute = 0
    for doc in sets:
        sum_brute += bruteForce(sets,id,k)
        if id%100 == 0:
            print ("Done with Jaccard Similarity for 100!")
        id += 1
    average_brute = sum_brute/len(sets)
    brute_time = time.clock() - t1
    print ("Brute Force: %.4f" % (average_brute))
    print ("Time: %f s" % (brute_time))
    print
    r = input("Number of rows to a band: ")
    numHashes = input("Number of permutations:")  
    print
    t1= time.clock()
    matrix = sigmatrix(sets,numHashes)
    average_lsh = lsh(matrix,sets,k,r)
    lsh_time = time.clock() - t1
    print ("LSH: %.4f" % (average_lsh))
    print ("Time: %f s" % (lsh_time))

if __name__ == '__main__':
    main()