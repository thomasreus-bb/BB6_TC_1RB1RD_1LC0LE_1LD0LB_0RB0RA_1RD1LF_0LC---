# Accelerated simulator for no. 48 (1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---)
# - tape as runs of 4-cell blocks, Ligocki-style chain steps (a whole run is crossed in one step)
# - "Bell" acceleration: after every macro step the shape (state, direction and block sequence of the whole tape) is compared with its
#   previous occurrences; if the run lengths changed by the same vector twice and the step increments
#   grow linearly, the same change is applied k times at once (k chosen so that every shrinking run keeps a margin).
#   This acceleration is not a proof; it is checked against direct simulation (see chk48.py).
import sys
M='1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---'
TT={}
for i,g in enumerate(M.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]
        TT[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
import os
BS=int(os.environ.get("BS48","12"))
ZERO=(0,)*BS
_tc={}
def trans(q,d,blk):
    key=(q,d,blk)
    if key in _tc: return _tc[key]
    t=list(blk); p=0 if d=='R' else BS-1; s=0
    while 0<=p<BS:
        tr=TT[(q,t[p])]
        if tr is None: r=('HALT',s+1,tuple(t),p); _tc[key]=r; return r
        t[p]=tr[0]; p+=tr[1]; q=tr[2]; s+=1
        if s>10000: raise Exception('loop in block')
    r=(tuple(t),q,'R' if p>=BS else 'L',s); _tc[key]=r; return r
def push(st,blk,n):
    if st and st[-1][0]==blk: st[-1][1]+=n
    else: st.append([blk,n])
class Sim:
    def __init__(s):
        s.L=[];s.R=[];s.minR=None;s.chained=False;s.edgehook=None;s.anchor=None;s.hist3={};s.cyclejumps=0;s.q=0;s.d='R';s.steps=0;s.hist={};s.halt=None;s.events=0;s.jumps=0
    def edge(s):
        # the head moves left into the leftmost block (or into blank tape): simulate that block cell by cell,
        # so that every left record can be shown to s.edgehook(s, cells, p, state, steps)
        # (cells[p:] followed by the runs of s.R is the tape from the head on)
        if s.L:
            t=list(s.L.pop()[0]); minp=s.leftmin
        else:
            t=[0]*BS; minp=BS
        p=BS-1; q=s.q; st=0
        while 0<=p<BS:
            if p<minp:
                minp=p
                s.edgehook(s,t,p,q,s.steps+st)
            tr=TT[(q,t[p])]
            if tr is None:
                s.halt=s.steps+st+1; return False
            t[p]=tr[0]; p+=tr[1]; q=tr[2]; st+=1
        s.steps+=st; s.q=q
        if p>=BS: s.L.append([tuple(t),1]); s.d='R'; s.leftmin=minp
        else: push(s.R,tuple(t),1); s.d='L'
        return True
    def macro(s):
        if s.edgehook and s.d=='L' and (not s.L or (len(s.L)==1 and s.L[0][1]==1)): return s.edge()
        if s.d=='R':
            src,dst=s.R,s.L
        else:
            src,dst=s.L,s.R
        if not src: src.append([ZERO,1<<62])   # blank side: a practically infinite run of zero blocks
        blk,n=src[-1]
        r=trans(s.q,s.d,blk)
        if r[0]=='HALT':
            s.halt=(s.steps+r[1]); return False
        nb,nq,nd,st=r
        if nq==s.q and nd==s.d and blk!=ZERO or (nq==s.q and nd==s.d and n<(1<<61)):
            # chain: cross the whole run
            src.pop(); push(dst,nb,n); s.steps+=st*n
            s.chained=True
        else:
            if n==1: src.pop()
            else: src[-1][1]-=1
            if nd==s.d: push(dst,nb,1)
            else: push(src,nb,1)
            if s.d=='R' and nd=='L' and s.minR is not None:
                # the head turned inside block blk; cells right of the turning point >= cells in R
                c=sum(x[1] for x in s.R)*BS-BS   # R already contains the turning block again
                if c<s.minR: s.minR=c
            s.q=nq; s.d=nd; s.steps+=st
        # normalise the blank runs
        for side in (s.L,s.R):
            if side and side[0][0]==ZERO and side[0][1]>=(1<<61): side.pop(0)
        return True
    def shape(s):
        return (s.q,s.d,tuple(b for b,n in s.L),tuple(b for b,n in s.R))
    def counts(s):
        return [n for b,n in s.L]+[n for b,n in s.R]
    def runs(s):
        return s.L+s.R
    def event(s):
        # called after every macro step: look for a shape that recurs with linearly changing run lengths
        s.events+=1
        sh=s.shape(); c=s.counts()
        if len(s.hist)>20000: s.hist={}      # keep memory bounded
        h=s.hist.setdefault(sh,[])
        h.append((c,s.steps))
        if len(h)>13: h.pop(0)
        for p in (1,2,3,4):
            if len(h)<3*p+1: break
            C=[x[0] for x in h[-(3*p+1)::p]]; T=[x[1] for x in h[-(3*p+1)::p]]   # 4 samples, p apart
            d=[[b-a for a,b in zip(C[i],C[i+1])] for i in range(3)]
            if not (d[0]==d[1]==d[2] and any(d[0])): continue
            inc=[T[i+1]-T[i] for i in range(3)]
            dd=inc[1]-inc[0]
            if inc[2]-inc[1]!=dd: continue
            k=None
            for cnt,dl in zip(C[3],d[2]):
                if dl<0:
                    kk=(cnt-2*(-dl)-2)//(-dl)
                    k=kk if k is None else min(k,kk)
            if k is None or k<2: continue
            for r,dl in zip(s.runs(),d[2]): r[1]+=dl*k
            s.steps+= k*inc[2] + dd*k*(k+1)//2
            s.jumps+=1
            s.hist[sh]=[]
            return
    def anchor_event(s,key):
        # called at a macro boundary right after a marked moment (e.g. a restart of the small sub-run);
        # if the whole tape shape recurs there with the same change of run lengths 3 times, jump k cycles
        sh=(key,)+s.shape(); c=s.counts()
        if key[1]==807:
            import hashlib
            import pickle,os
            with open(os.environ.get('ANCHORDUMP','/dev/null'),'ab') as f: pickle.dump((s.steps,s.q,s.d,[list(x) for x in s.L],[list(x) for x in s.R]),f)
            print('ANCHOR807 steps',s.steps,'state',s.q,s.d,'nL',len(s.L),'nR',len(s.R),'shapehash',hashlib.md5(repr(sh).encode()).hexdigest()[:10],
                  'L',[(''.join(map(str,b)),n) for b,n in s.L],'R(from head)',[(''.join(map(str,b)),n) for b,n in reversed(s.R)][-14:],flush=True)
        h=s.hist3.setdefault(sh,[])
        h.append((c,s.steps))
        if len(h)>4: h.pop(0)
        if key[1]==807 and len(h)>=2:
            dd0=[b-a for a,b in zip(h[-2][0],h[-1][0])]
            print('ANCHOR807 occurrences',len(h),'steps',s.steps,'step diff',h[-1][1]-h[-2][1],'changed runs',[(i,x) for i,x in enumerate(dd0) if x],'runs',len(c),'state',s.q,s.d,flush=True)
        if len(h)<4: return
        C=[x[0] for x in h]; T=[x[1] for x in h]
        d=[[b-a for a,b in zip(C[i],C[i+1])] for i in range(3)]
        if not (d[0]==d[1]==d[2] and any(d[0])): return
        inc=[T[i+1]-T[i] for i in range(3)]; dd=inc[1]-inc[0]
        if inc[2]-inc[1]!=dd: return
        k=None
        for cnt,dl in zip(C[3],d[2]):
            if dl<0:
                kk=(cnt-10*(-dl)-1000)//(-dl)
                k=kk if k is None else min(k,kk)
        if k is None or k<2: return
        for r,dl in zip(s.runs(),d[2]): r[1]+=dl*k
        s.steps+= k*inc[2] + dd*k*(k+1)//2
        s.cyclejumps+=1; s.jumps+=1
        s.hist3[sh]=[]
    def run(s,maxsteps,cb=None):
        while s.steps<maxsteps:
            if s.d=='L' and not s.L and cb: cb(s)
            s.chained=False
            if not s.macro(): return 'HALT'
            if s.anchor is not None:
                key=s.anchor; s.anchor=None; s.anchor_event(key)
            s.event()
        return 'MAX'
def tape_str(s):
    out=[]
    for b,n in s.L: out.append(''.join(map(str,b))*n)
    left=''.join(out)
    out=[]
    for b,n in reversed(s.R): out.append(''.join(map(str,b))*n)
    return left,''.join(out)
if __name__=='__main__':
    import time
    sim=Sim(); t0=time.time()
    r=sim.run(float(sys.argv[1]))
    print(r,'steps',sim.steps,'events',sim.events,'jumps',sim.jumps,'%.1fs'%(time.time()-t0))
    print([(''.join(map(str,b)),n) for b,n in reversed(sim.R)][:30])
