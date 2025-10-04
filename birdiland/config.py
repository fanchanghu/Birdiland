"""
配置文件
"""

import os
from typing import List

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
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # 模型配置
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    
    # 其他配置
    UV_INDEX_URL: str = ""
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量


# 全局配置实例
settings = Settings()
