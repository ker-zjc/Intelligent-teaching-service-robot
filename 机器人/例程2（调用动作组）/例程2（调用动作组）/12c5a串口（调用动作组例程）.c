#include <STC12C5A60S2.h>
#define uint unsigned int
#define uchar unsigned char
#include <string.h>
sbit qd=P2^0;
void delay(unsigned int cnt);
void UART_init (void)
{ EA = 1;
 ES = 1;
  PCON |= 0x80;  //ʹ�ܲ����ʱ���λSMOD 
  SCON = 0x50;  //8λ����,�ɱ䲨����
   AUXR |= 0x40;  //��ʱ��1ʱ��ΪFosc,��1T 
   AUXR &= 0xfe;  //����1ѡ��ʱ��1Ϊ�����ʷ����� 
   TMOD &= 0x0f;  //�����ʱ��1ģʽλ 
   TMOD |= 0x20;  //�趨��ʱ��1Ϊ8λ�Զ���װ��ʽ 
   TL1 = 0xFA;  //�趨��ʱ��ֵ 
   TH1 = 0xFA;  //�趨��ʱ����װֵ 
   ET1 = 0;  //��ֹ��ʱ��1�ж� 
   TR1 = 1;  //������ʱ��1
   }	  //���ô���ͨѶ�Ĳ����ʣ��������õ���115200��11.0592����
void UART_R (void) interrupt 4  using 1
{   
unsigned char UART_data;  
 RI = 0;     
 UART_data = SBUF; 
  }
  //���ô����жϺ���
  void UART_T (unsigned char UART_data)
  {
     SBUF = UART_data;
	    while(TI == 0);  
		TI = 0;
   }//���ڷ����ַ�����
void UART_TC (unsigned char *str)
{
  while(*str != '\0')
 {  
   UART_T(*str); 
     *str++; 
 } 
	  *str = 0;
 }	//���ڷ����ַ�������
 void main (void)
 {
   UART_init();
   while(1) 
   { 
 
   UART_TC("pl0 sq1 sm100\r");

   delay(90000000000000000000000000000);
  
   }
}//��***��ʾ��Ҫ���͵��ַ���,
void delay(unsigned int cnt)
{
 while(--cnt);
}



