"""This module implements version control for paper templates, including version management, history tracking and difference comparison。"""

from typing import Dict, List, Any, Optional, Callable, Tuple
import logging
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from .base.template import Template
import uuid
import difflib

@dataclass
class VersionInfo:
    """版本信息数据类"""
    version_id: str
    timestamp: datetime
    author: str
    description: str
    changes: Dict[str, Any]
    template_data: Dict[str, Any]
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    branch: str = "main"
    parent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionInfo':
        """从字典创建实例"""
        if 'timestamp' in data:
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

class VersionData:
    """版本数据类"""
    
    def __init__(self, version_id: str, template_id: str, template_data: Dict[str, Any],
                 metadata: Dict[str, Any] = None):
        """初始化版本数据
        
        Args:
            version_id: 版本ID
            template_id: 模板ID
            template_data: 模板数据
            metadata: 元数据
        """
        self.version_id = version_id
        self.template_id = template_id
        self.template_data = template_data
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionData':
        """从字典创建版本数据
        
        Args:
            data: 字典数据
            
        Returns:
            VersionData: 版本数据对象
        """
        required_fields = ["version_id", "template_id", "template_data"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        version_data = cls(
            version_id=data["version_id"],
            template_id=data["template_id"],
            template_data=data["template_data"],
            metadata=data.get("metadata")
        )
        
        if "created_at" in data:
            version_data.created_at = data["created_at"]
        if "updated_at" in data:
            version_data.updated_at = data["updated_at"]
        
        return version_data

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            Dict[str, Any]: 字典数据
        """
        return {
            "version_id": self.version_id,
            "template_id": self.template_id,
            "template_data": self.template_data,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class TemplateVersionControl:
    """版本控制系统类"""
    
    def __init__(self, storage_dir: str):
        """初始化版本控制系统
        
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
        
        # 初始化检查点目录
        self.checkpoint_dir = os.path.join(storage_dir, "checkpoints")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
    
    def create_version(self, template_id: str, template_data: Dict[str, Any],
                       metadata: Dict[str, Any] = None) -> Optional[str]:
        """创建版本
        
        Args:
            template_id: 模板ID
            template_data: 模板数据
            metadata: 元数据
            
        Returns:
            Optional[str]: 版本ID,如果创建失败则返回None
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not template_id:
            raise ValueError("Template ID cannot be empty")
        
        if not template_data:
            raise ValueError("Template data cannot be empty")
        
        try:
            # 生成版本ID
            version_id = str(uuid.uuid4())
            
            # 创建版本数据
            version_data = VersionData(
                version_id=version_id,
                template_id=template_id,
                template_data=template_data,
                metadata=metadata or {}
            )
            
            # 执行预保存钩子
            template_data, metadata = self._execute_pre_save_hooks(template_data, metadata or {})
            version_data.template_data = template_data
            version_data.metadata = metadata
            
            # 保存版本数据
            version_file = os.path.join(self.storage_dir, f"{version_id}.json")
            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(version_data.to_dict(), f, ensure_ascii=False, indent=2)
            
            # 执行后保存钩子
            self._execute_post_save_hooks(version_id, template_data, metadata)
            
            # 重新保存版本数据以包含钩子修改的元数据
            with open(version_file, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                saved_data["metadata"] = metadata
            
            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(saved_data, f, ensure_ascii=False, indent=2)
            
            return version_id
            
        except Exception as e:
            self.logger.error(f"Error creating version: {str(e)}")
            return None
    
    def get_version(self, version_id: str) -> Optional[VersionData]:
        """获取版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[VersionData]: 版本数据,如果不存在则返回None
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            # 读取版本数据
            version_file = os.path.join(self.storage_dir, f"{version_id}.json")
            if not os.path.exists(version_file):
                raise ValueError(f"Version {version_id} not found")
            
            with open(version_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return VersionData.from_dict(data)
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error getting version: {str(e)}")
            return None
    
    def list_versions(self) -> List[VersionData]:
        """列出所有版本
        
        Returns:
            List[VersionData]: 版本数据列表
        """
        try:
            versions = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith(".json"):
                    version_id = filename[:-5]
                    version = self.get_version(version_id)
                    if version:
                        versions.append(version)
            return versions
            
        except Exception as e:
            self.logger.error(f"Error listing versions: {str(e)}")
            return []
    
    def compare_versions(self, version1_id: str, version2_id: str) -> Optional[Dict[str, Any]]:
        """比较两个版本
        
        Args:
            version1_id: 第一个版本ID
            version2_id: 第二个版本ID
            
        Returns:
            Optional[Dict[str, Any]]: 版本差异数据,如果比较失败则返回None
        """
        try:
            if not version1_id or not version2_id:
                raise ValueError("Version IDs cannot be empty")
            
            # 获取版本数据
            version1 = self.get_version(version1_id)
            version2 = self.get_version(version2_id)
            
            if not version1 or not version2:
                raise ValueError("One or both versions not found")
            
            # 比较版本数据
            diff = self._compare_data(version1.template_data, version2.template_data)
            return diff
            
        except Exception as e:
            self.logger.error(f"Error comparing versions: {str(e)}")
            return None
    
    def rollback_version(self, version_id: str) -> bool:
        """回滚到指定版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            bool: 是否回滚成功
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            # 获取版本数据
            version = self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # 创建新版本
            new_version_id = self.create_version(
                template_id=version.template_id,
                template_data=version.template_data,
                metadata={"rollback_to": version_id}
            )
            
            if not new_version_id:
                raise ValueError("Failed to create new version")
            
            return True
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error rolling back version: {str(e)}")
            return False
    
    def export_version(self, version_id: str) -> Optional[Dict[str, Any]]:
        """导出版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[Dict[str, Any]]: 导出的版本数据,如果导出失败则返回None
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            # 获取版本数据
            version = self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # 导出版本数据
            export_data = {
                "version_id": version.version_id,
                "template_id": version.template_id,
                "template_data": version.template_data,
                "metadata": version.metadata,
                "created_at": version.created_at,
                "updated_at": version.updated_at
            }
            return export_data
            
        except Exception as e:
            self.logger.error(f"Error exporting version: {str(e)}")
            return None
    
    def import_version(self, import_data: Dict[str, Any]) -> Optional[str]:
        """导入版本
        
        Args:
            import_data: 导入的版本数据
            
        Returns:
            Optional[str]: 版本ID,如果导入失败则返回None
        """
        try:
            if not import_data:
                raise ValueError("Import data cannot be empty")
            
            # 验证导入数据
            required_fields = ["template_id", "template_data"]
            for field in required_fields:
                if field not in import_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # 创建版本
            version_id = self.create_version(
                template_id=import_data["template_id"],
                template_data=import_data["template_data"],
                metadata=import_data.get("metadata")
            )
            
            return version_id
            
        except Exception as e:
            self.logger.error(f"Error importing version: {str(e)}")
            return None
    
    def register_pre_save_hook(self, hook: Callable[[Dict[str, Any], Dict[str, Any]], Tuple[Dict[str, Any], Dict[str, Any]]]):
        """注册预保存钩子
        
        Args:
            hook: 钩子函数
        """
        if not callable(hook):
            raise ValueError("Hook must be callable")
        self.pre_save_hooks.append(hook)
    
    def register_post_save_hook(self, hook: Callable[[str, Dict[str, Any], Dict[str, Any]], None]):
        """注册后保存钩子
        
        Args:
            hook: 钩子函数
        """
        if not callable(hook):
            raise ValueError("Hook must be callable")
        self.post_save_hooks.append(hook)
    
    def clear_hooks(self):
        """清除所有钩子"""
        self.pre_save_hooks = []
        self.post_save_hooks = []
    
    def _execute_pre_save_hooks(self, template_data: Dict[str, Any], metadata: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """执行预保存钩子
        
        Args:
            template_data: 模板数据
            metadata: 元数据
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: 处理后的模板数据和元数据
        """
        for hook in self.pre_save_hooks:
            try:
                template_data, metadata = hook(template_data, metadata)
            except Exception as e:
                self.logger.error(f"Error executing pre-save hook: {str(e)}")
        return template_data, metadata
    
    def _execute_post_save_hooks(self, version_id: str, template_data: Dict[str, Any], metadata: Dict[str, Any]):
        """执行后保存钩子
        
        Args:
            version_id: 版本ID
            template_data: 模板数据
            metadata: 元数据
        """
        for hook in self.post_save_hooks:
            try:
                hook(version_id, template_data, metadata)
            except Exception as e:
                self.logger.error(f"Error executing post-save hook: {str(e)}")
    
    def _compare_data(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, Any]:
        """比较两个数据字典
        
        Args:
            data1: 第一个数据字典
            data2: 第二个数据字典
            
        Returns:
            Dict[str, Any]: 差异数据
        """
        diff = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        def compare_recursive(d1: Any, d2: Any, path: str = "") -> Dict[str, Any]:
            """递归比较数据
            
            Args:
                d1: 第一个数据
                d2: 第二个数据
                path: 当前路径
                
            Returns:
                Dict[str, Any]: 差异数据
            """
            if isinstance(d1, dict) and isinstance(d2, dict):
                result = {}
                for key in d2:
                    new_path = f"{path}.{key}" if path else key
                    if key not in d1:
                        result[key] = d2[key]
                    else:
                        sub_diff = compare_recursive(d1[key], d2[key], new_path)
                        if sub_diff:
                            result[key] = sub_diff
                for key in d1:
                    if key not in d2:
                        result[key] = None
                return result
            elif isinstance(d1, list) and isinstance(d2, list):
                if len(d1) != len(d2):
                    return {"old": d1, "new": d2}
                result = []
                for i, (item1, item2) in enumerate(zip(d1, d2)):
                    sub_diff = compare_recursive(item1, item2, f"{path}[{i}]")
                    if sub_diff:
                        result.append(sub_diff)
                return result if result else None
            elif d1 != d2:
                return {"old": d1, "new": d2}
            return None
        
        # 比较添加和修改的字段
        for key in data2:
            if key not in data1:
                diff["added"][key] = data2[key]
            else:
                sub_diff = compare_recursive(data1[key], data2[key], key)
                if sub_diff:
                    diff["modified"][key] = sub_diff
        
        # 比较删除的字段
        for key in data1:
            if key not in data2:
                diff["removed"][key] = data1[key]
        
        return diff

    def save_checkpoint(self, template_id: str, template_data: Dict[str, Any],
                       metadata: Dict[str, Any] = None) -> Optional[str]:
        """保存检查点
        
        Args:
            template_id: 模板ID
            template_data: 模板数据
            metadata: 元数据
            
        Returns:
            Optional[str]: 检查点ID,如果保存失败则返回None
        """
        try:
            if not template_id:
                raise ValueError("Template ID cannot be empty")
            
            if not template_data:
                raise ValueError("Template data cannot be empty")
            
            # 生成检查点ID
            checkpoint_id = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
            
            # 创建检查点数据
            checkpoint_data = {
                "checkpoint_id": checkpoint_id,
                "template_id": template_id,
                "template_data": template_data,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat()
            }
            
            # 执行预保存钩子
            for hook in self.pre_save_hooks:
                template_data, metadata = hook(template_data, metadata)
            
            # 保存检查点数据
            checkpoint_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.json")
            with open(checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
            
            # 执行后保存钩子
            for hook in self.post_save_hooks:
                hook(checkpoint_id, template_data, metadata)
            
            self.logger.info(f"Saved checkpoint {checkpoint_id} for template {template_id}")
            return checkpoint_id
            
        except Exception as e:
            self.logger.error(f"Error saving checkpoint: {str(e)}")
            return None
            
    def get_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """获取检查点
        
        Args:
            checkpoint_id: 检查点ID
            
        Returns:
            Optional[Dict[str, Any]]: 检查点数据,如果不存在则返回None
        """
        try:
            if not checkpoint_id:
                raise ValueError("Checkpoint ID cannot be empty")
            
            # 读取检查点数据
            checkpoint_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.json")
            if not os.path.exists(checkpoint_file):
                raise ValueError(f"Checkpoint {checkpoint_id} not found")
            
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                return json.load(f)
            
        except Exception as e:
            self.logger.error(f"Error getting checkpoint: {str(e)}")
            return None
            
    def list_checkpoints(self, template_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出检查点
        
        Args:
            template_id: 模板ID,如果指定则只列出该模板的检查点
            
        Returns:
            List[Dict[str, Any]]: 检查点数据列表
        """
        try:
            checkpoints = []
            for filename in os.listdir(self.checkpoint_dir):
                if filename.endswith(".json"):
                    checkpoint_id = filename[:-5]
                    checkpoint = self.get_checkpoint(checkpoint_id)
                    if checkpoint and (not template_id or checkpoint["template_id"] == template_id):
                        checkpoints.append(checkpoint)
            return sorted(checkpoints, key=lambda x: x["created_at"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error listing checkpoints: {str(e)}")
            return []
            
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """删除检查点
        
        Args:
            checkpoint_id: 检查点ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if not checkpoint_id:
                raise ValueError("Checkpoint ID cannot be empty")
            
            # 删除检查点文件
            checkpoint_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.json")
            if os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)
                self.logger.info(f"Deleted checkpoint {checkpoint_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error deleting checkpoint: {str(e)}")
            return False

    def create_branch(self, version_id: str, branch_name: str) -> Optional[str]:
        """创建分支
        
        Args:
            version_id: 版本ID
            branch_name: 分支名称
            
        Returns:
            Optional[str]: 新版本ID,如果创建失败则返回None
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            if not branch_name:
                raise ValueError("Branch name cannot be empty")
            
            # 获取版本数据
            version = self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # 创建新版本
            new_version_id = self.create_version(
                template_id=version.template_id,
                template_data=version.template_data,
                metadata={
                    "branch": branch_name,
                    "parent_id": version_id
                }
            )
            
            if not new_version_id:
                raise ValueError("Failed to create new version")
            
            return new_version_id
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error creating branch: {str(e)}")
            return None
    
    def list_branches(self) -> List[str]:
        """列出所有分支
        
        Returns:
            List[str]: 分支名称列表
        """
        try:
            branches = set()
            for version in self.list_versions():
                if version.metadata and "branch" in version.metadata:
                    branches.add(version.metadata["branch"])
            return sorted(list(branches))
            
        except Exception as e:
            self.logger.error(f"Error listing branches: {str(e)}")
            return []
    
    def get_branch_versions(self, branch_name: str) -> List[VersionData]:
        """获取分支的所有版本
        
        Args:
            branch_name: 分支名称
            
        Returns:
            List[VersionData]: 版本数据列表
        """
        try:
            if not branch_name:
                raise ValueError("Branch name cannot be empty")
            
            versions = []
            for version in self.list_versions():
                if version.metadata and version.metadata.get("branch") == branch_name:
                    versions.append(version)
            return sorted(versions, key=lambda x: x.created_at)
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error getting branch versions: {str(e)}")
            return []

    def update_version_metadata(self, version_id: str, metadata: Dict[str, Any]) -> bool:
        """更新版本元数据
        
        Args:
            version_id: 版本ID
            metadata: 元数据
            
        Returns:
            bool: 是否更新成功
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            if not metadata:
                raise ValueError("Metadata cannot be empty")
            
            # 获取版本数据
            version = self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # 更新元数据
            version.metadata.update(metadata)
            
            # 保存版本数据
            version_file = os.path.join(self.storage_dir, f"{version_id}.json")
            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(version.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error updating version metadata: {str(e)}")
            return False
    
    def get_version_metadata(self, version_id: str) -> Optional[Dict[str, Any]]:
        """获取版本元数据
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[Dict[str, Any]]: 元数据,如果不存在则返回None
        """
        try:
            if not version_id:
                raise ValueError("Version ID cannot be empty")
            
            # 获取版本数据
            version = self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            return version.metadata
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error getting version metadata: {str(e)}")
            return None
    
    def search_versions(self, query: Dict[str, Any]) -> List[VersionData]:
        """搜索版本
        
        Args:
            query: 查询条件
            
        Returns:
            List[VersionData]: 版本数据列表
        """
        try:
            if not query:
                raise ValueError("Query cannot be empty")
            
            versions = []
            for version in self.list_versions():
                match = True
                for key, value in query.items():
                    if key == "metadata":
                        if not version.metadata:
                            match = False
                            break
                        for meta_key, meta_value in value.items():
                            if meta_key not in version.metadata:
                                match = False
                                break
                            if meta_key == "tags":
                                # 检查标签是否存在
                                if not isinstance(version.metadata[meta_key], list):
                                    match = False
                                    break
                                if not isinstance(meta_value, list):
                                    match = False
                                    break
                                # 检查是否包含任一标签
                                if not any(tag in version.metadata[meta_key] for tag in meta_value):
                                    match = False
                                    break
                            elif version.metadata[meta_key] != meta_value:
                                match = False
                                break
                    elif getattr(version, key) != value:
                        match = False
                        break
                if match:
                    versions.append(version)
            return versions
            
        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error searching versions: {str(e)}")
            return []

    def unregister_pre_save_hook(self, hook: Callable[[Dict[str, Any], Dict[str, Any]], Tuple[Dict[str, Any], Dict[str, Any]]]):
        """注销预保存钩子
        
        Args:
            hook: 钩子函数
        """
        if hook in self.pre_save_hooks:
            self.pre_save_hooks.remove(hook)
    
    def unregister_post_save_hook(self, hook: Callable[[str, Dict[str, Any], Dict[str, Any]], None]):
        """注销后保存钩子
        
        Args:
            hook: 钩子函数
        """
        if hook in self.post_save_hooks:
            self.post_save_hooks.remove(hook) 