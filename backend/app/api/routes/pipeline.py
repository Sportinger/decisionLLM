from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.pipeline import PipelineConfig, PipelineLayer
from app.models.node import NodeConfig, NodeRole
from app.core.pipeline_store import pipeline_store

router = APIRouter()


@router.get("/")
async def list_pipelines():
    """List all available pipelines."""
    return {"pipelines": list(pipeline_store.get_all().values())}


@router.get("/{pipeline_id}")
async def get_pipeline(pipeline_id: str):
    """Get a specific pipeline configuration."""
    pipeline = pipeline_store.get(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.post("/")
async def create_pipeline(config: PipelineConfig):
    """Create a new pipeline configuration."""
    pipeline_store.save(config)
    return {"id": config.id, "message": "Pipeline created successfully"}


@router.put("/{pipeline_id}")
async def update_pipeline(pipeline_id: str, config: PipelineConfig):
    """Update an existing pipeline configuration."""
    existing = pipeline_store.get(pipeline_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    config.id = pipeline_id
    pipeline_store.save(config)
    return {"id": pipeline_id, "message": "Pipeline updated successfully"}


@router.delete("/{pipeline_id}")
async def delete_pipeline(pipeline_id: str):
    """Delete a pipeline configuration."""
    if pipeline_id == "default":
        raise HTTPException(status_code=400, detail="Cannot delete default pipeline")

    if not pipeline_store.delete(pipeline_id):
        raise HTTPException(status_code=404, detail="Pipeline not found")

    return {"message": "Pipeline deleted successfully"}


@router.get("/templates/list")
async def list_templates():
    """List available pipeline templates."""
    templates = [
        {
            "id": "3-layer-consensus",
            "name": "3-Layer Consensus",
            "description": "3 generators → 2 aggregators → 1 final",
            "layers": [
                {"level": 0, "node_count": 3},
                {"level": 1, "node_count": 2},
                {"level": 2, "node_count": 1},
            ],
        },
        {
            "id": "simple-voting",
            "name": "Simple Voting",
            "description": "3 generators → 1 final",
            "layers": [
                {"level": 0, "node_count": 3},
                {"level": 1, "node_count": 1},
            ],
        },
        {
            "id": "deep-consensus",
            "name": "Deep Consensus",
            "description": "5 generators → 3 aggregators → 2 validators → 1 final",
            "layers": [
                {"level": 0, "node_count": 5},
                {"level": 1, "node_count": 3},
                {"level": 2, "node_count": 2},
                {"level": 3, "node_count": 1},
            ],
        },
    ]
    return {"templates": templates}
