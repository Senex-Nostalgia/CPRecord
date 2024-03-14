---
tags:
  - 分数规划
  - 斜率优化 DP
---

### 题目描述

给你一个长度为 $N$ 的序列 $A=(A_1,A_2,\ldots,A_N)$。
求每个 $k=1,2,\ldots,N$ 的解：

- 当选择一个整数 $r$ 使得 $k\leq r\leq N$ 时，求序列 $A$ 中 $k$-th 到 $r$-th 项的最大平均值。
    这里，序列 $A$ 的 $k$-th 到 $r$-th 项的平均值定义为 $\frac{1}{r-k+1}\displaystyle\sum_{i=k}^r A_i$。

### 输入格式

第一行一个正整数 $N$ $(1\le N\le 2\times 10^5)$，表示序列的长度。

第二行 $N$ 个正整数 $A_1,A_2,\cdots, A_n$ $(1\le A_i\le 10^6)$，表示所给序列。

### 输出格式

输出 $N$ 行。

第 $i$ 行 $(1\le i\le N)$ 表示 $k=i$ 时的答案。

输出的答案被认为是正确的，当且仅当答案与标准答案绝对误差或相对误差小于 $10^{-6}$。

### 题解

二分答案，设当前答案为 $x$，若该答案可行，则：
$$
\begin{aligned}
\frac{1}{r-k+1}\displaystyle\sum_{i=k}^r A_i&\ge x\\
\sum_{i=k}^{r}A_i-(r-k+1)x&\ge 0\\
\sum_{i=k}^{r}(A_i-x)&\ge 0
\end{aligned}
$$
设 $P_i=\displaystyle \sum_{j=i}^{i}A_j$，那么对每个点 $i$ 维护一条直线 $-ix+P_i$，计算 $k$ 的答案时询问 $[k,n]$ 中所有直线在 $x$ 位置的最大值即可。

到这一步就可以计算答案了，也可以转成点的形式：

设第 $i$ 个位置的函数为 $f_i$，若 $i<j$ 且 $f_i(x)>f_j(x)$，则：
$$
\begin{aligned}
f_i(x)-f_j(x)&>0\\
(-ix+P_i)-(-jx+P_j)&>0\\
-(i-j)x&>P_j-P_i\\
x&<\frac{P_i-P_j}{i-j}
\end{aligned}
$$
维护若干个点 $(i,P_i)$ 的上凸包即可，同时插入的 $i$ 单调递减，可以单调队列维护。

### 代码

```cpp
/*
 * Copyright© 2024 Heratino & Nelofus. All rights reserved.
 * author: Heratino & Nelofus
 * Problem: ABC341G. Highest Ratio
 * Tag: 分数规划; 斜率优化 DP
 * Memory Limit: 1024MB
 * Time Limit: 2000ms
 * Source: Toyota Programming Contest 2024#2 (AtCoder Beginner Contest 341)
 * Date: 2024-03-14 
 */

// Narcissus & どうか安寧な記憶を

#include <bits/stdc++.h>
using i64 = long long;
using f64 = double;
using f128 = double;

constexpr int N = 2e5 + 10;
constexpr f64 eps = 1e-9;
int n;
int a[N];
i64 pre[N];
f64 ans[N];

struct Point {
	i64 x, y;
} P[N];
using Vector = Point;
inline Vector trans(const Point &a, const Point &b) {return {b.x - a.x, b.y - a.y};}
inline i64 Cross(const Vector &a, const Vector &b) {return a.x * b.y - a.y * b.x;}
inline int dcmp(const f128 &x) {
	if (fabs(x) < eps)
		return 0;
	return x > 0 ? 1 : -1;
}
inline int dcmp(const f128 &x, const f128 &y) {return dcmp(y - x);}
int q[N], tt;
inline f128 slope(const Point &a, const Point &b) {
	return (f128)(b.y - a.y) / (b.x - a.x);
}

inline bool check(const f128 &x, const i64 &Minus1, const i64 &Minus2) {
	int l = 0, r = tt - 1;
	while (r - l > 3) {
		int mid = l + r >> 1;
		// if (x < slope(P[q[mid]], P[q[mid + 1]]))
		if (x * (P[q[mid + 1]].x - P[q[mid]].x) > P[q[mid + 1]].y - P[q[mid]].y)
			r = mid;
		else
			l = mid;
	}
	f128 maxAns = -1e18;
	for (int i = l; i <= r; i++) {
		i64 t1 = pre[q[i]] - Minus1;
		f128 t2 = (-q[i] - Minus2) * x;
		if (dcmp(t1 + t2) >= 0)
			return true;
	}
	return false;
}

/* 无法忘却的记忆与苍蓝之梦 */
int main() {
#ifdef HeratinoNelofus
	freopen("input.txt", "r", stdin);
#endif
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	std::cin >> n;	
	for (int i = 1; i <= n; i++) {
		std::cin >> a[i];
		pre[i] = pre[i - 1] + a[i];
		P[i] = {i, pre[i]};
	}

	for (int i = n; i >= 1; i--) {
		while (tt > 1 && Cross(trans(P[i], P[q[tt - 2]]), trans(P[i], P[q[tt - 1]])) <= 0)
			tt--;
		q[tt++] = i;
		f128 l = 0, r = 1e9 + 10;
		while (dcmp(l, r) == 1) {
			f64 mid = (l + r) / 2;
			if (check(mid, pre[i - 1], -(i - 1)))
				l = mid;
			else
				r = mid;
		}
		ans[i] = l;
	}
	for (int i = 1; i <= n; i++)
		std::cout << std::fixed << std::setprecision(7) << ans[i] << '\n';
	return 0;
}
```

### 坑点

1.   `long double` 也不太能接受 $10^{11}$ 级别的乘法，特别是你需要精确到小数点后八位。
2.   除法速度比乘法慢多了，能用乘法就别用除法。
3.   斜率从除法变成乘法的时候，注意分母是否为负数，转换过去的时候可能需要翻转不等号。