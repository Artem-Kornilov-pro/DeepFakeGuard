"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="DeepFakeGuard",
    description="Privacy-Preserving Deepfake Detection with Federated Learning",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
