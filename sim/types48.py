# one-phase map of no. 48 for a phase type (prefix, near tail), no gaps behind, B in [lo,hi):
# for every residue class of B mod 45 (or mod 5 when it suffices) find a law B' = (5B+d)/3, (7B+d)/5 or B+d
# and the type of the next phase; list the halting B
import sys,pickle
from collections import defaultdict
from pmap48 import *
def run(pre,near,lo,hi):
    rows=[]
    for B in range(lo,hi):
        r=step(build(pre,B,near,[]),400.0*B*B+1e6)
        if r[0] in ('HALT','MAX'): rows.append((B,r[0])); continue
        p2,B2,n2,g2=parse(r[1]); rows.append((B,(p2,B2,n2 or '-',tuple(g for g,b in g2))))
    return rows
def laws(rows,m):
    res={}
    for k in range(m):
        sub=[(B,o) for B,o in rows if B%m==k]
        if not sub: continue
        if all(o=='HALT' for B,o in sub): res[k]='HALT'; continue
        if any(isinstance(o,str) for B,o in sub): res[k]='mixed:'+','.join(str(B) for B,o in sub if isinstance(o,str)); continue
        out={(o[0],o[2],len(o[3])) for B,o in sub}
        for name,f in (('5/3',lambda B,B2:3*B2-5*B),('7/5',lambda B,B2:5*B2-7*B),('+',lambda B,B2:B2-B)):
            ds={f(B,o[1]) for B,o in sub}
            if len(ds)==1 and len(out)==1:
                res[k]=(name,ds.pop(),out.pop()); break
        else: res[k]=('?',len(out))
    return res
if __name__=='__main__':
    pre=sys.argv[1]; near=sys.argv[2] if sys.argv[2]!='-' else ''; lo,hi=int(sys.argv[3]),int(sys.argv[4])
    rows=run(pre,near,lo,hi)
    pickle.dump(rows,open('type_%s_%s.pkl'%(pre,near or 'empty'),'wb'))
    print('TYPE',pre,near or '-','HALT B:',[B for B,o in rows if o=='HALT'][:40])
    for m in (5,45):
        L=laws(rows,m)
        unresolved=[k for k,v in L.items() if not (v=='HALT' or (isinstance(v,tuple) and v[0]!='?'))]
        print(' mod',m,':',len(L)-len(unresolved),'classes with one law;', 'unresolved',unresolved[:20])
        if m==5 or len(unresolved)<len(L):
            for k,v in sorted(L.items()):
                if v=='HALT' or (isinstance(v,tuple) and v[0]!='?'): print('   B%%%d=%d: %s'%(m,k,v))
