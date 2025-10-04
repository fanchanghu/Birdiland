"""
Birdiland 数字人演示脚本
展示如何使用 BirdilandAgent 进行对话
"""

import asyncio
from birdiland.agent import BirdilandAgent


async def demo_birdiland():
    """演示 Birdiland 数字人功能"""
    print("🚀 Birdiland 数字人演示开始")
    print("=" * 50)
    
    # 创建数字人代理
    agent = BirdilandAgent()
    
    # 演示对话
    conversations = [
        "你好，请介绍一下你自己",
        "你叫什么名字？",
        "你对什么感兴趣？",
        "你能帮我做什么？",
        "今天天气真好，你有什么想说的吗？"
    ]
    
    for i, message in enumerate(conversations, 1):
        print(f"\n💬 用户: {message}")
        response = await agent.chat(message)
        emotion = agent.analyze_emotion(response)
        print(f"🤖 Birdiland [{emotion}]: {response}")
        
        # 添加一点延迟，让对话更自然
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Birdiland 数字人演示完成！")
    print("💡 提示: 你可以通过 API 端点 /api/v1/chat 来使用这个数字人")


if __name__ == "__main__":
    asyncio.run(demo_birdiland())
