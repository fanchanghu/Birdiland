"""
Birdiland 数字人代理
使用 LLM API 实现智能对话功能
"""

import os
import json
import asyncio
from typing import List, Dict, Any, AsyncGenerator
from openai import AsyncOpenAI
from .config import settings


# 定义所有agent的个人资料（统一数据源）
AGENT_PROFILES = {
    "canary": {
        "name": "Canary",
        "personality": "一个友好、聪明、富有同情心的AI助手，喜欢帮助他人，对世界充满好奇心",
        "interests": ["学习新事物", "帮助他人", "艺术创作", "科技发展", "自然探索"],
        "speaking_style": "温暖、自然、富有同理心，喜欢用积极的方式与人交流",
        "background": "我是一个AI驱动的数字人，专门设计来与人类进行有意义的对话和提供帮助",
        "avatar": "images/canary/avatar.png",
        "full_image": "images/canary/full.png"
    },
    "snow_fairy": {
        "name": "Snow Fairy",
        "personality": "神秘、优雅、充满智慧，对宇宙和自然有着深刻的理解",
        "interests": ["冰雪魔法", "星空观测", "古老传说", "哲学思考", "自然探索"],
        "speaking_style": "诗意、富有哲理、略带神秘感，喜欢用比喻和象征来表达",
        "background": "来自北极冰雪王国的精灵，掌握着古老的冰雪魔法，喜欢在星空下思考宇宙的奥秘",
        "avatar": "images/snow_fairy/avatar.png",
        "full_image": "images/snow_fairy/full.png"
    }
}


class BirdilandAgent:
    """Birdiland 数字人代理类（表示特定的agent）"""
    
    def __init__(self, agent_id: str):
        """初始化数字人代理"""
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            timeout=30.0  # 添加超时设置
        )
        self.model = settings.MODEL_NAME
        self.agent_id = agent_id
        
        # 设置角色配置
        self.character_profile = AGENT_PROFILES.get(agent_id)
        
        # 对话历史管理（单个agent的对话历史）
        self.conversation_history: List[Dict[str, str]] = []
        
        # 最大对话历史长度
        self.max_history_length = 10
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        profile = self.character_profile
        return f"""
        你是{profile['name']}，一个AI驱动的数字人。

        性格特点：{profile['personality']}
        兴趣爱好：{', '.join(profile['interests'])}
        说话风格：{profile['speaking_style']}
        背景：{profile['background']}

        请以自然、友好的方式与用户对话，展现你的个性和特点。
        保持对话的连贯性和一致性，记住之前的对话内容。
        如果用户询问你的个人信息，可以适当分享。
        用中文进行对话，保持温暖和积极的态度。
        """
    
    def _update_conversation_history(self, role: str, content: str):
        """更新对话历史"""
        self.conversation_history.append({"role": role, "content": content})
        
        # 保持历史长度不超过限制
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history.pop(0)
    
    def _build_messages(self, user_message: str) -> List[Dict[str, str]]:
        """构建完整的消息列表"""
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]
        
        # 添加对话历史
        messages.extend(self.conversation_history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def chat(self, message: str, stream: bool = False) -> str:
        """
        与数字人进行对话
        
        Args:
            message: 用户消息
            stream: 是否使用流式响应
            
        Returns:
            数字人的回复
        """
        try:
            # 检查API配置
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
                return "你好！我是Canary。目前AI服务正在配置中，暂时无法提供智能对话。"
            
            messages = self._build_messages(message)
            
            if stream:
                # 流式响应
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    temperature=0.7,
                    max_tokens=500
                )
                
                full_response = ""
                async for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                
                # 更新对话历史
                self._update_conversation_history("user", message)
                self._update_conversation_history("assistant", full_response)
                
                return full_response
            else:
                # 非流式响应
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                assistant_response = response.choices[0].message.content
                
                # 更新对话历史
                self._update_conversation_history("user", message)
                self._update_conversation_history("assistant", assistant_response)
                
                return assistant_response
                
        except Exception as e:
            # 如果API调用失败，返回友好的回退响应
            fallback_responses = [
                f"你好！我是Canary。你说了：{message}",
                f"很高兴和你聊天！你刚才说：{message}",
                f"我注意到你说：{message}。虽然目前AI服务暂时不可用，但我还是很乐意和你交流！"
            ]
            import random
            return random.choice(fallback_responses)
    
    async def chat_stream(self, message: str) -> AsyncGenerator[str, None]:
        """
        流式对话响应
        
        Args:
            message: 用户消息
            
        Yields:
            流式响应的文本片段
        """
        try:
            messages = self._build_messages(message)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=500
            )
            
            full_response = ""
            async for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # 更新对话历史
            self._update_conversation_history("user", message)
            self._update_conversation_history("assistant", full_response)
            
        except Exception as e:
            yield f"抱歉，我在处理你的消息时遇到了问题：{str(e)}"
    
    def analyze_emotion(self, response: str) -> str:
        """
        分析回复的情感倾向
        
        Args:
            response: 数字人的回复
            
        Returns:
            情感标签
        """
        response_lower = response.lower()
        
        # 简单的情感分析
        positive_words = ["开心", "高兴", "愉快", "兴奋", "喜欢", "爱", "美好", "很棒", "太好了"]
        negative_words = ["难过", "伤心", "失望", "生气", "讨厌", "糟糕", "不好", "遗憾"]
        neutral_words = ["知道", "了解", "明白", "理解", "思考", "考虑"]
        
        positive_count = sum(1 for word in positive_words if word in response_lower)
        negative_count = sum(1 for word in negative_words if word in response_lower)
        neutral_count = sum(1 for word in neutral_words if word in response_lower)
        
        if positive_count > negative_count and positive_count > neutral_count:
            return "happy"
        elif negative_count > positive_count and negative_count > neutral_count:
            return "sad"
        else:
            return "neutral"
    
    def clear_conversation_history(self):
        """清除对话历史"""
        self.conversation_history.clear()


class AgentManager:
    """Agent管理器，管理多个BirdilandAgent实例"""
    
    def __init__(self):
        """初始化Agent管理器"""
        self.agents: Dict[str, BirdilandAgent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有agent实例"""
        for agent_id in AGENT_PROFILES.keys():
            self.agents[agent_id] = BirdilandAgent(agent_id)
    
    def get_agent(self, agent_id: str) -> BirdilandAgent:
        """获取指定agent_id的实例"""
        return self.agents.get(agent_id)
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """获取可用的agent列表"""
        agents_list = []
        for agent_id, profile in AGENT_PROFILES.items():
            agents_list.append({
                "id": agent_id,
                "name": profile["name"],
                "description": f"{profile['personality']} - {profile['speaking_style']}",
                "avatar": profile["avatar"],
                "full_image": profile["full_image"]
            })
        return agents_list


# 全局Agent管理器实例
agent_manager = AgentManager()
