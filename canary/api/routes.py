"""
API路由
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    user_id: str = "default"


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    emotion: str = "neutral"


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "Canary API"}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_canary(request: ChatRequest):
    """与Canary聊天"""
    try:
        # 这里将集成AI模型
        response = f"你好！我是Canary。你说了：{request.message}"
        
        return ChatResponse(
            response=response,
            emotion="happy"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")


@router.get("/profile")
async def get_canary_profile():
    """获取Canary的个人资料"""
    return {
        "name": "Canary",
        "description": "一个可爱的AI驱动的数字人",
        "personality": "友好、聪明、富有同情心",
        "interests": ["学习新事物", "帮助他人", "艺术创作"]
    }
