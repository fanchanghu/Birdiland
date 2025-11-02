"""
Birdiland 数字人测试用例
使用 pytest 测试 BirdilandAgent 功能
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from birdiland.agent import BirdilandAgent, AGENT_PROFILES


class TestBirdilandAgent:
    """BirdilandAgent 测试类"""
    
    @pytest.fixture
    def agent(self):
        """创建测试用的 BirdilandAgent 实例"""
        return BirdilandAgent("canary")
    
    @pytest.fixture
    def mock_openai_response(self):
        """模拟 OpenAI API 响应"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "你好！我是Canary，很高兴认识你！"
        return mock_response
    
    def test_agent_initialization(self, agent: BirdilandAgent):
        """测试代理初始化"""
        assert agent.agent_id == "canary"
        assert agent.character_profile == AGENT_PROFILES["canary"]
        assert agent.conversation_history == []
        assert agent.max_history_length == 10
    
    def test_agent_initialization_with_invalid_id(self):
        """测试使用无效 agent_id 初始化"""
        agent = BirdilandAgent("invalid_id")
        assert agent.character_profile == AGENT_PROFILES["canary"]  # 应该回退到默认
    
    @pytest.mark.asyncio
    async def test_conversation_history_through_chat(self, agent, mock_openai_response):
        """测试通过对话方法验证对话历史管理"""
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, return_value=mock_openai_response):
            # 进行对话
            response = await agent.chat("你好")
            
            # 验证对话历史被正确记录
            assert len(agent.conversation_history) == 2  # 用户消息和助手回复
            assert agent.conversation_history[0]["role"] == "user"
            assert agent.conversation_history[0]["content"] == "你好"
            assert agent.conversation_history[1]["role"] == "assistant"
            assert response == "你好！我是Canary，很高兴认识你！"
    
    @pytest.mark.asyncio
    async def test_chat_success(self, agent, mock_openai_response):
        """测试成功对话"""
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, return_value=mock_openai_response):
            response = await agent.chat("你好")
            
            assert response == "你好！我是Canary，很高兴认识你！"
            assert len(agent.conversation_history) == 2  # 用户消息和助手回复
    
    @pytest.mark.asyncio
    async def test_chat_without_api_key(self, agent):
        """测试没有 API 密钥时的对话"""
        # 临时移除 API 密钥
        original_key = agent.client.api_key
        agent.client.api_key = ""

        response = await agent.chat("你好")

        # 应该返回回退响应
        assert response is not None
        assert len(response) > 0
        assert "你好" in response  # 应该包含用户的消息
        
        # 恢复 API 密钥
        agent.client.api_key = original_key
    
    @pytest.mark.asyncio
    async def test_chat_exception_handling(self, agent):
        """测试异常处理"""
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, 
                         side_effect=Exception("API Error")):
            response = await agent.chat("你好")
            
            # 应该返回友好的回退响应
            assert response is not None
            assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_chat_stream_success(self, agent):
        """测试流式对话成功"""
        # 模拟流式响应
        async def mock_stream_response():
            chunks = [
                MagicMock(choices=[MagicMock(delta=MagicMock(content="你好"))]),
                MagicMock(choices=[MagicMock(delta=MagicMock(content="！我是"))]),
                MagicMock(choices=[MagicMock(delta=MagicMock(content="Canary"))])
            ]
            for chunk in chunks:
                yield chunk
        
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, return_value=mock_stream_response()):
            chunks = []
            async for chunk in agent.chat_stream("你好"):
                chunks.append(chunk)
            
            # 验证流式响应
            assert len(chunks) == 3
            assert "".join(chunks) == "你好！我是Canary"
            # 验证对话历史被更新
            assert len(agent.conversation_history) == 2
    
    @pytest.mark.asyncio
    async def test_chat_stream_exception(self, agent):
        """测试流式对话异常处理"""
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, 
                         side_effect=Exception("Stream Error")):
            chunks = []
            async for chunk in agent.chat_stream("你好"):
                chunks.append(chunk)
            
            # 应该返回错误消息
            assert len(chunks) == 1
            assert "抱歉" in chunks[0]
            assert "Stream Error" in chunks[0]
    
    def test_analyze_emotion_positive(self, agent):
        """测试积极情感分析"""
        response = "今天天气真好，我很开心！"
        emotion = agent.analyze_emotion(response)
        assert emotion == "happy"
    
    def test_analyze_emotion_negative(self, agent):
        """测试消极情感分析"""
        response = "听到这个消息我很难过"
        emotion = agent.analyze_emotion(response)
        assert emotion == "sad"
    
    def test_analyze_emotion_neutral(self, agent):
        """测试中性情感分析"""
        response = "我知道了，我会考虑的"
        emotion = agent.analyze_emotion(response)
        assert emotion == "neutral"
    
    @pytest.mark.asyncio
    async def test_clear_conversation_history(self, agent, mock_openai_response):
        """测试清除对话历史"""
        # 先进行对话来建立历史
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock, return_value=mock_openai_response):
            await agent.chat("测试消息")
            
            # 验证历史已建立
            assert len(agent.conversation_history) == 2
            
            # 清除历史
            agent.clear_conversation_history()
            assert len(agent.conversation_history) == 0


class TestAgentIntegration:
    """集成测试类"""
    
    @pytest.mark.asyncio
    async def test_multiple_conversations(self):
        """测试多次对话的连贯性"""
        agent = BirdilandAgent("canary")
        
        # 第一次对话
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock) as mock_create:
            mock_response1 = MagicMock()
            mock_response1.choices[0].message.content = "你好！我是Canary。"
            mock_create.return_value = mock_response1
            
            response1 = await agent.chat("你好")
            assert "Canary" in response1
        
        # 第二次对话应该包含历史
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock) as mock_create:
            mock_response2 = MagicMock()
            mock_response2.choices[0].message.content = "是的，我刚才说过我是Canary。"
            mock_create.return_value = mock_response2
            
            response2 = await agent.chat("你刚才说你叫什么？")
            assert "Canary" in response2


@pytest.mark.asyncio
async def test_demo_conversation_flow():
    """演示对话流程测试（基于原始演示脚本）"""
    agent = BirdilandAgent("canary")
    
    # 模拟对话序列
    conversations = [
        "你好，请介绍一下你自己",
        "你叫什么名字？",
        "你对什么感兴趣？"
    ]
    
    # 使用模拟的 API 响应
    mock_responses = [
        "你好！我是Canary，一个友好、聪明的AI助手。",
        "我叫Canary，很高兴认识你！",
        "我对学习新事物、帮助他人、艺术创作等都很感兴趣。"
    ]
    
    for i, (message, expected_response) in enumerate(zip(conversations, mock_responses)):
        with patch.object(agent.client.chat.completions, 'create', 
                         new_callable=AsyncMock) as mock_create:
            mock_response = MagicMock()
            mock_response.choices[0].message.content = expected_response
            mock_create.return_value = mock_response
            
            response = await agent.chat(message)
            emotion = agent.analyze_emotion(response)
            
            # 验证响应和情感分析
            assert response == expected_response
            assert emotion in ["happy", "sad", "neutral"]
            
            # 验证对话历史更新
            assert len(agent.conversation_history) == (i + 1) * 2


if __name__ == "__main__":
    # 保留原始演示功能，但使用 pytest 运行
    pytest.main([__file__, "-v"])
