from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from routes.auth import get_current_user, User

router = APIRouter(prefix="/api/writings", tags=["写作"])

# 数据模型
class Writing(BaseModel):
    id: str
    title: str
    content: str
    status: str
    created_at: str
    updated_at: str

class CreateWritingRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    discipline: str
    paperType: str

class SectionData(BaseModel):
    content: str
    completed: bool

# 模拟数据库
writings_db = {}
sections_db = {}

@router.get("/")
async def get_writings(current_user: User = Depends(get_current_user)):
    return list(writings_db.values())

@router.get("/{writing_id}")
async def get_writing(writing_id: str, current_user: User = Depends(get_current_user)):
    if writing_id not in writings_db:
        raise HTTPException(status_code=404, detail="写作不存在")
    return writings_db[writing_id]

@router.post("/")
async def create_writing(request: CreateWritingRequest, current_user: User = Depends(get_current_user)):
    writing_id = str(len(writings_db) + 1)
    now = datetime.utcnow().isoformat()
    writing = {
        "id": writing_id,
        "title": request.title or "新写作",
        "content": request.content or "",
        "status": "draft",
        "created_at": now,
        "updated_at": now,
        "user_id": current_user.id,
        "discipline": request.discipline,
        "paperType": request.paperType
    }
    writings_db[writing_id] = writing
    return writing

@router.put("/{writing_id}")
async def update_writing(
    writing_id: str,
    writing: Writing,
    current_user: User = Depends(get_current_user)
):
    if writing_id not in writings_db:
        raise HTTPException(status_code=404, detail="写作不存在")
    if writings_db[writing_id]["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此写作")
    
    writing_dict = writing.dict()
    writing_dict["updated_at"] = datetime.utcnow().isoformat()
    writings_db[writing_id] = writing_dict
    return writing_dict

@router.delete("/{writing_id}")
async def delete_writing(writing_id: str, current_user: User = Depends(get_current_user)):
    if writing_id not in writings_db:
        raise HTTPException(status_code=404, detail="写作不存在")
    if writings_db[writing_id]["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除此写作")
    
    del writings_db[writing_id]
    return {"message": "写作已删除"}

@router.get("/{writing_id}/sections/{section_id}")
async def get_section(
    writing_id: str,
    section_id: str,
    current_user: User = Depends(get_current_user)
):
    if writing_id not in writings_db:
        raise HTTPException(status_code=404, detail="写作不存在")
    if writings_db[writing_id]["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限访问此写作")
    
    section_key = f"{writing_id}_{section_id}"
    if section_key not in sections_db:
        return {"content": "", "completed": False}
    return sections_db[section_key]

@router.put("/{writing_id}/sections/{section_id}")
async def update_section(
    writing_id: str,
    section_id: str,
    section_data: SectionData,
    current_user: User = Depends(get_current_user)
):
    # 如果是新写作，自动创建
    if writing_id == "new":
        writing_id = str(len(writings_db) + 1)
        now = datetime.utcnow().isoformat()
        writing = {
            "id": writing_id,
            "title": "新写作",
            "content": "",
            "status": "draft",
            "created_at": now,
            "updated_at": now,
            "user_id": current_user.id
        }
        writings_db[writing_id] = writing
    elif writing_id not in writings_db:
        raise HTTPException(status_code=404, detail="写作不存在")
    elif writings_db[writing_id]["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此写作")
    
    section_key = f"{writing_id}_{section_id}"
    sections_db[section_key] = section_data.dict()
    return sections_db[section_key]

@router.get("/preview/{section_id}")
async def get_preview(section_id: str, current_user: User = Depends(get_current_user)):
    # 这里应该实现预览逻辑
    return {"html": "<p>预览内容</p>"}

@router.get("/export/{section_id}")
async def export_to_word(section_id: str, current_user: User = Depends(get_current_user)):
    # 这里应该实现导出逻辑
    return {"fileUrl": f"/exports/{section_id}.docx"} 