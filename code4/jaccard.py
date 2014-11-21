import threading
import time

#number of docs
n = 21000
#n = 21000
#length of feature vector
s_n = 2974

#value of k
k=10

print "loading the feature vector in memory"
time1 = time.time()
#loading feature vector
s= []
filename = 'feature_matrix.pytext'

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
  return (i*x + i*2 ) % s_n

sigs = []
documents = []

for i in range(0, n):

  documents.append(set())
  for jj in range(0, s_n -1):
    if s[i][jj] == 1:
      documents[i] |= set([jj])

def jaccard (a, b):
  try:
    return float(len(a & b)) / float(len(a | b))
  except:
    return 1.0



out = [[0 for x in range(n)] for x in range(n)] 

print "Finding the jaccard similarity and saving in file jaccard_dist2.pytext"
file_name = open('jaccard_dist2.pytext', 'w')
for ii in range(0, n):
  print ii
  temp ={}
  temp['ii']=ii
  t=[]
  for jj in range(0, ii):
    t.append(0)
  
  for jj in range(ii, n):
    #if ii != jj:
    t.append(jaccard(documents[ii], documents[jj]))
  
  temp['val']=t   
  print>> file_name, temp
      #out[ii][jj]=jaccard(documents[ii], documents[jj])
      
      #print "Doc", ii+1, "and doc", jj+1, "estimation", jaccard_estimate(sigs[ii], sigs[jj]), "actual", jaccard(documents[ii], documents[jj])
#print "out"
#print out

time2 = time.time()

print ' Program took %0.3f ms' % ((time2-time1)*1000.0)

'''
sum
200.461768888
SSE
0.932380320409
'''


