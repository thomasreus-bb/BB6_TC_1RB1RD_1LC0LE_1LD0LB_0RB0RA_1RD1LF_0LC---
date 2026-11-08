# phase map of no. 48: parse a phase-start tape into (prefix, B, near tail, list of (gap, block)) and back
import re,subprocess
def parse(s):
    m=re.match(r'^(010101|0100)((?:1001)+)(.*)$',s)
    pre,blk,rest=m.groups(); B=len(blk)//4
    parts=re.split(r'(0{20,})',rest)
    return pre,B,parts[0],[(len(parts[i]),parts[i+1]) for i in range(1,len(parts)-1,2)]
def build(pre,B,near,gaps):
    return pre+'1001'*B+near+''.join('0'*g+b for g,b in gaps)
def step(tape,lim=1e12):
    out=subprocess.run(['./step48',str(lim)],input=tape,capture_output=True,text=True).stdout.split()
    if out[0] in ('HALT','MAX'): return out[0],int(out[1]) if len(out)>1 else None
    return int(out[0]),out[1]
