# real-run phase starts of no. 48 from the accelerated simulator: at every left record in state C test whether the
# tape starts with 010101(1001)^B or 0100(1001)^B (B >= 10) followed by a near tail of at most 64 cells before
# 20 zeros; print step, prefix, B, near tail, length of the first gap of zeros ('inf' = end of tape)
import sys,time,os,pickle
from msim48 import Sim,BS
def cells(t,p,R):
    for c in t[p:]: yield c
    for b,n in reversed(R):
        if n>3:
            yield ('RUN',b,n)
        else:
            for _ in range(n):
                for c in b: yield c
class Reader:
    # reads cells one by one from the generator, expanding runs lazily; can skip whole periodic runs
    def __init__(s,g): s.g=g; s.buf=[]; s.run=None
    def peekrun(s):
        return s.run
    def next(s):
        while True:
            if s.buf: return s.buf.pop()
            if s.run:
                b,n=s.run; s.run=(b,n-1) if n>1 else None
                s.buf=list(reversed(b)); continue
            x=next(s.g,None)
            if x is None: return 0
            if isinstance(x,tuple): s.run=(x[1],x[2]); continue
            return x
out=[]
def hook(sim,t,p,q,steps):
    if q!=2: return
    R=sim.R
    rd=Reader(cells(t,p,R))
    first=[rd.next() for _ in range(6)]
    if first==[0,1,0,1,0,1]: pre='010101'; pend=[]
    elif first[:4]==[0,1,0,0]: pre='0100'; pend=first[4:]
    else: return
    # count 1001 units
    B=0; pat=[1,0,0,1]; seq=pend[:]
    while True:
        while len(seq)<4:
            if not rd.buf and not rd.run:
                x=next(rd.g,None)
                if isinstance(x,tuple): rd.run=(x[1],x[2])
                elif x is not None: rd.buf=[x]
            if not rd.buf and rd.run:
                b,n=rd.run; j=len(seq)
                if b==tuple((pat[j:]+pat[:j])*(BS//4)): B+=n*(BS//4); rd.run=None; continue
            seq.append(rd.next())
        if seq==pat: B+=1; seq=[]
        else: break
    if B<10: return
    # near tail: cells until 20 zeros
    near=seq[:]; z=0
    for c in near: z=z+1 if c==0 else 0
    while z<20 and len(near)<200:
        c=rd.next(); near.append(c); z=z+1 if c==0 else 0
    if len(near)>64+20: return
    near=near[:len(near)-20]
    zs=20
    while near and near[-1]==0: near.pop(); zs+=1
    # length of the first gap (zeros up to the next 1); 'inf' if the tape ends
    g=zs; ZB=tuple([0]*BS)
    while True:
        if not rd.buf and rd.run and rd.run[0]==ZB: g+=rd.run[1]*BS; rd.run=None; continue
        if not rd.buf and not rd.run:
            x=next(rd.g,None)
            if x is None: g='inf'; break
            if isinstance(x,tuple): rd.run=(x[1],x[2]); continue
            rd.buf=[x]
        c=rd.next()
        if c==1: break
        g+=1
        if g>10**40: g='inf'; break
    out.append((steps,pre,B,''.join(map(str,near)),g))
    if B<5000: sim.anchor=(pre,B,''.join(map(str,near)))
    if B==807 and pre=='010101' and not near and os.environ.get('TCDUMP'):
        # exact tape at the restart (a left record in state C): cells from the head, as runs
        runs=[(''.join(map(str,t[p:])),1)]+[(''.join(map(str,b)),n) for b,n in reversed(sim.R)]
        total=len(t)-p+sum(n for b,n in sim.R)*BS
        with open(os.environ['TCDUMP'],'ab') as f: pickle.dump((steps,q,runs,total,sim.minR),f)
        print('RESTART step',steps,'cells from head',total,'min cells right of head in the previous cycle',sim.minR,flush=True)
        sim.minR=10**60   # small phase: candidate anchor for a whole restart cycle
    print('PH %d %s %d %s %s'%(steps,pre,B,''.join(map(str,near)) or '-',g),flush=True)
if __name__=='__main__':
    sim=Sim(); sim.edgehook=hook; t0=time.time()
    r=sim.run(float(sys.argv[1]))
    print(r,sim.steps if r!='HALT' else sim.halt,'%.0fs'%(time.time()-t0),'cycle jumps',sim.cyclejumps)
