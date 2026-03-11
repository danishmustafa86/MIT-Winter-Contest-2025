#include <iostream>
#include <vector>
#include <set>

using namespace std;
using ll = long long;

void solve() {
    int n, q;
    cin >> n >> q;
    
    vector<ll> a(n + 1);
    int k = (n + 1) / 2; // Size of the Left half (BB's natural domain)

    ll sumL = 0, sumR = 0;
    multiset<ll> L, R;

    // Read initial array and populate our sets
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        if (i <= k) {
            sumL += a[i];
            L.insert(a[i]);
        } else {
            sumR += a[i];
            R.insert(a[i]);
        }
    }

    // Helper lambda to calculate and print the score in O(1) time
    auto print_ans = [&]() {
        ll mL = *L.begin();
        ll mR = *R.begin();
        ll bb = sumL;
        ll ss = sumR;

        if (n % 2 == 0) {
            // Even N: BB forces the trade if it benefits him
            if (mR > mL) {
                bb = sumL - mL + mR;
                ss = sumR - mR + mL;
            }
        } else {
            // Odd N: SS forces the trade if it benefits her
            if (mL > mR) {
                bb = sumL - mL + mR;
                ss = sumR - mR + mL;
            }
        }
        cout << bb << " " << ss << "\n";
    };

    // Print for the initial state
    print_ans();

    // Process Q modifications
    while (q--) {
        int x;
        ll v;
        cin >> x >> v;

        if (x <= k) {
            // Update Left half
            L.erase(L.find(a[x])); // Crucial: use find() to only erase ONE instance
            sumL -= a[x];
            a[x] = v;
            L.insert(a[x]);
            sumL += a[x];
        } else {
            // Update Right half
            R.erase(R.find(a[x]));
            sumR -= a[x];
            a[x] = v;
            R.insert(a[x]);
            sumR += a[x];
        }
        
        // Print state after modification
        print_ans();
    }
}

int main() {
    // Standard fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}