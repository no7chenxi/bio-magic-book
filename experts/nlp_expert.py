
import csv
import re
from collections import Counter
import os

class NLPExpert:
    """文本专家：负责挖掘关键词、标签和 N-grams 频率。"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.tag_counter = Counter()
        self.stopwords = {'视频', '内容', '大家', '一个', '这个', '我们', '可以', '关注'}

    def get_ngrams(self, text, n):
        text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
        if len(text) < n: return []
        return [text[i:i+n] for i in range(len(text)-n+1)]

    def analyze_tags(self):
        """
        封装自原 analyze_word_freq.py。
        统计 CSV 中的标签热度。
        """
        if not os.path.exists(self.file_path):
            return f"Error: 文件 {self.file_path} 不存在。"

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) < 2: continue
                    tags = row[1]
                    if tags:
                        clean_tags = tags.replace('，', ',').split(',')
                        for tag in clean_tags:
                            t = tag.strip()
                            if t and t not in self.stopwords:
                                self.tag_counter[t] += 1
            return f"分析完成，找到 {len(self.tag_counter)} 个唯一标签。"
        except Exception as e:
            return f"Error: {e}"

    def get_top_tags(self, n=20):
        return self.tag_counter.most_common(n)

if __name__ == "__main__":
    # 简单的本地测试
    expert = NLPExpert("/Users/july/Desktop/桌面 - 七月的MacBook Pro 2/2025卡车内容数据0127.csv")
    # print(expert.analyze_tags())
