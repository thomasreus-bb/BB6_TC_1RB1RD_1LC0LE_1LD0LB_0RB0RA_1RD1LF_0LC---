# Lin-recurrence (translated cycler) check for no. 48 from the exact restart dumps written by phase48m.py (TCDUMP):
# restart i and i+1 are left records in state C. During the cycle between them the head never comes closer than
# minR cells to the right end of the tape, i.e. it visits at most W = total_i - minR cells counted from the left edge.
# If the first W cells (from the left edge) at restart i equal the first W cells at restart i+1, and the state is the
# same, the cycle repeats forever (the head never reads anything else) and the machine never halts.
# The comparison is exact and cell by cell; long runs of equal 40-cell blocks are compared block-wise.
import sys,pickle
D=[]
with open(sys.argv[1],'rb') as f:
    while True:
        try: D.append(pickle.load(f))
        except Exception: break
class Stream:
    def __init__(s,runs): s.runs=runs; s.i=0; s.off=0   # off = cells already consumed in run i
    def cur(s):
        b,n=s.runs[s.i]; return b,n
    def remaining_in_run(s):
        b,n=s.cur(); return len(b)*n-s.off
    def cell(s):
        b,n=s.cur(); return b[s.off%len(b)]
    def advance(s,k):
        s.off+=k
        while s.i<len(s.runs) and s.off>=len(s.runs[s.i][0])*s.runs[s.i][1]:
            s.off-=len(s.runs[s.i][0])*s.runs[s.i][1]; s.i+=1
    def rotated_block(s):
        b,n=s.cur(); o=s.off%len(b); return b[o:]+b[:o]
def equal_prefix(r1,r2,W):
    a=Stream(r1); b=Stream(r2); pos=0
    while pos<W:
        if a.i>=len(a.runs) or b.i>=len(b.runs): return pos   # tape ended (blank beyond) - treat as end of comparison
        ra=a.remaining_in_run(); rb=b.remaining_in_run(); ba,_=a.cur(); bb,_=b.cur()
        if ra>=2*len(ba) and rb>=2*len(bb) and len(ba)==len(bb) and a.rotated_block()==b.rotated_block():
            k=min(ra,rb)-len(ba); k=min(k,W-pos)
            if k>0: a.advance(k); b.advance(k); pos+=k; continue
        if a.cell()!=b.cell(): return pos
        a.advance(1); b.advance(1); pos+=1
    return None
for i,(st,q,runs,total,minR) in enumerate(D):
    print('restart',i,'step',st,'state','ABCDEF'[q],'cells from head',total,'| min cells right of head since previous restart',minR)
for i in range(len(D)-1):
    st1,q1,r1,t1,_=D[i]; st2,q2,r2,t2,minR=D[i+1]
    W=t1-minR+100          # cells visited during the cycle, plus a safety margin of 100 cells
    d=equal_prefix(r1,r2,W)
    print('cycle %d->%d: period %d steps, shift %d cells, visited W=%d of %d cells; states %s; first %d cells: %s'%(
        i,i+1,st2-st1,t2-t1,W,t1,'equal' if q1==q2 else 'DIFFERENT',W,'EQUAL' if d is None else 'differ at cell %d'%d))
