from __future__ import annotations
import logging
from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Tool.GeneratePassword import GeneratePassword

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CipherForge API",
    description="CipherForge - Generate Secure Random Passwords With Configurable Options",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PasswordRequest(BaseModel):
    length: int = Field(default=16, ge=6, le=128)
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_digits: bool = True
    include_special: bool = True

class BulkPasswordRequest(PasswordRequest):
    count: int = Field(default=5, ge=1, le=50)

class PasswordResponse(BaseModel):
    password: str
    length: int
    strength: str

@app.get("/")
def HealthCheck():
    try:
        logger.info("Health Check Endpoint Called")
        return {"status": "ok", "message": "CipherForge API"}
    except Exception as e:
        logger.error("Error In Health Check: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate", response_model=PasswordResponse)
def GenerateSingle(req: PasswordRequest):
    try:
        logger.info("Generate Single Password Request (Length=%d)", req.length)
        result = GeneratePassword(
            length=req.length,
            include_uppercase=req.include_uppercase,
            include_lowercase=req.include_lowercase,
            include_digits=req.include_digits,
            include_special=req.include_special,
        )
        return result
    except ValueError as e:
        logger.warning("Validation Error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error Generating Password: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-bulk", response_model=List[PasswordResponse])
def GenerateBulk(req: BulkPasswordRequest):
    try:
        logger.info("Generate Bulk Password Request (Length=%d, Count=%d)", req.length, req.count)
        results = [
            GeneratePassword(
                length=req.length,
                include_uppercase=req.include_uppercase,
                include_lowercase=req.include_lowercase,
                include_digits=req.include_digits,
                include_special=req.include_special,
            )
            for _ in range(req.count)
        ]
        logger.info("Bulk Generation Completed: %d Passwords", req.count)
        return results
    except ValueError as e:
        logger.warning("Validation Error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error Generating Bulk Passwords: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))