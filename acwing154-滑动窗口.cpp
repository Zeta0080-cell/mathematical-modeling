//acwing154-滑动窗口(单调队列)
#include<bits/stdc++.h>
using namespace std;
const int N=1e6;
int n,k;//n个数字，长度为k的窗口 
int a[N],q[N];

int main()
{
	scanf("%d%d",&n,&k);
	for(int i=0;i<n;i++)
	{
		scanf("%d",&a[i]);
	}
	int hh=0,tt=-1;//队头指针和队尾指针 
	for(int i=0;i<n;i++) 
	{
		if(hh<=tt&&q[hh]<i-k+1)//如果队头元素已经不在当前窗口范围内，则将其从队头移除 
		{
			hh++;//移除越界的元素 
		}
		while(hh<=tt&&a[q[tt]]>=a[i])
		{
			tt--;//移除所有比当前元素ai大的元素的索引 
		}
		q[++tt]=i;
		if(i>=k-1)
		{
			printf("%d ",a[q[hh]]);
		}
	}
	return 0;
} 
