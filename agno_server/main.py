"""
Entry point for the Agno FastMCP Supabase server.
"""

import os
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Any, Dict, Optional, List
from supabase import create_client, Client
from fastapi.staticfiles import StaticFiles
from agno_server.orchestrator import AgnoOrchestrator
from agno_server.orchestrator_agno import AgnoOrchestratorAgno

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase credentials are not set in environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

app = FastAPI()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
def startup_event():
    app.state.supabase = get_supabase_client()

class ReadRowsRequest(BaseModel):
    table: str
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 100

class ReadRowsResponse(BaseModel):
    rows: List[Dict[str, Any]]

class CreateRecordRequest(BaseModel):
    table: str
    records: List[Dict[str, Any]]

class CreateRecordResponse(BaseModel):
    inserted: List[Dict[str, Any]]

class UpdateRecordRequest(BaseModel):
    table: str
    filters: Dict[str, Any]
    values: Dict[str, Any]

class UpdateRecordResponse(BaseModel):
    updated: List[Dict[str, Any]]

class DeleteRecordRequest(BaseModel):
    table: str
    filters: Dict[str, Any]

class DeleteRecordResponse(BaseModel):
    deleted: List[Dict[str, Any]]

class RefinePromptRequest(BaseModel):
    user_idea: str

class RefinePromptResponse(BaseModel):
    prompt: str

# Reason: Placeholder for MCP server startup logic
@app.get("/", include_in_schema=True)
def root():
    return {"status": "Agno MCP server running"}

@app.post("/tools/read_rows", response_model=ReadRowsResponse)
def read_rows(request: ReadRowsRequest, http_request: Request):
    """
    Reads rows from a specified Supabase table using optional filters.
    Args:
        request (ReadRowsRequest): The request parameters.
    Returns:
        ReadRowsResponse: The rows from the table.
    Raises:
        HTTPException: If the table does not exist or query fails.
    """
    supabase = http_request.app.state.supabase
    table = request.table
    filters = request.filters or {}
    limit = request.limit or 100
    try:
        query = supabase.table(table).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        rows = query.limit(limit).execute().data
        return ReadRowsResponse(rows=rows)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/create_record", response_model=CreateRecordResponse)
def create_record(request: CreateRecordRequest, http_request: Request):
    """
    Creates one or more records in a Supabase table.
    Args:
        request (CreateRecordRequest): The request parameters.
    Returns:
        CreateRecordResponse: The inserted records.
    Raises:
        HTTPException: If insertion fails.
    """
    supabase = http_request.app.state.supabase
    table = request.table
    records = request.records
    try:
        inserted = supabase.table(table).insert(records).execute().data
        return CreateRecordResponse(inserted=inserted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/update_record", response_model=UpdateRecordResponse)
def update_record(request: UpdateRecordRequest, http_request: Request):
    """
    Updates one or more records in a Supabase table.
    Args:
        request (UpdateRecordRequest): The request parameters.
    Returns:
        UpdateRecordResponse: The updated records.
    Raises:
        HTTPException: If update fails.
    """
    supabase = http_request.app.state.supabase
    table = request.table
    filters = request.filters
    values = request.values
    try:
        query = supabase.table(table)
        for key, value in filters.items():
            query = query.eq(key, value)
        updated = query.update(values).execute().data
        return UpdateRecordResponse(updated=updated)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/delete_record", response_model=DeleteRecordResponse)
def delete_record(request: DeleteRecordRequest, http_request: Request):
    """
    Deletes one or more records in a Supabase table.
    Args:
        request (DeleteRecordRequest): The request parameters.
    Returns:
        DeleteRecordResponse: The deleted records.
    Raises:
        HTTPException: If deletion fails.
    """
    supabase = http_request.app.state.supabase
    table = request.table
    filters = request.filters
    try:
        query = supabase.table(table)
        for key, value in filters.items():
            query = query.eq(key, value)
        deleted = query.delete().execute().data
        return DeleteRecordResponse(deleted=deleted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

orchestrator = AgnoOrchestrator()
agno_orchestrator = AgnoOrchestratorAgno()

@app.post("/refine_prompt", response_model=RefinePromptResponse)
def refine_prompt(request: RefinePromptRequest):
    """
    Refine a rough user idea into a production-ready prompt using the multi-agent workflow.
    Args:
        request (RefinePromptRequest): The user's rough idea.
    Returns:
        RefinePromptResponse: The final, production-ready prompt.
    """
    try:
        prompt = orchestrator.refine_prompt(request.user_idea)
        return RefinePromptResponse(prompt=prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prompt refinement failed: {str(e)}")

# --- AGNO MULTI-AGENT ENDPOINT ---
@app.post("/refine_prompt_agno", response_model=RefinePromptResponse)
def refine_prompt_agno(request: RefinePromptRequest):
    """
    Refine a rough user idea into a production-ready prompt using Agno's official multi-agent abstractions.
    Args:
        request (RefinePromptRequest): The user's rough idea.
    Returns:
        RefinePromptResponse: The final, production-ready prompt.
    """
    prompt = agno_orchestrator.refine_prompt(request.user_idea)
    return RefinePromptResponse(prompt=prompt)
