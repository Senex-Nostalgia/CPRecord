### 题目描述

有一个网格，网格中有 $N$ 行 $N$ 列。让 $(i,j)$ 表示从上面起第 $i$ 行和从左边起第 $j$ 列的方格。

高桥最初在 $(1,1)$ 个方格中的钱为零。

当高桥在 $(i,j)$ 号方格时，他可以在**一次**行动中完成以下其中一项：

- 停留在同一位置并增加 $P_{i,j}$ 的钱数。
- 从他的钱中支付 $R_{i,j}$ 并移动到 $(i,j+1)$ 格。
- 从他的钱中支付 $D_{i,j}$ 并移动到 $(i+1,j)$ 格。

他不会采取会使他的金钱变为负数或使他离开网格的一次行动。

如果高桥采取最优行动，他需要多少次行动才能到达 $(N,N)$ 位置？

### 数据范围

$2 \leq N \leq 80,1 \leq P_{i,j} \leq 10^9$

$1 \leq R_{i,j},D_{i,j} \leq 10^9$

### 题解

考虑DP，最朴素的想法是设 $f(x,y,mx,res)$ 表示当前在 $(x,y)$，路径中最大的值为 $mx$，剩余的钱数为 $res$ 的最小步数，转移平凡。

不难发现每次停留必定是在已经走过的格子中 $P$ 最大的位置，否则在前面停留一定更好，那么我们只用关注 $P$ 递增的子序列，其余的部分我们一定不会在那里停留，所以状态可以优化为 $f(x,y,res)$，若 $P_{c,d}>P_{a,b}$，那么沿着从 $(a,b)$ 到 $(c,d)$ 的最短路移动，计算缺少的钱需要在 $(a,b)$ 处停留多久才能赚够即可。

更进一步地，我们发现其实 $res$ 并不需要维护——假设前面在某个节点处多停留了一天，取得了一些冗余的钱，那我们换成在当前位置 $(a,b)$ 停留一定赚得更多。

所以不需要考虑需不需要多停留若干天赚更多钱，缺少的直接在当前位置赚回来更优，我们只需要尽可能压缩天数即可。

那么现在设 $f(x,y)=(k,res)$ 表示到达 $(x,y)$ 时的最小天数为 $k$，在最小化天数的情况下最多剩下 $res$ 块钱即可转移。

时间复杂度 $\mathcal O(n^4)$。

### 代码

```cpp
/*
 * Copyright© 2024 Heratino & Nelofus. All rights reserved.
 * author: Heratino & Nelofus
 * Problem: ABC344F. Earn to Advance
 * Tag: DP
 * Memory Limit: 1024MiB
 * Time Limit: 4000ms
 * Source: ABC344
 */

// Narcissus & どうか安寧な記憶を

#include <bits/stdc++.h>
using i64 = long long;

constexpr int N = 85;
constexpr i64 inf = 0x3f3f3f3f3f3f3f3f;
int n;
int p[N][N], R[N][N], D[N][N];
std::pair<i64, i64> f[N][N];
i64 dis[N][N];

void solve() {
	std::cin >> n;
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			std::cin >> p[i][j];
	p[n][n] = 1e9 + 10;

	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n - 1; j++)
			std::cin >> R[i][j];
	for (int i = 1; i <= n - 1; i++)
		for (int j = 1; j <= n; j++)
			std::cin >> D[i][j];
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++) {
			auto &[a, b] = f[i][j];
			a = inf;
			b = 0ll;
		}
	f[1][1] = std::make_pair(0ll, 0ll);
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++) {
			memset(dis, 0x3f, sizeof(dis));
			dis[i][j] = 0ll;
			for (int x = i; x <= n; x++)
				for (int y = j; y <= n; y++) {
					dis[x][y] = std::min(dis[x][y], dis[x][y - 1] + R[x][y - 1]);
					dis[x][y] = std::min(dis[x][y], dis[x - 1][y] + D[x - 1][y]);
				}
			for (int x = i; x <= n; x++)
				for (int y = j; y <= n; y++) {
					if (p[x][y] <= p[i][j])
						continue;
					auto &[k, res] = f[i][j];
					i64 need = std::max(0ll, (dis[x][y] - res - 1) / p[i][j] + 1);
					i64 newk = k + need + (x - i) + (y - j);
					i64 neww = res - dis[x][y] + need * p[i][j];
					if (newk < f[x][y].first || (newk == f[x][y].first && neww > f[x][y].second))
						f[x][y] = std::make_pair(newk, neww);
				}
		}
	std::cout << f[n][n].first << '\n';
}

/* 无法忘却的记忆与苍蓝之梦 */
int main() {
#ifdef HeratinoNelofus
	freopen("input.txt", "r", stdin);
#endif
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int T = 1;
	while (T--) {
		solve();
	}
	return 0;
}
```



