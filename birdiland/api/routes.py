"""
API路由
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    user_id: str = "default"
    stream: bool = False


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    emotion: str = "neutral"


class StreamResponse(BaseModel):
    """流式响应"""
    content: str
    emotion: str = "neutral"
    is_final: bool = False


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "Birdiland API"}


@router.post("/chat")
async def chat_with_birdiland(request: ChatRequest):
    """与Birdiland聊天"""
    try:
        if request.stream:
            # 流式响应
            async def generate_stream():
                message = request.message
                # 模拟AI生成文本的过程
                words = f"你好！我是Birdiland。你说了：{message}".split()
                
                for i, word in enumerate(words):
                    # 模拟AI思考时间
                    await asyncio.sleep(0.1)
                    
                    # 发送部分响应
                    stream_data = StreamResponse(
                        content=word + " ",
                        emotion="happy",
                        is_final=(i == len(words) - 1)
                    )
                    yield f"data: {stream_data.json()}\n\n"
                
                # 发送结束信号
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/plain; charset=utf-8"
            )
        else:
            # 非流式响应（保持向后兼容）
            response = f"你好！我是Birdiland。你说了：{request.message}"
            
            return ChatResponse(
                response=response,
                emotion="happy"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")


@router.get("/profile")
async def get_birdiland_profile():
    """获取Birdiland的个人资料"""
    return {
        "name": "Birdiland",
        "description": "一个可爱的AI驱动的数字人",
        "personality": "友好、聪明、富有同情心",
        "interests": ["学习新事物", "帮助他人", "艺术创作"]
    }
