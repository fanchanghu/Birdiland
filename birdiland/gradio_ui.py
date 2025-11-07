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
        self.chat_history: List[dict] = []
        self.api_base_url = f"http://{settings.HOST}:{settings.PORT}/api/v1"
    
    async def chat_with_birdiland(self, message: str, chat_history: List[dict], agent_id: str = "canary") -> AsyncGenerator[Tuple[str, List[dict]], None]:
        """与Birdiland聊天（支持流式响应）"""
        if not message.strip():
            # 如果消息为空，直接返回不处理
            yield "", chat_history
            return
        
        try:
            # 预先添加空的助手消息，确保chat_history[-1]能正确修改
            chat_history.append({"role": "assistant", "content": ""})
            
            # 调用后端API（使用流式响应）
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.api_base_url}/chat",
                    json={
                        "message": message,
                        "agent_id": agent_id,  # 传递选择的agent_id
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
                                    chat_history[-1] = {"role": "assistant", "content": self._add_emotion_emoji(full_response, emotion)}
                                    
                                    # 返回更新后的聊天历史
                                    yield "", chat_history
                                    
                                except json.JSONDecodeError:
                                    continue
                        
                        # 最终更新（确保表情符号正确）
                        chat_history[-1] = {"role": "assistant", "content": self._add_emotion_emoji(full_response, emotion)}
                        yield "", chat_history
                    else:
                        error_msg = f"❌ 抱歉，服务暂时不可用 (错误: {response.status_code})"
                        chat_history[-1] = {"role": "assistant", "content": error_msg}
                        yield "", chat_history
                    
        except httpx.TimeoutException:
            error_msg = "⏰ 请求超时，请稍后重试"
            chat_history[-1] = {"role": "assistant", "content": error_msg}
            yield "", chat_history
        except Exception as e:
            error_msg = f"❌ 发生错误: {str(e)}"
            chat_history[-1] = {"role": "assistant", "content": error_msg}
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
    
    def clear_chat(self) -> List[dict]:
        """清空聊天记录"""
        self.chat_history = []
        return []
    
    async def get_agents_list(self) -> list:
        """获取agent列表"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/agent/list")
                if response.status_code == 200:
                    return response.json()
                else:
                    return []
        except Exception as e:
            print(f"获取agent列表时出错: {str(e)}")
            return []
    
    async def get_birdiland_profile(self, agent_id: str = "canary") -> str:
        """获取Birdiland个人资料"""
        try:
            async with httpx.AsyncClient() as client:
                # 获取个人资料详情
                profile_response = await client.get(f"{self.api_base_url}/agent/{agent_id}/profile")
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    
                    # 构建包含全身照的个人资料
                    profile_content = ""
                    profile_content += f"![{profile['name']}](/{profile['full_image']})\n\n"
                    
                    profile_content += f"""
- **姓名**: {profile['name']}
- **性格**: {profile['personality']}
- **兴趣**: {', '.join(profile['interests'])}
- **说话风格**: {profile['speaking_style']}
- **背景**: {profile['background']}
"""
                    return profile_content
                else:
                    return "❌ 无法获取个人资料信息"
        except Exception as e:
            return f"❌ 获取个人资料时出错: {str(e)}"

    async def get_agent_conversation_history(self, agent_id: str) -> List[dict]:
        """获取指定agent的对话历史"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/agent/{agent_id}/history")
                if response.status_code == 200:
                    history = response.json()
                    # 确保返回的格式与gradio兼容
                    return history
                else:
                    return []
        except Exception as e:
            print(f"获取对话历史时出错: {str(e)}")
            return []


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
            
            这是一个AI驱动的数字人，可以回答你的问题并与你交流。
            """)
        
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    chatbot = gr.Chatbot(
                        height=550,
                        show_copy_button=True,
                        show_label=False,
                        type="messages"  # 使用新的消息格式
                    )
                    
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="输入你想说的话...",
                        show_label=False,
                        lines=1,
                        max_lines=6,
                        submit_btn="发送"
                    )
                
            
            # 隐藏组件用于保存用户输入
            user_message = gr.State()
            
            with gr.Column(scale=1):
                # 数字人选择下拉框
                gr.Markdown("### 选择数字人")
                digital_human_dropdown = gr.Dropdown(
                    choices=[],
                    show_label=False,
                    interactive=True
                )
                
                gr.Markdown("### 角色个人资料")
                profile_output = gr.Markdown()
    
        # 事件处理
        def save_user_message(message):
            """保存用户消息到状态"""
            return message
        
        def add_user_message_to_chat(message, chat_history):
            """将用户消息添加到聊天历史并立即显示"""
            if not message.strip():
                # 如果消息为空，不添加到聊天历史
                return message, chat_history
            chat_history.append({"role": "user", "content": message})
            return "", chat_history
        
        async def load_agents_on_start():
            """界面加载时自动加载agent列表"""
            agents = await chat_ui.get_agents_list()
            if agents:
                # 创建下拉框选项：使用agent id作为值，agent name作为显示文本
                choices = [(agent["name"], agent["id"]) for agent in agents]
                # 设置默认值为第一个agent的id
                default_value = agents[0]["id"] if agents else ""
                return gr.update(choices=choices, value=default_value)
            else:
                return gr.update(choices=[], value="")
        
        async def load_profile_on_start():
            """界面加载时自动加载个人资料"""
            agents = await chat_ui.get_agents_list()
            if agents:
                # 使用第一个agent的id来加载个人资料
                return await chat_ui.get_birdiland_profile(agents[0]["id"])
            else:
                return "❌ 无法获取agent列表"
        
        async def update_profile_on_digital_human_change(agent_id):
            """当数字人选择改变时更新个人资料"""
            return await chat_ui.get_birdiland_profile(agent_id)
        
        async def get_agent_avatar(agent_id: str) -> str:
            """根据agent_id获取对应的头像路径"""
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{chat_ui.api_base_url}/agent/list")
                    if response.status_code == 200:
                        agents = response.json()
                        for agent in agents:
                            if agent["id"] == agent_id:
                                return agent.get("avatar", "images/canary/avatar.png")
            except Exception as e:
                return None
        
        async def update_chatbot_avatar(agent_id):
            """更新聊天机器人的头像"""
            avatar_path = await get_agent_avatar(agent_id)
            return gr.update(avatar_images=(None, avatar_path))
        
        async def load_conversation_history_on_agent_change(agent_id):
            """当切换角色时加载该角色的对话历史"""
            history = await chat_ui.get_agent_conversation_history(agent_id)
            return history
        
        # 界面加载时自动加载agent列表和个人资料
        interface.load(
            load_agents_on_start,
            outputs=[digital_human_dropdown]
        ).then(
            load_profile_on_start,
            outputs=[profile_output]
        )
        
        # 数字人选择改变时更新个人资料、加载对话历史并更新头像
        digital_human_dropdown.change(
            update_profile_on_digital_human_change,
            inputs=[digital_human_dropdown],
            outputs=[profile_output]
        ).then(
            lambda: [],
            inputs=[],
            outputs=[chatbot]
        ).then(
            update_chatbot_avatar,
            inputs=[digital_human_dropdown],
            outputs=[chatbot]
        ).then(
            load_conversation_history_on_agent_change,
            inputs=[digital_human_dropdown],
            outputs=[chatbot]
        )
        
        msg.submit(
            save_user_message,
            inputs=[msg],
            outputs=[user_message]
        ).then(
            add_user_message_to_chat,
            inputs=[user_message, chatbot],
            outputs=[msg, chatbot]
        ).then(
            chat_ui.chat_with_birdiland,
            inputs=[user_message, chatbot, digital_human_dropdown],  # 添加agent_id输入
            outputs=[msg, chatbot]
        )
    
    return interface


def mount_gradio_to_fastapi(app):
    """将Gradio界面挂载到FastAPI应用"""
    interface = create_gradio_interface()
    
    # 使用FastAPI的挂载方式，并配置防止阻塞
    import gradio as gr
    gr.mount_gradio_app(
        app, 
        interface, 
        path="/chat",
        # 添加配置防止阻塞
        app_kwargs={
            "block_thread": False,  # 不阻塞主线程
            "show_error": True,
            "quiet": True
        }
    )
    
    return app
