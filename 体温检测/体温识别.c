#include <AT89X52.H>

#include <INTRINS.h>

unsigned char code displaybit[]={0xfe,0xfd,0xfb,0xf7,

0xef,0xdf,0xbf,0x7f};

unsigned char code displaycode[]={0x3f,0x06,0x5b,0x4f,

0x66,0x6d,0x7d,0x07,

0x7f,0x6f,0x77,0x7c,

0x39,0x5e,0x79,0x71,0x00,0x40};

unsigned char code dotcode[32]={0,3,6,9,12,16,19,22,

25,28,31,34,38,41,44,48,

50,53,56,59,63,66,69,72,

75,78,81,84,88,91,94,97};

unsigned char displaycount;

unsigned char displaybuf[8]={16,16,16,16,16,16,16,16};

unsigned char timecount;

unsigned char readdata[8];



sbit DQ=P3^7;

bit sflag;

bit resetpulse(void)

{

unsigned char i;



DQ=0;

for(i=255;i>0;i--);

DQ=1;

for(i=60;i>0;i--);

return(DQ);

for(i=200;i>0;i--);

}



void writecommandtods18b20(unsigned char command)

{

unsigned char i;

unsigned char j;

for(i=0;i<8;i++)

{

if((command & 0x01)==0)

{

DQ=0;

for(j=35;j>0;j--);

DQ=1;

}

else

{

DQ=0;

for(j=2;j>0;j--);

DQ=1;

for(j=33;j>0;j--);

}

command=_cror_(command,1);

}

}



unsigned char readdatafromds18b20(void)

{

unsigned char i;

unsigned char j;

unsigned char temp;



temp=0;

for(i=0;i<8;i++)

{

temp=_cror_(temp,1);

DQ=0;

_nop_();

_nop_();

DQ=1;

for(j=10;j>0;j--);

if(DQ==1)

{

temp=temp | 0x80;

}

else

{

temp=temp | 0x00;

}

for(j=200;j>0;j--);

}

return(temp);

}



void main(void)

{

TMOD=0x01;

TH0=(65536-4000)/256;

TL0=(65536-4000)%256;

ET0=1;

EA=1;



while(resetpulse());

writecommandtods18b20(0xcc);

writecommandtods18b20(0x44);

TR0=1;

while(1)

{

;

}

}



void t0(void) interrupt 1 using 0

{

unsigned char x;

unsigned int result;



TH0=(65536-4000)/256;

TL0=(65536-4000)%256;

if(displaycount==2)

{

P0=displaycode[displaybuf[displaycount]] | 0x80;

}

else

{

P0=displaycode[displaybuf[displaycount]];

}

P2=displaybit[displaycount];

displaycount++;

if(displaycount==8)

{

displaycount=0;

}



timecount++;

if(timecount==150)

{

timecount=0;

while(resetpulse());

writecommandtods18b20(0xcc);

writecommandtods18b20(0xbe);

readdata[0]=readdatafromds18b20();

readdata[1]=readdatafromds18b20();

for(x=0;x<8;x++)

{

displaybuf[x]=16;

}

sflag=0;

if((readdata[1] & 0xf8)!=0x00)

{

sflag=1;

readdata[1]=~readdata[1];

readdata[0]=~readdata[0];

result=readdata[0]+1;

readdata[0]=result;

if(result>255)

{

readdata[1]++;

}

}

readdata[1]=readdata[1]<<4;

readdata[1]=readdata[1] & 0x70;

x=readdata[0];

x=x>>4;

x=x & 0x0f;

readdata[1]=readdata[1] | x;

x=2;

result=readdata[1];

while(result/10)

{

displaybuf[x]=result%10;

result=result/10;

x++;

}

displaybuf[x]=result;

if(sflag==1)

{

displaybuf[x+1]=17;

}

x=readdata[0] & 0x0f;

x=x<<1;

displaybuf[0]=(dotcode[x])%10;

displaybuf[1]=(dotcode[x])/10;

while(resetpulse());

writecommandtods18b20(0xcc);

writecommandtods18b20(0x44);

}

}