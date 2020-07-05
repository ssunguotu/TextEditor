#include <iostream>
#include<Windows.h>
#include<vector>
#include <queue>
using namespace std;

int maze[4][6] = { {1, 1, 0, 0, 0, 0},
				   {0, 1, 1, 1, 0, 0},
				   {1, 1, 0, 1, 0, 0},
				   {0, 0, 0, 1, 0, 0} };
vector<pair<int, int> > path;
int dir[4][2] = { {0, 1}, {1, 0}, {0, -1}, {-1, 0} };
bool search(vector<pair<int, int> > tpath, int x, int y)

{
	if (x < 0 || y < 0 || x > 3 || y > 5)//越界返回 
		return false;
	if (x == 3 && y == 3)
	{
		tpath.push_back(make_pair(3, 3));
		path = tpath; //如果找到了出口,则记录下路径
		return true;
	}
	for (int ix = 0; ix < 4; ix++)//四个方向搜索 
	{
		if (maze[x + dir[ix][0]][y + dir[ix][1]] == 1)
		{
			tpath.push_back(make_pair(x, y));
			if (!search(tpath, x + dir[ix][0], y + dir[ix][1]))
				tpath.pop_back();
			else
				return true;
		}
	}
	return false;
}

void test1()
{
	vector<pair<int, int> > tpath;
	search(tpath, 0, 0);//从开始点找起 
	for (auto i : path)
	{
		cout << i.first << "  " << i.second << endl;
	}
}

//****************************************************
//八皇后递归解法
class QueenSolution
{
	vector<int> queen; // 例如queen[2] = 1, 则表示第2列的行数为1。
	int count = 0;
	int N;

public:
	QueenSolution(int num = 8)
	{
		queen.resize(num, -1); // 初始值设定为-1
		N = num;
	}

	int getCount()
	{
		findSpace(0);
		return count;
	}

private:
	bool isSafe(int row, int column) { //判断某个皇后是否与已有皇后冲突
		for (int i = 0; i < column; i++) {
			if (row == queen[i])return false; //同行
			if ((row + column) == (i + queen[i]))return false;//副对角线
			if ((row - column) == (queen[i] - i))return false;//主对角线
		}
		return true;
	}

	void findSpace(int column) {//在第column列找能放皇后的位置
		for (int i = 0; i < N; i++) {//从1~N遍历这一列的N个空位
			if (isSafe(i, column)) {
				queen[column] = i;  //记录下皇后的位置
				if (column == N-1) {  //如果N个皇后都放满了统计一下
					count++;
					return;
				}
				findSpace(column + 1); //递归放下一列的皇后
			}
		}
		if(column)
			queen[--column] = -1; //回溯，重置标记
		return;	
	}
};


void test2() {
	DWORD startTime = GetTickCount();//计时开始
	cout << QueenSolution(8).getCount() << endl;
	DWORD endTime = GetTickCount();//计时结束
	cout << "用时：" << endTime - startTime << "ms" << endl;
}


//**************************************************
// 骑士游历问题
class KnightSolution
{
	int maze[8][8]{ 0 };
	bool isSolved = false;
	int dir[8][2] = { { -2, 1 }, { 2, 1 }, {-2, -1}, {2, -1}, {-1, 2},{1, 2}, { -1, -2 },{1, -2 } };
public:
	vector<pair<int, int>> getSolution(int x, int y) 
	{
		dfs(x, y);
		return tmpPath;
	}

private:
	vector<pair<int, int> > tmpPath; 
	void dfs(int x, int y)//参数用来表示状态
	{
		if (x < 0 || x > 7 || y < 0 || y > 7 || maze[x][y])
			return;
		if (tmpPath.size() == 64 - 1 )
		{
			tmpPath.push_back(make_pair(x, y));
			isSolved = true;
			return;
		}
		maze[x][y] = 1; //标记
		tmpPath.push_back(make_pair(x, y));
		for (int ix = 0; ix < 8; ix++)
		{
			auto x_ = x + dir[ix][0];
			auto y_ = y + dir[ix][1];
			if (!(x_ < 0 || x_ > 7 || y_ < 0 || y_ > 7 || maze[x_][y_] != 0))
			{
				dfs(x_, y_);
				if (isSolved) //剪枝
					return;
				maze[x_][y_] = 0;//还原标记
				tmpPath.pop_back();
			}

		}
	}
};

void test3()
{
	cout << "请输入起点：";
	int x = 0, y = 0;
	cin >> x >> y;
	auto vec = KnightSolution().getSolution(x, y);
	for (auto it = vec.begin(); it != vec.end();)
	{
		for (int i = 0; i < 8; i++)
		{
			cout << it->first << it->second << "  ";
			it++;
		}
		cout << endl;
	}
}

//***************************************
//倒水问题
class PourSolution
{
	int sizeMaxA, sizeMaxB, target;//分别表示两个杯子的最大容量,n表示目标值。
	int(*rem)[1000] = new int[1000][1000];
	int cnt = 0;

	struct node
	{
		int a, b;//代表着a杯和b杯当前的水量
		vector  <int> ans; //操作序列
	};


	void bfs(int x, int y) {
		auto translate = [](int i)->string {
			switch (i)
			{
			case 1:
				return "将a倒满";
			case 2:
				return "将b倒满";
			case 3:
				return "将a清空";
			case 4:
				return "将b清空";
			case 5:
				return "将a倒入b中";
			case 6:
				return "将b倒入a中";
			default:
				break;
			}
		};
		memset(rem, 0, sizeof(rem));//重置数组
		queue  <node> que;//搜索队列
		node rootNode;
		rootNode.a = x;
		rootNode.b = y;
		que.push(rootNode);
		while (1) {
			node temp;
			temp = que.front();//从队头取出一个搜索状态
			que.pop();
			cnt++;//计数

			//终止条件
			if (temp.b == target || temp.a == target) {
				cout << "总步数为：" << temp.ans.size() << " " << endl;
				cout << "步骤为：" << endl;
				for (int i = 0; i < temp.ans.size(); i++) {
					cout << i + 1 << "." + translate(temp.ans[i]) << endl;//输出解
				}
				break;
			}
			if (cnt >= 10e6)
			{
				cout << "No solution." << endl;
				break;
			}
			if (temp.a != sizeMaxA) { 
				node later = temp;
				later.a = sizeMaxA;
				later.ans.push_back(1); 
				if (!rem[later.a][later.b]) { 
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}

			if (temp.b != sizeMaxB) {
				node later = temp;
				later.b = sizeMaxB;
				later.ans.push_back(2);
				if (!rem[later.a][later.b]) {
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}

			if (temp.a != 0) {
				node later = temp;
				later.a = 0;
				later.ans.push_back(3);
				if (!rem[later.a][later.b]) {
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}

			if (temp.b != 0) {
				node later = temp;
				later.b = 0;
				later.ans.push_back(4);
				if (!rem[later.a][later.b]) {
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}

			
			if (temp.b != 0 && temp.a != sizeMaxB) {
				node later = temp;
			if (later.b > sizeMaxA - later.a) {
					later.b -= sizeMaxA - later.a;
					later.a = sizeMaxA;
				}
				else {
					later.a += later.b;
					later.b = 0;
				}
				later.ans.push_back(5);
				if (!rem[later.a][later.b]) {
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}

			if (temp.a != 0 && temp.b != sizeMaxB) {
				node later = temp;
				if (later.a > sizeMaxB - later.b) {
					later.a -= sizeMaxB - later.b;
					later.b = sizeMaxB;
				}
				else {
					later.b += later.a;
					later.a = 0;
				}
				later.ans.push_back(6);
				if (!rem[later.a][later.b]) {
					que.push(later);
					rem[later.a][later.b] = 1;
				}
			}
		}
	}

public:
	PourSolution()
	{
		
		cin >> sizeMaxA >> sizeMaxB >> target;
		if (target > sizeMaxA&& target > sizeMaxB)
		{
			cout << "No solution." << endl;
			return;
		}
		bfs(0, 0); 
	}
	~PourSolution()
	{
		delete[] rem;
	}
};

void test4()
{
	PourSolution();
}

int main()
{
	test1();
	//test2();
	//test3();
	//test4();
}