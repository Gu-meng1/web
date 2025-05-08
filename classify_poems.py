import json

# 读取原始诗词列表（你爬虫生成的）
with open("poetry_data.json", "r", encoding="utf-8") as f:
    poems = json.load(f)

# 定义关键词映射表
THEME_KEYWORDS = {
    "思乡": ["思乡", "故乡", "家", "归", "夜", "月", "乡"],
    "春天": ["春", "花", "风", "柳", "莺", "燕", "绿"],
    "孤独": ["孤", "寂", "独", "冷", "愁", "清", "影"],
    "友情": ["友", "别", "送", "知己", "相逢", "离", "酒"],
    "爱情": ["情", "爱", "郎", "妾", "相思", "红豆"],
    "山水": ["山", "水", "江", "湖", "云", "峰", "林"]
}

# 分类处理
structured = {k: [] for k in THEME_KEYWORDS}
for poem in poems:
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in poem["text"] for kw in keywords):
            structured[theme].append(poem)

# 移除空分类
structured = {k: v for k, v in structured.items() if v}

# 保存结构化结果
with open("structured_poetry.json", "w", encoding="utf-8") as f:
    json.dump(structured, f, ensure_ascii=False, indent=2)

print("分类完成，已保存为 structured_poetry.json")
