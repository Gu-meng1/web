import requests
from bs4 import BeautifulSoup
import json
import time

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 主页面：唐诗三百首
LIST_URL = "https://so.gushiwen.cn/gushi/tangshi.aspx"
BASE_URL = "https://so.gushiwen.cn"

def get_poem_links():
    response = requests.get(LIST_URL, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select(".typecont span a")
    return [BASE_URL + link['href'] for link in links]

def get_poem_detail(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.select_one(".cont h1").text.strip()
    author = soup.select_one(".cont .source a").text.strip()
    content = soup.select_one(".cont .contson").text.strip().replace(" ", "").replace("\n", "")
    
    return {
        "title": title,
        "author": author,
        "text": content
    }

def main():
    poems = []
    links = get_poem_links()
    print(f"共获取到 {len(links)} 首诗链接")

    for i, link in enumerate(links):
        try:
            poem = get_poem_detail(link)
            poems.append(poem)
            print(f"[{i+1}] 成功获取：{poem['title']} - {poem['author']}")
            time.sleep(1)  # 避免访问过快被封
        except Exception as e:
            print(f"[{i+1}] 抓取失败：{link}，错误：{e}")

    # 保存到 JSON 文件
    with open("poetry_data.json", "w", encoding="utf-8") as f:
        json.dump(poems, f, ensure_ascii=False, indent=2)
    print("所有诗词已保存为 poetry_data.json")

if __name__ == "__main__":
    main()
