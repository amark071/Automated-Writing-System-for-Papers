"""
路由模块，包含所有API路由。

主要组件：
- auth: 认证相关的路由
- writing: 写作相关的路由
- agent: 智能代理相关的路由
- empirical: 实证分析相关的路由
"""

from fastapi import APIRouter
from .auth import router as auth_router
from .writing import router as writing_router
from .agent import router as agent_router
from .empirical import router as empirical_router

# 创建主路由
router = APIRouter()

# 注册子路由
router.include_router(auth_router)
router.include_router(writing_router)
router.include_router(agent_router)
router.include_router(empirical_router)

# 导出主路由
__all__ = ["router"] 