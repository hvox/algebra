#include <bits/stdc++.h>
using namespace std;

const int max_difference = 20;

int main() {
  string s1, s2; cin >> s1 >> s2;
  int m = s1.length(), n = s2.length();
  if (abs(n - m) > max_difference) {
    cout << "difference is too big to be measured..." << endl;
    return 0;
  }
  int arr0[max_difference*2+1], arr1[max_difference*2+1]; int *v0 = arr0, *v1 = arr1;
  for (int j = 0; j <= max_difference; j++) v0[max_difference + j] = j;
  for (int i = 0; i < m; i++) {
    // TODO: is this if necessary? Isn't it covered in the next loop?
    if (-1 + max_difference - i >= 0)
      v1[-1 + max_difference - i] = i + 1;
    for (int real_j = 0; real_j < 41; real_j++) {
      int j = real_j - max_difference + i;
      int cost1 = real_j < 2*max_difference ? v0[real_j + 1] + 1 : 321;
      int cost2 = real_j > 0 ? v1[real_j - 1] + 1 : 321;
      int cost3 = 321; if (j >= 0 and j <= n - 1) cost3 = v0[real_j] + (s1[i] == s2[j] ? 0 : 1);
      v1[real_j] = min(cost1, min(cost2, cost3));
    }
    swap(v0, v1);
  }
  int difference =  v0[max_difference - m + n];
  if (difference <= max_difference)
    cout << "difference = " << difference << endl;
  else
    cout << "difference is too big to be measured..." << endl;
  return 0;
}
