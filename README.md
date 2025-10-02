# Birdiland - AI驱动的数字人项目

## 项目简介

Birdiland是一个由AI驱动的数字人项目。本项目致力于打造一个智能、互动、可爱、富有情感的二次元形象的数字伙伴。

## 项目目标

- 打造一个具有独特个性的AI数字人
- 实现自然流畅的人机对话交互
- 构建可爱的二次元形象展示
- 提供丰富的互动功能和情感表达

## 功能特性

### 核心功能
- ✅ 智能对话系统
- ✅ 情感识别与表达
- ✅ 个性化形象展示
- [ ] 多模态交互支持

### 扩展功能
- [ ] 语音交互支持
- [ ] 表情动画系统
- [ ] 个性化学习能力
- [ ] 第三方服务集成

### Web界面
- ✅ Gradio对话界面 (/chat)
- ✅ FastAPI文档界面 (/docs)

## 技术架构

### 前端技术栈
- [ ] 待补充（建议：React/Vue + 动画库）

### 后端技术栈  
- ✅ Python 3.11+
- ✅ FastAPI (Web框架)
- ✅ Uvicorn (ASGI服务器)
- ✅ Pydantic (数据验证)
- ✅ uv (Python包管理和虚拟环境)
- ✅ Gradio (Web UI框架)

### AI技术栈
- ✅ OpenAI API
- ✅ Transformers (Hugging Face)
- ✅ PyTorch
- [ ] 语音识别与合成
- [ ] 计算机视觉

### 数据存储
- [ ] 待补充（建议：SQLite/PostgreSQL）

## 快速开始

### 环境要求
- ✅ Python 3.11 或更高版本
- ✅ uv (Python包管理器)
- ✅ Git

### 安装步骤
```bash
# 克隆项目
git clone [项目地址]
cd birdiland

# 使用uv安装依赖
uv sync

# 或者使用pip安装依赖
pip install -r requirements.txt
```

### 运行项目
```bash
# 使用uv运行
uv run python -m birdiland.main

# 或者直接运行
python -m birdiland.main
```

### 访问界面
项目启动后，可以通过以下地址访问不同界面：

- **聊天界面**: http://127.0.0.1:8000/chat
  - 基于Gradio的友好对话界面
  - 支持实时聊天交互
  - 包含清空对话、查看个人资料等功能

- **API文档**: http://127.0.0.1:8000/docs
  - 交互式API文档
  - 支持在线测试API接口

- **健康检查**: http://127.0.0.1:8000/api/v1/health
  - 服务状态检查接口

### 开发环境设置
```bash
# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
uv run isort src/
```

## 项目结构

```
birdiland/
├── birdiland/             # Python包目录
│   ├── __init__.py        # 包初始化文件
│   ├── main.py            # 主程序入口
│   ├── config.py          # 配置管理
│   ├── gradio_ui.py       # Gradio对话界面
│   └── api/               # API路由
│       └── routes.py      # API路由定义
├── docs/                  # 文档
├── tests/                 # 测试文件
├── pyproject.toml         # 项目配置和依赖
├── README.md              # 项目说明
└── test_gradio_ui.py      # Gradio UI测试脚本
```

## 开发指南

### 贡献代码
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 代码规范
- [ ] 待补充（代码风格、提交规范等）

## 许可证

[待补充] 本项目采用 [许可证名称] 许可证

## 联系方式

- 项目负责人：[待补充]
- 邮箱：[待补充]
- 项目地址：[待补充]

## 致谢

感谢所有为这个项目做出贡献的开发者和设计师！

---

**注意**: 本README文件中的部分内容需要根据项目实际进展进行补充。请根据开发进度及时更新相关信息。
