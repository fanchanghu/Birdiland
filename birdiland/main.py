"""
Birdiland 数字人主程序
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from fastapi.responses import FileResponse

from .config import settings
from .api.routes import router as api_router
from .gradio_ui import mount_gradio_to_fastapi


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title="Birdiland API",
        description="AI驱动的数字人API服务",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册API路由
    app.include_router(api_router, prefix="/api/v1")

    # 挂载Gradio UI
    app = mount_gradio_to_fastapi(app)

    root_dir = Path(__file__).parent.parent

    app.mount("/images", StaticFiles(directory=str(root_dir / "images")), name="images")

    @app.get("/favicon.ico", include_in_schema=False)
    async def get_favicon():
        return FileResponse(str(root_dir / "favicon.ico"))

    @app.get("/manifest.json", include_in_schema=False)
    async def manifest():
        return FileResponse(str(root_dir / "manifest.json"))

    return app


def main():
    """主函数"""
    app = create_app()
    
    print("🚀 Birdiland 数字人服务启动中...")
    print(f"📖 API文档: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"💬 聊天界面: http://{settings.HOST}:{settings.PORT}/chat")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        # 添加优雅关闭配置
        timeout_keep_alive=30,           # 保持连接超时时间（秒）
        timeout_graceful_shutdown=3,   # 优雅关闭超时时间（秒）
    )


if __name__ == "__main__":
    main()
