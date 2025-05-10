from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import app

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 更新为 Vite 开发服务器的默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start():
    """启动服务器"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start() 