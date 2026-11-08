# canonical cell-level description of a block-run tape: literal cells and periodic segments (period <= 8),
# independent of the 40-cell block alignment
def minper(s):
    for p in range(1,9):
        if len(s)%p==0 and s==s[:p]*(len(s)//p): return p
    return None
def canon(runs):
    # runs: list of (blockstring, count) from left to right
    segs=[]   # ['L', string] or ['P', unit, ncells]
    def addlit(x):
        if segs and segs[-1][0]=='L': segs[-1][1]+=x
        else: segs.append(['L',x])
    for b,n in runs:
        p=minper(b)
        if n>=3 and p:
            unit=b[:p]
            segs.append(['P',unit,len(b)*n])
        else:
            addlit(b*n)
    # absorb literal cells at the edges of periodic segments, then normalise units to start at segment start
    out=[]
    for i,sg in enumerate(segs):
        out.append(sg)
    # extend periodic segments into neighbouring literals
    for i,sg in enumerate(out):
        if sg[0]!='P': continue
        u=sg[1]; p=len(u)
        # right side
        if i+1<len(out) and out[i+1][0]=='L':
            lit=out[i+1][1]; k=0; ph=sg[2]%p
            while k<len(lit) and lit[k]==u[(ph+k)%p]: k+=1
            sg[2]+=k; out[i+1][1]=lit[k:]
        # left side
        if i>0 and out[i-1][0]=='L':
            lit=out[i-1][1]; k=0
            while k<len(lit) and lit[len(lit)-1-k]==u[(-1-k)%p]: k+=1
            if k:
                out[i-1][1]=lit[:len(lit)-k]; sg[1]=(u*((k//p)+2))[(-k)%p:][:p] if False else None
                # recompute unit starting at the new segment start
                start_shift=(-k)%p
                sg[1]=(u[start_shift:]+u[:start_shift]); sg[2]+=k
    return [tuple(x) for x in out if not (x[0]=='L' and x[1]=='')]
