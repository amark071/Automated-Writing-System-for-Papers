"""
论文自动化写作系统后端模块

主要组件：
- app: FastAPI应用程序实例
- routes: API路由模块
  - empirical_result: 实证分析结果路由
  - discussion: 讨论部分路由
  - conclusion: 结论部分路由
- utils: 工具函数模块
"""

from fastapi import FastAPI
from .routes import router

# 创建FastAPI应用实例
app = FastAPI(
    title="论文自动化写作系统",
    description="基于大语言模型的智能写作辅助系统",
    version="1.0.0"
)

# 注册路由
app.include_router(router)

# 导出应用实例
__all__ = ["app"] 