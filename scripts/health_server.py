import os
from aiohttp import web
from loguru import logger
import asyncio

async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logger.info(f"Starting health check server on port {port}...")
    await site.start()
    
    # Keep it running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_health_server())
