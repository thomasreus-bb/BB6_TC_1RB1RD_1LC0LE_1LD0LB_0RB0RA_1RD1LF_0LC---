// at48 FILE : FILE has one step number per line (increasing). Direct simulation of no. 48; at each listed step
// print: step state tape (the tape trimmed of leading/trailing zeros) and the head offset from the first 1
#include <stdio.h>
#include <stdlib.h>
const char*M="1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---";
int main(int c,char**v){ FILE*f=fopen(v[1],"r"); unsigned char W[12],N[12]; signed char D[12];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;int k=2*i+b; if(x[0]=='-'){N[k]=255;continue;} W[k]=x[0]-'0';D[k]=x[1]=='R'?1:-1;N[k]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p; int q=0; long long s=0, target;
 while(fscanf(f,"%lld",&target)==1){
  for(;s<target;s++){ int k=2*q+t[p]; if(N[k]==255){printf("HALT %lld\n",s+1);return 0;} t[p]=W[k]; p+=D[k]; q=N[k]; if(p<lo)lo=p; if(p>hi)hi=p; }
  long a=lo; while(a<hi&&!t[a])a++; long e=hi; while(e>a&&!t[e])e--;
  printf("%lld %c %ld ",s,'A'+q,p-a); for(long j=a;j<=e;j++)putchar('0'+t[j]); putchar('\n'); fflush(stdout); }
}
