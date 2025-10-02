"""
Birdiland 数字人主程序
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.routes import router as api_router


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

    return app


def main():
    """主函数"""
    app = create_app()
    
    print("🚀 Birdiland 数字人服务启动中...")
    print(f"📖 API文档: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
