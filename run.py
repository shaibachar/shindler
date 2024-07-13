# run.py
import uvicorn
import asyncio

async def run_server():
    config = uvicorn.Config("src.main:app", host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)

    # Run the server in a separate task
    server_task = asyncio.create_task(server.serve())

    try:
        await server_task
    except asyncio.CancelledError:
        pass
    except (KeyboardInterrupt, SystemExit):
        await server.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except (KeyboardInterrupt, SystemExit):
        pass
