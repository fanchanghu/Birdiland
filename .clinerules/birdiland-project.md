## Brief overview
本项目为 Birdiland AI 代理项目，使用 Python 开发，包含 Gradio UI 界面和 API 路由。规则文件涵盖项目特定的开发约定和偏好。

## 项目结构
- 主代码位于 `birdiland/` 目录下
- API 路由在 `birdiland/api/routes.py` 中定义
- UI 界面使用 `birdiland/gradio_ui.py` 实现
- 配置文件包括 `pyproject.toml` 和 `.env.local` 文件

## 依赖管理
- 使用 `pyproject.toml` 进行依赖管理
- 主要依赖包括 Gradio 用于 UI 界面
- 环境变量配置使用 `.env.local` 文件
- 依赖安装流程：
  1. 更新 `pyproject.toml` 文件中的依赖定义
  2. 使用 uv 安装依赖：`uv pip install -e ".[dev]"`
  3. 确保依赖版本一致性，便于团队协作

## 代码组织
- 将业务逻辑与 UI 界面分离
- API 路由单独组织在 api 目录中
- 配置管理使用专门的 config 模块

## 部署考虑
- 包含 manifest.json 用于应用配置
- 支持环境变量配置
- 提供清晰的 README 文档
