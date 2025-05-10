from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel
from ...data_analysis.data_analyzer import DataAnalyzer
from ...data_analysis.file_handler import FileHandler

router = APIRouter()
analyzer = DataAnalyzer()

class EmpiricalAnalysisRequest(BaseModel):
    data: List[Dict[str, Any]]
    dependentVar: str
    independentVars: List[str]
    controlVars: List[str]
    groupVars: List[str]

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    处理文件上传请求
    
    Args:
        file: 上传的文件对象
        
    Returns:
        Dict包含:
        - 数据预览
        - 变量选项
        - 数据结构信息
    """
    try:
        # 验证文件
        FileHandler.validate_file(file)
        
        # 保存文件
        temp_file = FileHandler.save_upload_file(file)
        
        # 加载数据
        preview, variable_options, structure_info = analyzer.load_data(temp_file)
        
        # 清理临时文件
        FileHandler.cleanup_file(temp_file)
        
        return {
            "status": "success",
            "data": {
                "preview": preview.to_dict(),
                "variable_options": variable_options,
                "structure_info": structure_info
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理文件时发生错误：{str(e)}")
        
@router.post("/analyze")
async def analyze_data(selected_vars: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    分析选定的变量
    
    Args:
        selected_vars: 选定的变量字典，包含因变量和自变量
        
    Returns:
        分析结果和建议的实证策略
    """
    try:
        results = analyzer.analyze_data(selected_vars)
        return {
            "status": "success",
            "data": results
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析数据时发生错误：{str(e)}")

@router.post("/empirical-analysis")
async def run_empirical_analysis(request: EmpiricalAnalysisRequest) -> Dict[str, Any]:
    """
    运行实证分析
    
    Args:
        request: 包含数据和变量选择的请求对象
        
    Returns:
        实证分析结果
    """
    try:
        # 运行实证分析
        results = analyzer.run_empirical_analysis(
            data=request.data,
            dependent_var=request.dependentVar,
            independent_vars=request.independentVars,
            control_vars=request.controlVars,
            group_vars=request.groupVars
        )
        
        return {
            "success": True,
            "data": results
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"实证分析时发生错误：{str(e)}")

# 定期清理旧文件的任务
@router.on_event("startup")
async def startup_event():
    FileHandler.cleanup_old_files() 