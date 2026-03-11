import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        n = int(data[idx]); idx += 1
        a = [int(data[idx + i]) for i in range(n)]
        idx += n
        if n == 1:
            out.append('0')
            continue
        a.sort()
        score = sum(a) - n * a[0]
        best = score
        delta_base = a[n - 1] + a[0]
        for k in range(2, n):
            score += delta_base - 2 * a[k - 1]
            if score > best:
                best = score
        out.append(str(best))
    sys.stdout.write('\n'.join(out) + '\n')

main()
