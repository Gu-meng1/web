from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jieba
import json
import random
import os

# 加载结构化诗词数据（按主题）
with open("structured_poetry.json", "r", encoding="utf-8") as f:
    POETRY_DB = json.load(f)

# 创建 FastAPI 应用
app = FastAPI()

# 启用跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求数据结构
class ChatRequest(BaseModel):
    message: str

# 会话历史记录（简单记忆）
conversation_history = []

def match_poem(user_words, poems_by_theme):
    matches = []
    for theme, poems in poems_by_theme.items():
        for poem in poems:
            score = 0
            if any(w in poem["text"] for w in user_words):
                score += 2
            if any(w in poem["title"] for w in user_words):
                score += 1
            if any(w in poem["author"] for w in user_words):
                score += 1
            if score > 0:
                matches.append((score, poem))

    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0][1]
    else:
        return None
# 聊天接口
@app.post("/chat")
async def chat(req: ChatRequest):
    user_input = req.message.strip()
    words = jieba.lcut(user_input)

    # 记录用户输入
    conversation_history.append({"role": "user", "text": user_input})
    if len(conversation_history) > 6:
        conversation_history.pop(0)

    # 匹配诗句
    matched_poem = match_poem(words, POETRY_DB)

    if matched_poem:
        reply = f"古人云《{matched_poem['title']}》({matched_poem['author']}): {matched_poem['text']}"
    else:
        reply = "古人未有此问，吾亦难答之。但愿你心中自有明月。"

    conversation_history.append({"role": "bot", "text": reply})
    return {"reply": reply}
