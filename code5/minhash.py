import threading
import time

#number of docs
n = 21000

#length of feature vector
s_n = 2974

#value of k
k= 16


time1 = time.time()
s= []
filename = 'feature_matrix.pytext'
print "loading feature vector in memory"

i=0
for line in open(filename):
    record = eval(line)
    temp = map(int, list(record['feature_vector']))
    s.append(temp)
    
    if i >= n-1:
      break
    i =i+1

#hashing function    
def h(x,i):
  return (i*x + i ) % s_n


#creating permutations
permutations =[[]]*k
for x in range(0,k):
  temp =[]
  for i in range(0, s_n):
    temp.append(h(x,i))
  permutations[x]=temp

#finding minhash values
def minhash (permutation, document):
  foundindex = 9999
  permutation = permutations[permutation]
  for ii in range(0, s_n):
    if s[document][ii] == 1:
      if permutation[ii] < foundindex:
        foundindex = permutation[ii]
  return foundindex

sigs = []
documents = []

sig_time = time.time()

print "calculating signatures for docs"
for i in range(0, n):
  temp =[]
  for x in range (0,k):
    temp.append(minhash(x, i))
 # print "Signature of doc: ", i+1, ":", temp
  sigs.append(temp)
  documents.append(set())
  for jj in range(0, s_n):
    if s[i][jj] == 1:
      documents[i] |= set([jj])

sig_time2 =time.time()


def jaccard (a, b):
  try:
    return float(len(a & b)) / float(len(a | b))
  except:
    return 1.0

def jaccard_estimate (a, b):
  same = 0
  try:
    for i in range(0, k):
      if a[i] == b[i]: same += 1
    return float(same) / k
  except:
    return 1.0


#uncomment these lines to load from the jaccard similarity file
'''
print "loading the jaccard similarity from file"
out = [[0 for x in range(n)] for x in range(n)] 

file_name = 'jaccard_dist2.pytext'


for line in open(file_name):
  record = eval(line)
  ii = record['ii']
  #print ii
  val = list(record['val'])
  out[ii] = val
  #for i in range (0,n):
  #  out[ii][i] = val[i]
   # orig = jaccard(documents[ii], documents[i])
  if ii >= n-1:
    break

'''

#print out
sse_arr= []

def calc(start,end,t):
  
  sum_val = 0
  for ii in range(start, end):
    for jj in range(ii, n):
      if ii != jj:
        
        pred=jaccard_estimate(sigs[ii], sigs[jj])
        original=jaccard(documents[ii], documents[jj])
        #uncomment this line to load from the file
        #original = out[ii][jj]
        err=  abs((original-pred)**(2))
        sum_val = sum_val + err
  sse_arr.append(sum_val)


v = n/2
print "Calculating MSE for all docs"

#creating threads to speed up comparisons
t1 = threading.Thread(target=calc, args = (0,n/4,0))
t1.start()

t2 = threading.Thread(target=calc, args = (n/4,n/2,0))
t2.start()

t3 = threading.Thread(target=calc, args = (n/2,3*n/4,0))
t3.start()

t4 = threading.Thread(target=calc, args = (3*n/4,n,0))
t4.start()



t1.join()
t2.join()
t3.join()
t4.join()

sum_val = sum (sse_arr)
#print "\nsum"
#print sum_val 


print "Number of docs : %s" %(n)
print "K:  %s" %(k)

den = (n*(n-1))/2
fin =sum_val/den
print 'MSE is %0.5f ' % (fin)
time2 = time.time()
print 'Program took %0.3f ms' % ((time2-time1)*1000.0)
print 'Min Hasing took %0.3f ms' % ((sig_time2-sig_time)*1000.0)


