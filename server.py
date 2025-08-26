from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application state during startup."""
    app.state.last_result = None
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/reverse")
async def reverse_string(in_: str = Query(..., alias="in")):
    """Reverse the order of words in the input string."""
    if not in_ or not in_.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'in' must not be empty.")

    try:
        words = in_.strip().split()
        reversed_str = " ".join(reversed(words))
        app.state.last_result = reversed_str
        return {"result": reversed_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/restore")
async def restore_result():
    """Return the last reversed string, if available."""
    result = app.state.last_result
    if result is None:
        raise HTTPException(status_code=404, detail="No reversed result found. Use /reverse first.")
    return {"result": result}

@app.get("/health")
async def health_check():
    """Health check endpoint to confirm the server is running."""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
