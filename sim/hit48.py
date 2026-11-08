# halting chance of a restart phase of no. 48: prefix 010101, empty near tail, B = 0 mod 5, one gap G = ratio*B (+-5 %)
# followed by the marker X; B random in [lo,hi)
import sys,random
from pmap48 import *
X='1'+'100'*3+'0110011001'
lo,hi,n,ratio,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5])
random.seed(seed); h=[]; out={}
for i in range(n):
    B=5*random.randrange(lo//5,hi//5); G=int(ratio*B*random.uniform(0.95,1.05))
    r=step(build('010101',B,'',[(G,X)]),300.0*B*B+1e6)
    if r[0]=='HALT': h.append((B,G))
print('ratio %.3f B in [%d,%d): %d samples, %d HALT (%.1f %%)'%(ratio,lo,hi,n,len(h),100*len(h)/n),h,flush=True)
