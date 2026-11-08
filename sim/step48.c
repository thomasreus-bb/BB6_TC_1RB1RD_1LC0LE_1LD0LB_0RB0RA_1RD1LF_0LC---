// step48 [MAXSTEPS] < TAPE : TAPE (stdin) is a 0/1 string; the head stands on its first cell in state C (a left record).
// Runs no. 48 directly until the next left record in state C whose tape starts with 010101(1001)^k or 0100(1001)^k, k>=10,
// followed by at most 64 cells before the first run of 20 zeros (or the end of the tape).
// Prints: steps and the new tape (0/1 string, trailing zeros removed), or HALT steps, or MAX.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*M="1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---";
int main(int c,char**v){ static char T[1<<26]; if(scanf("%s",T)!=1) return 1; double lim=c>1?atof(v[1]):1e12; unsigned char W[12],N[12]; signed char D[12];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;int k=2*i+b; if(x[0]=='-'){N[k]=255;continue;} W[k]=x[0]-'0';D[k]=x[1]=='R'?1:-1;N[k]=x[2]-'A';}
 long L=strlen(T); long SZ=4*L+(1L<<22); unsigned char*t=calloc(SZ,1); long base=SZ/2-L; for(long i=0;i<L;i++)t[base+i]=T[i]-'0';
 long p=base,lo=base,hi=base+L-1; int q=2;
 for(long long s=0;s<lim;s++){ int k=2*q+t[p]; if(N[k]==255){printf("HALT %lld\n",s+1);return 0;} t[p]=W[k]; p+=D[k]; q=N[k];
  if(p>hi)hi=p;
  if(p<lo){ lo=p; if(q==2){ long i=lo; int ok=0;
     if(t[i]==0&&t[i+1]==1&&t[i+2]==0&&t[i+3]==1&&t[i+4]==0&&t[i+5]==1) i+=6, ok=1;
     else if(t[i]==0&&t[i+1]==1&&t[i+2]==0&&t[i+3]==0) i+=4, ok=1;
     if(ok){ long kk=0; while(t[i]==1&&t[i+1]==0&&t[i+2]==0&&t[i+3]==1){kk++;i+=4;}
       long j=i, z=0; while(j<=hi && z<20){ z = t[j]? 0 : z+1; j++; } long nearlen=(j-z)-i;
       if(kk>=10 && nearlen<=64){ long e=hi; while(e>lo&&!t[e])e--; printf("%lld ",s+1); for(long j=lo;j<=e;j++)putchar('0'+t[j]); putchar('\n'); return 0; } } } } }
 printf("MAX\n"); }
