from zhipuai import ZhipuAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

client = ZhipuAI(api_key="d8d023135e604e2f83c1d746db018be8.P8dGs3AMHmA1HpBC")  # 替换为你自己的 key

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    user_input = req.message.strip()

    try:
        response = client.chat.completions.create(
            model="glm-4",  # 或者你有权限的模型，如 "glm-4-plus"
            messages=[
                {"role": "system", "content": "你是一位温文儒雅的古风诗人，擅长用古诗词表达情感。"},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("API call failed.")
        reply = "AI服务暂时不可用，请稍后再试。"

    return {"reply": reply}
