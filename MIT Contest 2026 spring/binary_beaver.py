import json
import os
import sys
import time

NEG = -10**30
DEBUG_LOG_PATH = os.path.join(os.path.dirname(__file__), "debug-14ad07.log")
DEBUG_LOG_PATH_CWD = os.path.join(os.getcwd(), "debug-14ad07.log")
DEBUG_SESSION_ID = "14ad07"


def debug_log(run_id: str, hypothesis_id: str, location: str, message: str, data: dict) -> None:
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    line = json.dumps(payload, separators=(",", ":")) + "\n"
    try:
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    if DEBUG_LOG_PATH_CWD != DEBUG_LOG_PATH:
        try:
            with open(DEBUG_LOG_PATH_CWD, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass


def ints():
    data = sys.stdin.buffer.read()
    num = 0
    in_num = False
    for b in data:
        if 48 <= b <= 57:
            num = num * 10 + (b - 48)
            in_num = True
        elif in_num:
            yield num
            num = 0
            in_num = False
    if in_num:
        yield num


def solve() -> None:
    run_id = str(time.time_ns())
    # #region agent log
    debug_log(
        run_id,
        "H0",
        "binary_beaver.py:43",
        "logger_paths",
        {"script_log_path": DEBUG_LOG_PATH, "cwd_log_path": DEBUG_LOG_PATH_CWD},
    )
    # #endregion
    all_data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    t = all_data[p]
    p += 1
    out = []

    # #region agent log
    debug_log(run_id, "H1", "binary_beaver.py:41", "solve_start", {"t": t})
    # #endregion

    for tc in range(t):
        tc_start = time.perf_counter_ns()
        n = all_data[p]
        q = all_data[p + 1]
        k = all_data[p + 2]
        p += 3

        arr = all_data[p:p + n]
        p += n

        left = [-1]
        right = [-1]
        cnt = [0]
        best = [0]
        score = [0]  # score[node] = cnt[node] + best[node], except root cnt is kept 0.
        path = [0] * (k + 1)
        apply_calls = 0
        node_creations = 0
        build_start = time.perf_counter_ns()

        def apply_value(x: int, delta: int) -> None:
            nonlocal apply_calls, node_creations
            apply_calls += 1
            cur = 0
            path[0] = 0
            y = x

            for d in range(k):
                if y & 1:
                    nxt = right[cur]
                    if nxt == -1:
                        nxt = len(left)
                        left.append(-1)
                        right.append(-1)
                        cnt.append(0)
                        best.append(0)
                        score.append(0)
                        right[cur] = nxt
                        node_creations += 1
                else:
                    nxt = left[cur]
                    if nxt == -1:
                        nxt = len(left)
                        left.append(-1)
                        right.append(-1)
                        cnt.append(0)
                        best.append(0)
                        score.append(0)
                        left[cur] = nxt
                        node_creations += 1
                cur = nxt
                cnt[cur] += delta
                path[d + 1] = cur
                y >>= 1

            leaf = path[k]
            if cnt[leaf] == 0:
                best[leaf] = 0
                score[leaf] = 0
            else:
                best[leaf] = NEG
                score[leaf] = NEG

            for d in range(k - 1, -1, -1):
                node = path[d]
                l = left[node]
                r = right[node]
                lv = 0 if l == -1 else score[l]
                rv = 0 if r == -1 else score[r]
                b = lv if lv >= rv else rv
                best[node] = b
                score[node] = b if node == 0 else cnt[node] + b

        for v in arr:
            apply_value(v, 1)

        build_ms = (time.perf_counter_ns() - build_start) / 1e6
        out.append(str(best[0]))
        query_start = time.perf_counter_ns()

        for _ in range(q):
            i = all_data[p] - 1
            v = all_data[p + 1]
            p += 2
            old = arr[i]
            if old != v:
                apply_value(old, -1)
                apply_value(v, 1)
                arr[i] = v
            out.append(str(best[0]))
        query_ms = (time.perf_counter_ns() - query_start) / 1e6

        # #region agent log
        debug_log(
            run_id,
            "H2_H3_H4_H5_H7",
            "binary_beaver.py:132",
            "testcase_metrics",
            {
                "tc": tc + 1,
                "n": n,
                "q": q,
                "k": k,
                "nodes": len(left),
                "apply_calls": apply_calls,
                "node_creations": node_creations,
                "build_ms": build_ms,
                "query_ms": query_ms,
                "total_ms": (time.perf_counter_ns() - tc_start) / 1e6,
            },
        )
        # #endregion

    # #region agent log
    debug_log(run_id, "H1", "binary_beaver.py:151", "solve_end", {"outputs": len(out)})
    # #endregion
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
