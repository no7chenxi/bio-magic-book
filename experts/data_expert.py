
import pandas as pd
import numpy as np
import os

class DataExpert:
    """数据专家：负责加载、清洗和初步分析 Excel/CSV 数据。"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_excel_data(self, sheet_name):
        """
        封装自原 forecast_2026.py。
        自动寻找表头并加载运营数据。
        """
        if not os.path.exists(self.file_path):
            return f"Error: 文件 {self.file_path} 不存在。"
            
        # 探测表头行
        df_temp = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None, nrows=10)
        header_row_idx = -1
        for i, row in df_temp.iterrows():
            if "月份" in [str(val).strip() for val in row.values]:
                header_row_idx = i
                break
        
        if header_row_idx == -1:
            return "Error: 未在 Excel 中找到 '月份' 列。"

        self.df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=header_row_idx)
        self.df.columns = [str(c).replace('\n', '').strip() for c in self.df.columns]
        self.df = self.df.dropna(subset=['月份'])
        self.df = self.df[self.df['月份'] != '合计']
        self.df['月份_clean'] = self.df['月份'].apply(lambda x: int(''.join(filter(str.isdigit, str(x)))))
        
        # 确保数值化
        if '月度总金额' in self.df.columns:
            self.df['月度总金额'] = pd.to_numeric(self.df['月度总金额'], errors='coerce').fillna(0)
            
        return f"数据加载成功，共 {len(self.df)} 条记录。"

    def get_baseline(self):
        """计算基准营收"""
        if self.df is None: return None
        return self.df['月度总金额'].mean()

if __name__ == "__main__":
    # 简单的本地测试
    expert = DataExpert("Desktop/桌面 - 七月的MacBook Pro 2/公司/会员合作/2025年运营数据.xlsx")
    # print(expert.load_excel_data('2025年运营数据'))
