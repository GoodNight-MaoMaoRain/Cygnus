import httpx
from fastapi import HTTPException

class HttpClient:
    __instance = None
    @staticmethod
    async def get_log() -> str:
        url = "http://example.com/api/logs"  # 替换为实际的日志API端点
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()  # 如果响应状态码不是 2xx，会引发 HTTPStatusError
                return response.text
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error fetching logs: {exc.response.text}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(exc)}")

    # 813解决问题加的假数据
    @staticmethod
    def get_instance():
        if HttpClient.__instance is None:
            HttpClient.__instance = HttpClient()
        return HttpClient.__instance
