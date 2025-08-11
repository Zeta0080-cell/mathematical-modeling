#include<bits/stdc++.h>
#define pi 3.14159265358979323846
using namespace std;
float theta;//极角 
//参数初始化 
float p=0.55; //螺距(m)
float v0=1;  //(m/s)
float theta0=32*pi/180; //初始角度转换为弧度 
float b=p/(2*pi);

//由极角求极径
float R(float theta)
{
	float result;
	result=(p/2*pi)*theta;
	return result;
}

//极坐标转换公式 
float xtrans(float theta,float r)//传入极角和极径 
{
	float result;
	result=r*cos(theta);
	return result;
}

//积分函数
float L_length1(float b,float theta)//传入b和积分上限或下限
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

//求龙头的极角，极径，极坐标和二维坐标 
int main()
{
	int t1=30,t2=0;
	float temp1,temp2;
	temp1=L_length2(t2,t1);
	return 0;
}
