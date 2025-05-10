"""模板预览模块

此模块实现了论文模板的实时预览功能, including preview generation, update and rendering。
"""

from typing import Dict, List, Any, Optional, Callable, Tuple
import logging
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from .base.template import Template
import uuid

@dataclass
class PreviewData:
    """预览数据类"""
    
    def __init__(self, preview_id: str, template_id: str, content: Dict[str, Any],
                 style: Dict[str, Any], metadata: Dict[str, Any] = None):
        """初始化预览数据
        
        Args:
            preview_id: 预览ID
            template_id: 模板ID
            content: 内容数据
            style: 样式数据
            metadata: 元数据
        """
        self.preview_id = preview_id
        self.template_id = template_id
        self.content = content
        self.style = style
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return getattr(self, key)
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            Dict[str, Any]: 字典数据
        """
        return {
            "preview_id": self.preview_id,
            "template_id": self.template_id,
            "content": self.content,
            "style": self.style,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreviewData':
        """从字典创建预览数据
        
        Args:
            data: 字典数据
            
        Returns:
            PreviewData: 预览数据对象
        """
        required_fields = ["preview_id", "template_id", "content", "style"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        preview_data = cls(
            preview_id=data["preview_id"],
            template_id=data["template_id"],
            content=data["content"],
            style=data["style"],
            metadata=data.get("metadata")
        )
        
        if "created_at" in data:
            preview_data.created_at = data["created_at"]
        if "updated_at" in data:
            preview_data.updated_at = data["updated_at"]
        
        return preview_data

class TemplatePreviewManager:
    """模板预览管理器"""
    
    def __init__(self, storage_dir: str):
        """初始化预览管理器
        
        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = storage_dir
        self.logger = logging.getLogger(__name__)
        
        # 创建存储目录
        os.makedirs(storage_dir, exist_ok=True)
        
        # 初始化钩子函数
        self.pre_save_hooks = []
        self.post_save_hooks = []
        
    def create_preview(self, template_id: str, content: Dict[str, Any], style: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """创建预览
        
        Args:
            template_id: 模板ID
            content: 预览内容
            style: 预览样式
            metadata: 元数据
        
        Returns:
            str: 预览ID
        """
        try:
            if not template_id:
                raise ValueError("Template ID cannot be empty")
            if not content:
                raise ValueError("Content cannot be empty")
            if style is None:
                style = {}
            
            preview_id = str(uuid.uuid4())
            preview_data = PreviewData(
                preview_id=preview_id,
                template_id=template_id,
                content=content,
                style=style,
                metadata=metadata
            )
            
            # 调用预保存钩子
            for hook in self.pre_save_hooks:
                preview_data.content, preview_data.style = hook(preview_data.content, preview_data.style)
            
            # 保存预览数据
            preview_file = os.path.join(self.storage_dir, f"{preview_id}.json")
            with open(preview_file, "w", encoding="utf-8") as f:
                json.dump(preview_data.to_dict(), f, ensure_ascii=False, indent=2)
            
            # 调用后保存钩子
            for hook in self.post_save_hooks:
                hook(preview_id, preview_data.content, preview_data.style)
            
            return preview_id
            
        except Exception as e:
            self.logger.error(f"Error creating preview: {str(e)}")
            raise
            
    def get_preview(self, preview_id: str) -> Optional[PreviewData]:
        """获取预览
        
        Args:
            preview_id: 预览ID
            
        Returns:
            Optional[PreviewData]: 预览数据,如果不存在则返回None
        """
        try:
            if not preview_id:
                raise ValueError("Preview ID cannot be empty")
            
            # 读取预览数据
            preview_file = os.path.join(self.storage_dir, f"{preview_id}.json")
            if not os.path.exists(preview_file):
                raise ValueError(f"Preview {preview_id} not found")
            
            with open(preview_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return PreviewData.from_dict(data)
            
        except Exception as e:
            self.logger.error(f"Error getting preview: {str(e)}")
            return None
            
    def update_preview(self, preview_id: str, content: Dict[str, Any], style: Optional[Dict[str, Any]] = None) -> None:
        """更新预览
        
        Args:
            preview_id: 预览ID
            content: 预览内容
            style: 预览样式
        """
        try:
            if not preview_id:
                raise ValueError("Preview ID cannot be empty")
            if not content:
                raise ValueError("Content cannot be empty")
            
            preview = self.get_preview(preview_id)
            if not preview:
                raise ValueError(f"Preview {preview_id} not found")
            
            # 更新内容
            preview.content = content
            
            # 如果提供了样式，则更新样式
            if style is not None:
                preview.style = style
            
            # 更新时间
            preview.updated_at = datetime.now().isoformat()
            
            # 调用预保存钩子
            for hook in self.pre_save_hooks:
                preview.content, preview.style = hook(preview.content, preview.style)
            
            # 保存预览数据
            preview_file = os.path.join(self.storage_dir, f"{preview_id}.json")
            with open(preview_file, "w", encoding="utf-8") as f:
                json.dump(preview.to_dict(), f, ensure_ascii=False, indent=2)
            
            # 调用后保存钩子
            for hook in self.post_save_hooks:
                hook(preview_id, preview.content, preview.style)
            
        except Exception as e:
            self.logger.error(f"Error updating preview: {str(e)}")
            raise
            
    def delete_preview(self, preview_id: str) -> bool:
        """删除预览
        
        Args:
            preview_id: 预览ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if not preview_id:
                raise ValueError("Preview ID cannot be empty")
            
            # 删除预览文件
            preview_file = os.path.join(self.storage_dir, f"{preview_id}.json")
            if os.path.exists(preview_file):
                os.remove(preview_file)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting preview: {str(e)}")
            return False
            
    def list_previews(self) -> List[PreviewData]:
        """列出所有预览
        
        Returns:
            List[PreviewData]: 预览数据列表
        """
        try:
            previews = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith(".json"):
                    preview_id = filename[:-5]
                    preview = self.get_preview(preview_id)
                    if preview:
                        previews.append(preview)
            return previews
            
        except Exception as e:
            self.logger.error(f"Error listing previews: {str(e)}")
            return []
            
    def render_preview(self, preview_id: str) -> Optional[str]:
        """渲染预览
        
        Args:
            preview_id: 预览ID
            
        Returns:
            Optional[str]: 渲染后的HTML内容,如果渲染失败则返回None
        """
        try:
            if not preview_id:
                raise ValueError("Preview ID cannot be empty")
            
            # 获取预览数据
            preview = self.get_preview(preview_id)
            if not preview:
                raise ValueError(f"Preview {preview_id} not found")
            
            # 渲染预览
            html_content = self._render_template(preview.content, preview.style)
            return html_content
            
        except Exception as e:
            self.logger.error(f"Error rendering preview: {str(e)}")
            return None
            
    def export_preview(self, preview_id: str) -> Optional[Dict[str, Any]]:
        """导出预览
        
        Args:
            preview_id: 预览ID
            
        Returns:
            Optional[Dict[str, Any]]: 导出的预览数据,如果导出失败则返回None
        """
        try:
            if not preview_id:
                raise ValueError("Preview ID cannot be empty")
            
            # 获取预览数据
            preview = self.get_preview(preview_id)
            if not preview:
                raise ValueError(f"Preview {preview_id} not found")
            
            # 导出预览数据
            export_data = preview.to_dict()
            return export_data
            
        except Exception as e:
            self.logger.error(f"Error exporting preview: {str(e)}")
            return None
            
    def import_preview(self, import_data: Dict[str, Any]) -> Optional[str]:
        """导入预览
        
        Args:
            import_data: 导入的预览数据
            
        Returns:
            Optional[str]: 预览ID,如果导入失败则返回None
        """
        try:
            if not import_data:
                raise ValueError("Import data cannot be empty")
            
            # 验证导入数据
            required_fields = ["template_id", "content", "style"]
            for field in required_fields:
                if field not in import_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # 创建预览
            preview_id = self.create_preview(
                template_id=import_data["template_id"],
                content=import_data["content"],
                style=import_data["style"],
                metadata=import_data.get("metadata")
            )
            
            return preview_id
            
        except Exception as e:
            self.logger.error(f"Error importing preview: {str(e)}")
            return None
            
    def register_pre_save_hook(self, hook: Callable[[Dict[str, Any], Dict[str, Any]], Tuple[Dict[str, Any], Dict[str, Any]]]):
        """注册预保存钩子
        
        Args:
            hook: 钩子函数
        """
        self.pre_save_hooks.append(hook)
        
    def register_post_save_hook(self, hook: Callable[[str, Dict[str, Any], Dict[str, Any]], None]):
        """注册后保存钩子
        
        Args:
            hook: 钩子函数
        """
        self.post_save_hooks.append(hook)
        
    def _render_template(self, content: Dict[str, Any], style: Dict[str, Any]) -> str:
        """渲染模板
        
        Args:
            content: 模板内容
            style: 样式设置
        
        Returns:
            str: 渲染后的HTML
        """
        try:
            # 构建HTML内容
            html_content = []
            html_content.append("<!DOCTYPE html>")
            html_content.append("<html>")
            html_content.append("<head>")
            html_content.append("<meta charset='utf-8'>")
            html_content.append("<title>模板预览</title>")
            html_content.append("<style>")
            html_content.append("body { font-family: Arial, sans-serif; margin: 20px; }")
            html_content.append("h1 { color: #333; }")
            html_content.append("h2 { color: #666; }")
            html_content.append("p { line-height: 1.6; }")
            
            # 应用自定义样式
            if style:
                for selector, properties in style.items():
                    if isinstance(properties, dict):
                        style_str = f"{selector} {{ "
                        for prop, value in properties.items():
                            style_str += f"{prop}: {value}; "
                        style_str += "}"
                        html_content.append(style_str)
            
            html_content.append("</style>")
            html_content.append("</head>")
            html_content.append("<body>")
            
            # 渲染内容
            if "chapters" in content:
                for chapter in content["chapters"]:
                    if "title" in chapter:
                        html_content.append(f"<h1>{chapter['title']}</h1>")
                    if "sections" in chapter:
                        for section in chapter["sections"]:
                            if "title" in section:
                                html_content.append(f"<h2>{section['title']}</h2>")
                            if "content" in section:
                                html_content.append(f"<p>{section['content']}</p>")
            
            html_content.append("</body>")
            html_content.append("</html>")
            
            return "\n".join(html_content)
            
        except Exception as e:
            self.logger.error(f"Error rendering template: {str(e)}")
            raise 