//问题一-位置迭代公式 
#include<bits/stdc++.h>
#define pi 3.14159265358979323846
using namespace std;
float p1;
float theta1;
float theta2;
int d=55;
int l=110;//前后把手中心的距离 
//螺线方程 
float luoxian(float p1,float theta1,float theta2)
{
	float p2;
	p2=p1+d/(2*pi)*(theta2-theta1);
	return p2;
}

int main()
{
	//余弦定理检验 
	return 0;
}
