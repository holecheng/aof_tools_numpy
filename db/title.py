from dataclasses import dataclass


@dataclass
class Title:
    group: str = '分类列名'
    group_key: str = '分类值'
    allowance: str = '分类裕量'
    avg_ev: str = '平均期望ev'
    avg_flop_ev: str = '平均结果flop_ev'
    avg_turn_ev: str = '平均结果turn_ev'
    avg_outcome: str = '平均结果outcome'
    diff_ev_outcome: str = 'outcome-ev差'
    counts: str = '总局数'
    avg_flop_i: str = '平均购买flop保险'
    avg_turn_i: str = '平均购买turn保险'



