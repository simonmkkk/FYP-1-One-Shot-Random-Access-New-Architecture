# Simulation 效能優化文檔

本文檔說明 One-Shot Random Access 模擬的效能優化技術。

---

## 📊 當前性能

- **吞吐量**：~70,000-74,000 樣本/秒
- **10^7 樣本預計耗時**：約 140-145 秒（~2.4 分鐘）
- **記憶體用量**：穩定 ~250-300 MB（滑動窗口模式）

**運行環境**：
- Python 3.14.0 Free-threaded (GIL 已禁用)
- 16 核心 CPU
- ThreadPoolExecutor 並行執行

**進度顯示**：
```
模擬進度:  50%|█████     | 5,000,000/10,000,000 [01:07<01:07, 74,382.15樣本/s]
```

---

## 🔧 已實現的優化技術

### 1. 批量隨機數生成

一次性預生成所有 AC 迭代所需的隨機數，減少函數調用開銷。

```python
# 一次生成 (I_max × M) 的隨機數矩陣
all_random = rng.integers(0, N, (I_max, M))

for ac in range(1, I_max + 1):
    choices = all_random[ac - 1, :remaining]  # 陣列切片，O(1)
```

**原理**：將 `I_max` 次 RNG 調用減少為 1 次，切片操作只建立視圖不複製數據。

---

### 2. Thread-local RNG

每個線程使用獨立的隨機數生成器，避免多線程鎖競爭。

```python
_thread_local = threading.local()

def _get_thread_rng():
    if not hasattr(_thread_local, 'rng'):
        _thread_local.rng = np.random.default_rng()
    return _thread_local.rng

def clear_thread_local_rng():
    """模擬結束後清理，釋放記憶體"""
    global _thread_local
    _thread_local = threading.local()
```

**原理**：Thread-local storage 確保每個線程有獨立的 RNG 實例，模擬結束後清理釋放記憶體。

---

### 3. 純 Python dict 計數

使用 Python dict 替代 `np.bincount`，對稀疏數據更高效。

```python
counts = {}
for c in choices:
    counts[c] = counts.get(c, 0) + 1

success = sum(1 for v in counts.values() if v == 1)
collision = sum(1 for v in counts.values() if v >= 2)
```

**原理**：dict 只存儲實際被選中的 RAO，當 M < N 時比 bincount 更快。

---

### 4. 單樣本並行 + 滑動窗口

每個 worker 執行單個樣本模擬，使用滑動窗口限制同時提交的任務數量。

```python
def _single_sample_worker(args):
    M, N, I_max, idx, results_array = args
    result = simulate_group_paging_single_sample(M, N, I_max)
    results_array[idx] = result
    return idx

# 滑動窗口式任務提交
max_pending = num_workers * 2
while active_futures:
    done, _ = wait(active_futures.keys(), return_when=FIRST_COMPLETED)
    for future in done:
        # 提交新任務填補空缺
        if remaining > 0:
            new_future = executor.submit(_single_sample_worker, new_args)
```

**原理**：
- `wait(FIRST_COMPLETED)` 避免 polling 開銷
- 滑動窗口確保 CPU 始終有任務執行
- 直接寫入共享 array，減少數據拷貝

---

### 5. 預分配結果陣列

在模擬開始前預分配完整的結果陣列，避免動態擴展造成的記憶體碎片。

```python
# 預分配結果陣列
results_array = np.empty((num_samples, 3), dtype=np.float64)

# Worker 直接寫入對應位置
results_array[idx, 0] = result[0]
results_array[idx, 1] = result[1]
results_array[idx, 2] = result[2]
```

**原理**：避免 Python list 的動態擴展和最後的 `np.array()` 轉換。

---

### 6. 即時進度顯示

使用 tqdm 顯示樣本進度，每完成一個樣本即更新。

```python
with tqdm(total=num_samples, desc="模擬進度", unit="樣本",
          bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,.0f}/{total:,.0f} '
                     '[{elapsed}<{remaining}, {rate_fmt}]') as pbar:
    pbar.update(1)  # 每完成一個樣本更新一次
```

---

### 7. 每次 N 迴圈後強制 GC

在 Figure 345 模擬中，每完成一個 N 值的模擬就清理記憶體。

```python
for N in N_range:
    results_array = simulate_group_paging_multi_samples(...)
    # 處理結果...
    
    # 記憶體優化：釋放大型結果陣列並強制 gc
    del results_array
    gc.collect()

# 模擬結束後清理 thread-local RNG
clear_thread_local_rng()
gc.collect()
```

---

## ⚙️ 配置說明

`config/simulation/figure345.yaml`:

```yaml
performance:
  num_samples: 10000000      # 樣本數量 (10^7)
  num_workers: -1            # 並行線程數 (-1 = 所有 CPU 核心)
```

---

## 🚀 未來可優化方向

### Numba JIT 編譯

將核心迴圈編譯為機器碼，預期可獲得 2-5x 額外提升。

```python
from numba import njit, prange

@njit(parallel=True)
def simulate_batch(M, N, I_max, num_samples):
    results = np.empty((num_samples, 3))
    for i in prange(num_samples):
        results[i] = simulate_single(M, N, I_max)
    return results
```

**目前阻礙**：Numba 尚未支援 Python 3.14。

---

### Cython 編譯

將熱點函數編譯為 C 擴展，預期可獲得 3-10x 提升。

**代價**：需要編譯步驟，增加部署複雜度。

---

## 📚 相關文件

- `simulation/core/group_paging.py` - 核心模擬函數（包含所有優化）
- `simulation/figure_simulation/figure345_simulation.py` - Figure 模擬（包含 GC 優化）
- `config/simulation/figure345.yaml` - 性能配置
