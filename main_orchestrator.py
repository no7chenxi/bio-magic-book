
from experts.data_expert import DataExpert
from experts.nlp_expert import NLPExpert
import pandas as pd
import numpy as np
import os

class GenosOrchestrator:
    """Genos 总调度器：协调多个专家进行综合预测。"""
    
    def __init__(self, data_file, nlp_file):
        # 自动调整路径，处理本地与脚本路径的关系
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_expert = DataExpert(data_file)
        self.nlp_expert = NLPExpert(nlp_file)
        
    def run_full_analysis(self):
        print("\n" + "="*40)
        print("   GENOS 业务专家委员会 - 2026 战略报告")
        print("="*40)
        
        # 1. 调用数据专家 (使用最新的全量货车调研数据)
        # 注意：这里我们使用 Sheet1 作为默认表名
        res_data = self.data_expert.load_excel_data('Sheet1')
        print(f"[数据专家] {res_data}")
        
        # 2. 调用 NLP 专家
        res_nlp = self.nlp_expert.analyze_tags()
        print(f"[内容专家] {res_nlp}")
        
        # 3. 综合预测逻辑
        print("\n" + "-"*15 + " 决策层洞察 " + "-"*15)
        
        # 获取最热门的标签
        top_tags = self.nlp_expert.get_top_tags(15)
        tag_list = [w for w, c in top_tags]
        print(f"核心关键词: {', '.join(tag_list[:8])}...")
        
        # 模拟业务增长逻辑
        growth_multiplier = 1.0
        if any(keyword in tag_list for keyword in ['电瓶', '新能源', '续航', '配件']):
            growth_multiplier += 0.15
            print(">> 【预警】内容热点显示'新能源/配件'需求激增，2026 业务增长潜力 +15%！")
        
        if '会员' in tag_list:
            growth_multiplier += 0.05
            print(">> 【机会】'会员'粘性增强，预期复购率提升。")
            
        print(f">> 最终确定的 2026 综合增长系数: {growth_multiplier:.2f}")

        # 营收预估逻辑 (如果数据专家成功加载)
        if self.data_expert.df is not None:
            # 尝试获取 2025 的月度均值 (如果列名匹配)
            if '月度总金额' in self.data_expert.df.columns:
                avg_rev = self.data_expert.df['月度总金额'].mean()
                print(f"\n--- 财务预估 ---")
                print(f"2025 月均营收基准: {avg_rev:,.2f}")
                print(f"2026 预估年营收 (含趋势修正): {avg_rev * 12 * growth_multiplier:,.2f}")
            else:
                print("\n[系统提示] 数据文件中缺少'月度总金额'列，已跳过财务预估，转为纯趋势分析。")
        
        print("\n" + "="*40)
        print("   分析完成。祝你在 2026 开启'战斗模式'！")
        print("="*40)

if __name__ == "__main__":
    # 更新后的路径
    DATA_PATH = "/Users/july/货车调研_全量最新版.xlsx"
    NLP_PATH = "/Users/july/Desktop/桌面 - 七月的MacBook Pro 2/2025卡车内容数据0127.csv"
    
    orchestrator = GenosOrchestrator(DATA_PATH, NLP_PATH)
    orchestrator.run_full_analysis()
