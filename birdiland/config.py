"""
配置文件
"""

import os
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 服务器配置
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # AI配置
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    
    # 模型配置
    MODEL_NAME: str = ""
    
    # 其他配置
    UV_INDEX_URL: str = ""
    
    model_config = ConfigDict(
        env_file=".env.local",
        case_sensitive=True,
        extra="ignore"  # 忽略额外的环境变量
    )


# 全局配置实例
settings = Settings()
