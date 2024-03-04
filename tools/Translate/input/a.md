sadgxcasfd
sagdasfxcvad

sadgsafd

sa
df
```cpp
#include <bits/stdc++.h>
using i64 = long long;

int main() {
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int T;
	std::cin >> T;
	while (T--) {
		int n;
		i64 d;
		std::cin >> n >> d;
		std::vector<i64> a(n);
		for (auto &x : a)	std::cin >> x;
		std::sort(a.begin(), a.end());

		std::priority_queue<i64> q;
		i64 ans = 0;
		for (int i = 0; i < n; i++) {
			i64 pos = a[i] - i * d;
			if (pos < 0)
				ans += -pos, pos = 0;
			if (!q.empty() && pos < q.top()) {
				ans += q.top() - pos;
				q.pop();
				q.push(pos);
			}
			q.push(pos);
		}
		std::cout << ans << '\n';
	}
	return 0;
}
```
```cpp
#include <bits/stdc++.h>
using i64 = long long;

int main() {
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int T;
	std::cin >> T;
	while (T--) {
		int n;
		i64 d;
		std::cin >> n >> d;
		std::vector<i64> a(n);
		for (auto &x : a)	std::cin >> x;
		std::sort(a.begin(), a.end());

		std::priority_queue<i64> q;
		i64 ans = 0;
		for (int i = 0; i < n; i++) {
			i64 pos = a[i] - i * d;
			if (pos < 0)
				ans += -pos, pos = 0;
			if (!q.empty() && pos < q.top()) {
				ans += q.top() - pos;
				q.pop();
				q.push(pos);
			}
			q.push(pos);
		}
		std::cout << ans << '\n';
	}
	return 0;
}
```


## Others

一些模拟和补题存在了本地，或者是加密了。

如果是加密了的可以找我要密码？没人会看就是了。
