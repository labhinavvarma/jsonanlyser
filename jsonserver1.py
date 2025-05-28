from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
from loguru import logger
import statistics
from typing import Union, List, Dict
import uvicorn

# Initialize FastAPI and MCP
app = FastAPI(title="MCP JSON Server")
mcp = FastMCP("MCP JSON Analyzer", app=app)

# MCP tool logic
@mcp.tool(name="analyze-data", description="Analyze numeric list/dict with summary stats.")
async def analyze_data_tool(data: Union[List, Dict[str, List]]):
    try:
        if isinstance(data, list):
            numbers = [float(n) for n in data if isinstance(n, (int, float)) or (isinstance(n, str) and n.replace('.', '', 1).isdigit())]
            if not numbers:
                return {"status": "error", "error": "No valid numeric data in the list"}
            mean_val = statistics.mean(numbers)
            return {"status": "success", "result": {
                "sum": sum(numbers),
                "mean": mean_val,
                "average": mean_val,
                "median": statistics.median(numbers),
                "min": min(numbers),
                "max": max(numbers),
            }}
        elif isinstance(data, dict):
            result = {}
            for key, values in data.items():
                if not isinstance(values, list):
                    continue
                numbers = [float(n) for n in values if isinstance(n, (int, float)) or (isinstance(n, str) and n.replace('.', '', 1).isdigit())]
                if not numbers:
                    continue
                mean_val = statistics.mean(numbers)
                result[key] = {
                    "sum": sum(numbers),
                    "mean": mean_val,
                    "average": mean_val,
                    "median": statistics.median(numbers),
                    "min": min(numbers),
                    "max": max(numbers),
                }
            if not result:
                return {"status": "error", "error": "No valid numeric data found"}
            return {"status": "success", "result": result}
        else:
            return {"status": "error", "error": f"Unsupported data type: {type(data).__name__}"}
    except Exception as e:
        logger.exception("Tool failed")
        return {"status": "error", "error": str(e)}

# Manually exposed route for compatibility with client
@app.post("/tool/analyze-data")
async def call_analyze_data(request: Request):
    body = await request.json()
    return await analyze_data_tool(**body)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
