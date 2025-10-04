"""
Gradio UI模块
提供基于gradio的对话界面
"""

import gradio as gr
from typing import List, Tuple, Generator, AsyncGenerator
import httpx
import json
from .config import settings


class ChatUI:
    """聊天UI类"""
    
    def __init__(self):
        self.chat_history: List[List[str]] = []
        self.api_base_url = f"http://{settings.HOST}:{settings.PORT}/api/v1"
    
    async def chat_with_birdiland(self, message: str, chat_history: List[List[str]]) -> AsyncGenerator[Tuple[str, List[List[str]]], None]:
        """与Birdiland聊天（支持流式响应）"""
        if not message.strip():
            yield "", chat_history
            return
        
        try:
            # 添加用户消息到历史（使用Gradio兼容的格式）
            chat_history.append([message, None])
            
            # 调用后端API（使用流式响应）
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.api_base_url}/chat",
                    json={
                        "message": message,
                        "user_id": "gradio_user",
                        "stream": True
                    },
                    timeout=30.0
                ) as response:
                    
                    if response.status_code == 200:
                        full_response = ""
                        emotion = "neutral"
                        
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                data_line = line[6:]  # 移除 "data: " 前缀
                                
                                if data_line == "[DONE]":
                                    break
                                
                                try:
                                    stream_data = json.loads(data_line)
                                    content = stream_data.get("content", "")
                                    emotion = stream_data.get("emotion", "neutral")
                                    is_final = stream_data.get("is_final", False)
                                    
                                    # 更新响应内容
                                    full_response += content
                                    
                                    # 更新聊天历史中的最后一条消息
                                    chat_history[-1][1] = self._add_emotion_emoji(full_response, emotion)
                                    
                                    # 返回更新后的聊天历史
                                    yield "", chat_history
                                    
                                except json.JSONDecodeError:
                                    continue
                        
                        # 最终更新（确保表情符号正确）
                        chat_history[-1][1] = self._add_emotion_emoji(full_response, emotion)
                        yield "", chat_history
                    else:
                        error_msg = f"❌ 抱歉，服务暂时不可用 (错误: {response.status_code})"
                        chat_history[-1][1] = error_msg
                        yield "", chat_history
                    
        except httpx.TimeoutException:
            error_msg = "⏰ 请求超时，请稍后重试"
            chat_history[-1][1] = error_msg
            yield "", chat_history
        except Exception as e:
            error_msg = f"❌ 发生错误: {str(e)}"
            chat_history[-1][1] = error_msg
            yield "", chat_history
    
    def _add_emotion_emoji(self, text: str, emotion: str) -> str:
        """根据情绪添加表情符号"""
        if emotion == "happy":
            return "😊 " + text
        elif emotion == "sad":
            return "😢 " + text
        elif emotion == "excited":
            return "🎉 " + text
        else:
            return "🤖 " + text
    
    def clear_chat(self) -> List[List[str]]:
        """清空聊天记录"""
        self.chat_history = []
        return []
    
    async def get_birdiland_profile(self) -> str:
        """获取Birdiland个人资料"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/profile")
                if response.status_code == 200:
                    profile = response.json()
                    return f"""
**🤖 Birdiland 个人资料**

**姓名**: {profile['name']}
**描述**: {profile['description']}
**性格**: {profile['personality']}
**兴趣**: {', '.join(profile['interests'])}
"""
                else:
                    return "❌ 无法获取个人资料信息"
        except Exception as e:
            return f"❌ 获取个人资料时出错: {str(e)}"


def create_gradio_interface() -> gr.Blocks:
    """创建Gradio界面"""
    
    chat_ui = ChatUI()
    
    with gr.Blocks(
        title="Birdiland 聊天助手",
        theme=gr.themes.Default(),
    ) as interface:
        with gr.Row():
            gr.Markdown("""
            # 🤖 Birdiland 聊天助手
            
            欢迎与Birdiland聊天！这是一个AI驱动的数字人，可以回答你的问题并与你交流。
            """)
        
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    chatbot = gr.Chatbot(
                        height=500,
                        show_copy_button=True,
                        show_label=False,
                        avatar_images=(None, "images/canary/avatar.png")
                    )
                    
                with gr.Row(equal_height=True):
                    msg = gr.Textbox(
                        placeholder="输入你想说的话...",
                        scale=8,
                        show_label=False,
                        lines=3,
                        max_lines=10,
                        submit_btn="发送"
                    )
                
                with gr.Row():
                    clear_btn = gr.Button("清空对话", variant="secondary")
                    profile_btn = gr.Button("查看个人资料", variant="secondary")
            
            # 隐藏组件用于保存用户输入
            user_message = gr.State()
            
            with gr.Column(scale=1):
                gr.Markdown("### ℹ️ 使用说明")
                gr.Markdown("""
                - 在下方输入框输入消息
                - 点击发送或按Enter键发送
                - 可以随时清空对话记录
                - 点击"查看个人资料"了解Birdiland
                
                **功能特点:**
                - 友好的对话界面
                - 表情丰富的回复
                - 支持长对话
                - 响应式设计
                """)
                profile_output = gr.Markdown()
    
        # 事件处理
        def save_user_message(message):
            """保存用户消息到状态"""
            return message
        
        msg.submit(
            save_user_message,
            inputs=[msg],
            outputs=[user_message]
        ).then(
            lambda: "",  # 清空输入框
            outputs=[msg]
        ).then(
            chat_ui.chat_with_birdiland,
            inputs=[user_message, chatbot],
            outputs=[msg, chatbot]
        )
        
        clear_btn.click(
            chat_ui.clear_chat,
            outputs=[chatbot]
        )
        
        profile_btn.click(
            chat_ui.get_birdiland_profile,
            outputs=[profile_output]
        )
    
    return interface


def mount_gradio_to_fastapi(app):
    """将Gradio界面挂载到FastAPI应用"""
    interface = create_gradio_interface()
    
    # 使用FastAPI的挂载方式
    import gradio as gr
    gr.mount_gradio_app(app, interface, path="/chat")
    
    return app
