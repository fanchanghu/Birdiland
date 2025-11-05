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
  1. 使用 `uv add` 更新 `pyproject.toml` 文件中的依赖定义
  2. 使用 `uv sync --dev` 安装所有依赖
  3. 确保依赖版本一致性，便于团队协作

## 代码组织
- 将业务逻辑与 UI 界面分离
- API 路由单独组织在 api 目录中
- 配置管理使用专门的 config 模块
- 使用 Pydantic V2 语法（ConfigDict 而非 class Config）

## 测试规范
- 只测试模块外部接口，不测试 `_` 开头的内部函数
- 测试文件位于 `tests/` 目录
- 使用 pytest 作为测试框架
- 测试命名规范：`test_*.py`
- 测试类命名规范：`Test*`
- 异步测试需要添加 `@pytest.mark.asyncio` 装饰器
- 使用 `unittest.mock` 进行模拟测试
- 测试覆盖率应包括所有公共 API 方法

## 部署考虑
- 包含 manifest.json 用于应用配置
- 支持环境变量配置
- 提供清晰的 README 文档
