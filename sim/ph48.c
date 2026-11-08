// ph48 STEPS : direct simulation of no. 48; at left records in state C count the leading (01) pairs a;
// whenever a drops by more than 100 (a new phase has started) print step, a and the whole tape as 0/1 string
#include <stdio.h>
#include <stdlib.h>
const char*M="1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---";
int main(int c,char**v){ double n=atof(v[1]); unsigned char W[12],N[12]; signed char D[12];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;int k=2*i+b; if(x[0]=='-'){N[k]=255;continue;} W[k]=x[0]-'0';D[k]=x[1]=='R'?1:-1;N[k]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p; int q=0; long lasta=0;
 for(long long s=0;s<n;s++){ int k=2*q+t[p]; if(N[k]==255){printf("HALT %lld\n",s+1);return 0;} t[p]=W[k]; p+=D[k]; q=N[k];
  if(p>hi)hi=p;
  if(p<lo){ lo=p; if(q==2){ long i=lo,a=0; while(i+1<=hi&&t[i]==0&&t[i+1]==1){a++;i+=2;}
     if(a+100<lasta){ printf("%lld %ld ",s+1,a); for(long j=lo;j<=hi;j++)putchar('0'+t[j]); putchar('\n'); fflush(stdout);} lasta=a; } } }
 printf("END\n"); }
