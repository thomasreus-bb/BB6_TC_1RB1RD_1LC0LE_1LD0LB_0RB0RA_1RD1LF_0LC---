# compare the tapes dumped at successive restarts (anchors.pkl, written by msim48.py when ANCHORDUMP is set)
import pickle
A=[]
with open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'anchors.pkl','rb') as f:
    while True:
        try: A.append(pickle.load(f))
        except Exception: break
print(len(A),'restarts')
for st,q,d,L,R in A: print(st,q,d,len(L),len(R))
for j in range(len(A)-1):
    R1=[(tuple(b),n) for b,n in reversed(A[j][4])]; R2=[(tuple(b),n) for b,n in reversed(A[j+1][4])]
    k=len(R2)-len(R1)
    diff=[(i,R1[i][1],R2[k+i][1]) for i in range(len(R1)) if R1[i]!=R2[k+i]]
    print('cycle',j,'->',j+1,': new runs',k,'; old part differs at',len(diff),'runs:',diff[:8])
    print('  L',A[j][3],'->',A[j+1][3])
    print('  first new runs',[(''.join(map(str,b)),n) for b,n in R2[:min(k,8)]])
from canon48 import canon
def tape_runs(L,R):
    return [(''.join(map(str,b)),n) for b,n in L]+[(''.join(map(str,b)),n) for b,n in reversed(R)]
C=[canon(tape_runs(a[3],a[4])) for a in A]
for j in range(len(C)):
    lit=[x for x in C[j] if x[0]=='L']
    print('restart',j,'segments',len(C[j]))
for j in range(len(C)-1):
    a,b=C[j],C[j+1]
    k=len(b)-len(a)
    same_tail=sum(1 for i in range(1,len(a)+1) if a[-i]==b[-i])
    print('restart',j,'->',j+1,'segments added',k,'; identical segments counted from the right end:',same_tail,'of',len(a))
    # left part that differs
    print('   new left part:',[ (x[0],x[1][:30],x[2] if len(x)>2 else len(x[1])) for x in b[:len(b)-same_tail]][:12])
    print('   old left part:',[ (x[0],x[1][:30],x[2] if len(x)>2 else len(x[1])) for x in a[:len(a)-same_tail]][:12])
