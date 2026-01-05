"""
簡單計時器模組

提供簡潔的層級計時功能，用於測量程序各部分的執行時間。

Input: 計時器名稱
Output: 樹狀時間報告
Position: 性能監測的簡化替代方案

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import json
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class SimpleTimer:
    """
    簡單的層級計時器
    
    用法:
        timer = SimpleTimer("Figure 1 完整流程")
        
        with timer.step("解析計算") as t:
            t.record("N=3 計算", duration)
            t.record("N=6 計算", duration)
        
        with timer.step("繪圖"):
            plot_figure1()
        
        timer.print_report()
    """
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.steps: List[Dict[str, Any]] = []
        self._current_step: Optional[Dict[str, Any]] = None
    
    @contextmanager
    def step(self, name: str):
        """
        開始一個計時步驟
        
        用法:
            with timer.step("解析計算") as t:
                # 執行代碼
                t.record("N=3", 0.01)  # 可選：記錄子項
        """
        step_data = {
            'name': name,
            'start_time': time.time(),
            'end_time': None,
            'duration': 0.0,
            'children': [],
        }
        self._current_step = step_data
        
        try:
            yield self
        finally:
            step_data['end_time'] = time.time()
            step_data['duration'] = step_data['end_time'] - step_data['start_time']
            self.steps.append(step_data)
            self._current_step = None
    
    def record(self, name: str, duration: float):
        """
        記錄一個子項的時間（用於已有計時的情況）
        
        Args:
            name: 子項名稱
            duration: 持續時間（秒）
        """
        if self._current_step is not None:
            self._current_step['children'].append({
                'name': name,
                'duration': duration,
            })
    
    def finish(self) -> float:
        """結束計時，返回總時間"""
        self.end_time = time.time()
        return self.end_time - self.start_time
    
    def get_total_duration(self) -> float:
        """獲取總時間"""
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
    
    def print_report(self):
        """打印樹狀時間報告"""
        if self.end_time is None:
            self.finish()
        
        total = self.get_total_duration()
        
        print(f"\n{'='*60}")
        print(f"性能報告: {self.name}")
        print(f"{'='*60}")
        print(f"總時間: {_format_duration(total)}")
        print(f"\n時間分布:")
        
        for i, step in enumerate(self.steps):
            is_last = (i == len(self.steps) - 1)
            prefix = "└── " if is_last else "├── "
            child_prefix = "    " if is_last else "│   "
            
            # 計算百分比
            percent = (step['duration'] / total * 100) if total > 0 else 0
            print(f"{prefix}{step['name']}: {_format_duration(step['duration'])} ({percent:.1f}%)")
            
            # 打印子項
            for j, child in enumerate(step['children']):
                is_last_child = (j == len(step['children']) - 1)
                child_marker = "└── " if is_last_child else "├── "
                print(f"{child_prefix}{child_marker}{child['name']}: {_format_duration(child['duration'])}")
        
        print(f"{'='*60}\n")
    
    def save_json(self, output_dir: Optional[str] = None) -> str:
        """
        保存數據到 JSON 文件
        
        Args:
            output_dir: 輸出目錄（默認 result/performance/{timestamp}）
        
        Returns:
            JSON 文件路徑
        """
        if self.end_time is None:
            self.finish()
        
        # 創建輸出目錄
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / 'result' / 'performance' / timestamp
        else:
            output_dir = Path(output_dir) / timestamp
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 準備數據
        data = {
            'name': self.name,
            'total_duration': self.get_total_duration(),
            'total_duration_formatted': _format_duration(self.get_total_duration()),
            'steps': [
                {
                    'name': step['name'],
                    'duration': step['duration'],
                    'duration_formatted': _format_duration(step['duration']),
                    'percent': (step['duration'] / self.get_total_duration() * 100) if self.get_total_duration() > 0 else 0,
                    'children': [
                        {
                            'name': child['name'],
                            'duration': child['duration'],
                            'duration_formatted': _format_duration(child['duration']),
                        }
                        for child in step['children']
                    ],
                }
                for step in self.steps
            ],
            'timestamp': datetime.now().isoformat(),
        }
        
        # 保存文件
        json_path = output_dir / 'performance_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 性能數據已保存: {json_path}")
        return str(json_path)


def _format_duration(seconds: float) -> str:
    """格式化時間顯示"""
    if seconds < 0.01:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


# 全局計時器實例（用於簡單場景）
_current_timer: Optional[SimpleTimer] = None


def start_timer(name: str) -> SimpleTimer:
    """開始一個新的計時器"""
    global _current_timer
    _current_timer = SimpleTimer(name)
    return _current_timer


def get_timer() -> Optional[SimpleTimer]:
    """獲取當前計時器"""
    return _current_timer


def clear_timer():
    """清除當前計時器"""
    global _current_timer
    _current_timer = None

