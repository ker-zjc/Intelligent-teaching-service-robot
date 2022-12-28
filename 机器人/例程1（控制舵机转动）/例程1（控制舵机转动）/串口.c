#include <STC12C5A60S2.h>
#define uint unsigned int
#define uchar unsigned char
#include <string.h>   
sbit p1=P1^0;
sbit p2=P1^1;
void UART_init (void)
{ 
EA = 1; 
ES = 1; 
PCON |= 0x80;  //ʹ�ܲ����ʱ���λ
SCON = 0x50;  //8λ����,�ɱ䲨���� 
AUXR |= 0x40;  //��ʱ��1ʱ��ΪFosc,��1T 
AUXR &= 0xfe;  //����1ѡ��ʱ��1Ϊ�����ʷ����� 
TMOD &= 0x0f;  //�����ʱ��1ģʽλ
TMOD |= 0x20;  //�趨��ʱ��1Ϊ8λ�Զ���װ��ʽ 
TL1 = 0xFA;  //�趨��ʱ��ֵ 
TH1 = 0xFA;  //�趨��ʱ����װֵ 
ET1 = 0;  //��ֹ��ʱ��1�ж� 
TR1 = 1;  //������ʱ��1
}

 void DELAY_MS (uint z)
{ 
	uint x,y;
	for(x=z;x>0;x--)
		for(y=110;y>0;y--);
}
void UART_R (void) interrupt 4  using 1
{   
     unsigned char UART_data;   
     RI = 0;
     UART_data = SBUF;  
}

void UART_T (unsigned char UART_data)
{
   SBUF = UART_data;
   while(TI == 0);
   TI = 0;   
}

void UART_TC (unsigned char *str)
{
  while(*str != '\0') 
  {
     UART_T(*str);
     *str++;
  } 
  *str = 0; 
}
void main (void)
{
  UART_init();
  while(1)
 {
   if(p1==0)
   {UART_TC("#16P1000#24P2000T2000\r\n");
  DELAY_MS (1500);}
   if(p2==0)
   {UART_TC("#16P1800#24P1000T2000\r\n");
  DELAY_MS (1500);}
 }
}
