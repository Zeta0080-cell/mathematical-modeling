#include<bits/stdc++.h>
#define pi 3.14159265358979323846
using namespace std;
float theta;//���� 
//������ʼ�� 
float p=0.55; //�ݾ�(m)
float v0=1;  //(m/s)
float theta0=32*pi/180; //��ʼ�Ƕ�ת��Ϊ���� 
float b=p/(2*pi);

//�ɼ����󼫾�
float R(float theta)
{
	float result;
	result=(p/2*pi)*theta;
	return result;
}

//������ת����ʽ 
float xtrans(float theta,float r)//���뼫�Ǻͼ��� 
{
	float result;
	result=r*cos(theta);
	return result;
}

//���ֺ���
float L_length1(float b,float theta)//����b�ͻ������޻�����
{
	float result;
	result=(b/2)/(theta * std::sqrt(1 + theta * theta) + std::log(std::sqrt(1 + theta * theta) + theta));
	return result;	
} 

float L_length2(int t1,int t2)
{
	float result;
	result=v0*(t2-t1);
	return result;
}

//����ͷ�ļ��ǣ�������������Ͷ�ά���� 
int main()
{
	int t1=30,t2=0;
	float temp1,temp2;
	temp1=L_length2(t2,t1);
	return 0;
}
