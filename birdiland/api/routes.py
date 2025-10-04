"""
API路由
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

from ..agent import birdiland_agent

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
                full_response = ""
                async for chunk in birdiland_agent.chat_stream(request.message, request.user_id):
                    full_response += chunk
                    
                    # 分析情感
                    emotion = birdiland_agent.analyze_emotion(full_response)
                    
                    # 发送部分响应
                    stream_data = StreamResponse(
                        content=chunk,
                        emotion=emotion,
                        is_final=False
                    )
                    yield f"data: {stream_data.model_dump_json()}\n\n"
                
                # 发送最终响应
                final_emotion = birdiland_agent.analyze_emotion(full_response)
                stream_data = StreamResponse(
                    content="",
                    emotion=final_emotion,
                    is_final=True
                )
                yield f"data: {stream_data.model_dump_json()}\n\n"
                
                # 发送结束信号
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/plain; charset=utf-8"
            )
        else:
            # 非流式响应
            response = await birdiland_agent.chat(request.message, request.user_id, stream=False)
            emotion = birdiland_agent.analyze_emotion(response)
            
            return ChatResponse(
                response=response,
                emotion=emotion
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
