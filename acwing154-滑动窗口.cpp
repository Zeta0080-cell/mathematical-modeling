//acwing154-��������(��������)
#include<bits/stdc++.h>
using namespace std;
const int N=1e6;
int n,k;//n�����֣�����Ϊk�Ĵ��� 
int a[N],q[N];

int main()
{
	scanf("%d%d",&n,&k);
	for(int i=0;i<n;i++)
	{
		scanf("%d",&a[i]);
	}
	int hh=0,tt=-1;//��ͷָ��Ͷ�βָ�� 
	for(int i=0;i<n;i++) 
	{
		if(hh<=tt&&q[hh]<i-k+1)//�����ͷԪ���Ѿ����ڵ�ǰ���ڷ�Χ�ڣ�����Ӷ�ͷ�Ƴ� 
		{
			hh++;//�Ƴ�Խ���Ԫ�� 
		}
		while(hh<=tt&&a[q[tt]]>=a[i])
		{
			tt--;//�Ƴ����бȵ�ǰԪ��ai���Ԫ�ص����� 
		}
		q[++tt]=i;
		if(i>=k-1)
		{
			printf("%d ",a[q[hh]]);
		}
	}
	return 0;
} 
