//����ģ��-���5
#include<bits/stdc++.h>
using namespace std;
const int N=1e6;
int a[N],d[N];

int main()
{
	int n,m;
	int l,r,c;
	cin>>n>>m;
	for(int i=1;i<=n;i++)
	{
		scanf("%d",&a[i]);//���������� 
	}
	for(int i=1;i<=n;i++)
	{
		d[i]=a[i]-a[i-1];	
	}
	while(m--)
	{
		cin>>l>>r>>c;
		d[l]+=c;
		d[r+1]-=c;
	}
	for(int i=1;i<=n;i++)//����ǰ׺��������������� 
	{
		d[i]+=d[i-1];
	}
	for(int i=1;i<=n;i++)
	{
		printf("%d ",d[i]);
	}
	return 0;
} 
