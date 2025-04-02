## 使用python sdk创建和使用 MCP 服务器的完整示例

我将通过一个具体的例子来展示如何创建 MCP 服务器，然后如何访问和使用它。这个例子将包括服务器创建、安装和使用的完整流程。

### 第一步：创建一个简单的 MCP 服务器

首先，让我们创建一个简单的天气查询服务器：

```python

# weather_server.py
from mcp.server.fastmcp import FastMCP
import random

# 创建 MCP 服务器
mcp = FastMCP("天气助手")

# 添加一个城市天气资源
@mcp.resource("weather://{city}")
def get_city_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    weather_types = ["晴朗", "多云", "小雨", "大雨", "雷阵雨", "小雪", "大雪"]
    temp = random.randint(-10, 35)
    weather = random.choice(weather_types)
    return f"{city}的天气：{weather}，温度：{temp}°C"

# 添加一个天气预报工具
@mcp.tool()
def forecast_weather(city: str, days: int = 3) -> str:
    """预测未来几天的天气"""
    if days > 7:
        return "抱歉，最多只能预测未来7天的天气。"
    
    weather_types = ["晴朗", "多云", "小雨", "大雨", "雷阵雨", "小雪", "大雪"]
    forecast = []
    
    for i in range(days):
        temp = random.randint(-10, 35)
        weather = random.choice(weather_types)
        forecast.append(f"第{i+1}天：{weather}，温度：{temp}°C")
    
    return f"{city}未来{days}天天气预报：\n" + "\n".join(forecast)

# 添加一个温度转换工具
@mcp.tool()
def convert_temperature(celsius: float) -> dict:
    """将摄氏度转换为华氏度和开尔文"""
    fahrenheit = (celsius * 9/5) + 32
    kelvin = celsius + 273.15
    return {
        "摄氏度": celsius,
        "华氏度": fahrenheit,
        "开尔文": kelvin
    }

# 添加一个天气查询提示
@mcp.prompt()
def weather_query(city: str) -> str:
    """创建一个天气查询提示"""
    return f"请告诉我{city}的天气情况，并提供一些适合这种天气的活动建议。"

if __name__ == "__main__":
    mcp.run()

```
### 第二步：安装和运行服务器

 有几种方式可以运行和使用这个服务器：
#### 方式一：在 Claude Desktop 中安装
1. 首先，确保你已经安装了 Claude Desktop
2. 然后，使用命令行安装你的 MCP 服务器：

```
mcp install weather_server.py --name "我的天气助手"
```

#### 方式二：使用 MCP Inspector 进行开发测试

```
如果你想先测试你的服务器，可以使用 MCP Inspector：
mcp dev weather_server.py
```
这将启动一个交互式界面，你可以在其中测试你的资源、工具和提示。

#### 方式三：直接运行服务器

```
python weather_server.py

or

mcp run weather_server.py
```

### 第三步：使用 MCP 服务器

你可以在cursor、cline中按照我另一篇文章直接配置后使用即可。也可以mcp客户端sdk来使用

```python
# client_example.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 创建服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["weather_server.py"],
    )
    
    # 连接到服务器
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            
            # 列出可用工具
            tools = await session.list_tools()
            print("可用工具:", [tool.name for tool in tools])
            
            # 调用天气预报工具
            result = await session.call_tool(
                "forecast_weather", 
                arguments={"city": "上海", "days": 3}
            )
            print("天气预报结果:", result)
            
            # 读取天气资源
            content, mime_type = await session.read_resource("weather://北京")
            print("北京天气:", content)
            
            # 获取提示模板
            prompts = await session.list_prompts()
            print("可用提示:", [prompt.name for prompt in prompts])
            
            prompt = await session.get_prompt(
                "weather_query", 
                arguments={"city": "广州"}
            )
            print("天气查询提示:", prompt)

if __name__ == "__main__":
    asyncio.run(main())
```