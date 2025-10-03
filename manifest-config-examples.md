# Manifest.json 配置选项说明

## 基础配置选项

### 必需字段
```json
{
  "name": "应用完整名称",
  "short_name": "应用简称", 
  "start_url": "/",  // 应用启动时打开的URL
  "display": "standalone"  // 显示模式
}
```

### 显示模式 (display)
- `"standalone"` - 全屏应用，隐藏浏览器UI
- `"fullscreen"` - 全屏显示，隐藏所有UI
- `"minimal-ui"` - 最小化浏览器UI
- `"browser"` - 普通浏览器标签页

### 图标配置 (icons)
```json
"icons": [
  {
    "src": "图标路径",
    "sizes": "尺寸",  // 如 "192x192", "512x512"
    "type": "image/png",
    "purpose": "用途"  // "any", "maskable", "monochrome"
  }
]
```

## 主题和样式

### 颜色配置
```json
{
  "background_color": "#ffffff",  // 启动时的背景色
  "theme_color": "#3b82f6"       // 状态栏、工具栏颜色
}
```

### 方向配置 (orientation)
- `"portrait"` - 竖屏
- `"landscape"` - 横屏  
- `"portrait-primary"` - 主要竖屏方向
- `"landscape-primary"` - 主要横屏方向
- `"any"` - 任意方向

## 高级功能

### 快捷方式 (shortcuts)
```json
"shortcuts": [
  {
    "name": "快捷方式名称",
    "short_name": "简称",
    "description": "描述",
    "url": "/目标页面",
    "icons": []  // 可选图标
  }
]
```

### 截图 (screenshots)
```json
"screenshots": [
  {
    "src": "截图路径",
    "sizes": "尺寸",
    "type": "image/png",
    "form_factor": "wide|narrow"  // 宽屏或窄屏
  }
]
```

## 语言和地区

```json
{
  "lang": "zh-CN",        // 语言代码
  "dir": "ltr",           // 文字方向: ltr(左到右), rtl(右到左)
  "scope": "/"            // 应用作用域
}
```

## 分类 (categories)
- `"entertainment"` - 娱乐
- `"social"` - 社交
- `"productivity"` - 生产力
- `"utilities"` - 工具
- `"games"` - 游戏
- `"photo"` - 照片
- `"news"` - 新闻

## 实际应用示例

### 聊天应用配置
```json
{
  "name": "智能聊天助手",
  "short_name": "聊天助手",
  "description": "AI驱动的智能对话机器人",
  "start_url": "/chat",
  "display": "standalone",
  "background_color": "#f8fafc",
  "theme_color": "#06b6d4",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### 工具类应用配置
```json
{
  "name": "在线工具集",
  "short_name": "工具集",
  "description": "多种实用在线工具",
  "start_url": "/tools",
  "display": "minimal-ui",
  "background_color": "#ffffff",
  "theme_color": "#10b981",
  "orientation": "portrait-primary"
}
```

## 最佳实践

1. **图标尺寸**：至少提供192x192和512x512两种尺寸
2. **颜色搭配**：theme_color应与网站主题色一致
3. **启动URL**：设置为用户最常访问的页面
4. **描述信息**：简洁明了地描述应用功能
5. **测试验证**：使用浏览器开发者工具检查manifest有效性

## 验证工具

- Chrome DevTools → Application → Manifest
- [Web App Manifest Validator](https://manifest-validator.appspot.com/)
- [PWA Builder](https://www.pwabuilder.com/)
