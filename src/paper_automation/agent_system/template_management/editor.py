"""Template editing module

This module implements paper template editing functionality, including content editing, structure editing and style editing.
"""

from typing import Dict, List, Any, Optional, Callable, Tuple, Union
from datetime import datetime
import logging
import os
import json
import tempfile
import uuid
from dataclasses import dataclass, asdict
from .base.template import Template
import copy

VALID_OPERATION_TYPES = ["modify", "add", "delete", "move", "copy"]

@dataclass
class EditOperation:
    """编辑操作"""
    operation_id: str
    operation_type: str
    target_path: List[str]
    value: Any = None
    source_path: Optional[List[str]] = None
    timestamp: Optional[datetime] = None
    author: str = "anonymous"
    description: str = ""
    metadata: Dict[str, Any] = None
    old_data: Dict[str, Any] = None
    new_data: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat() if self.timestamp else None

        # 处理 old_data 和 new_data 中的 Template 对象
        if isinstance(self.old_data, Template):
            data['old_data'] = self.old_data.to_dict()
        if isinstance(self.new_data, Template):
            data['new_data'] = self.new_data.to_dict()

        return data
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EditOperation':
        """从字典创建实例"""
        if 'timestamp' in data:
            data['timestamp'] = datetime.fromisoformat(data['timestamp']) if data['timestamp'] else None
        return cls(**data)

class DateTimeEncoder(json.JSONEncoder):
    """处理日期时间的 JSON 编码器"""
    def default(self, obj):
        """处理特殊类型的序列化"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Template):
            return obj.to_dict()
        elif isinstance(obj, EditOperation):
            return obj.to_dict()
        elif isinstance(obj, EditSession):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        elif hasattr(obj, 'to_dict'):  # 处理其他可能的对象
            return obj.to_dict()
        return str(obj)  # 如果无法序列化，转换为字符串

@dataclass
class EditSession:
    """编辑会话"""
    session_id: str
    template_id: str
    template_data: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    history: List[EditOperation] = None
    redo_stack: List[EditOperation] = None
    current_version: int = 0
    
    def __post_init__(self):
        """初始化后的处理"""
        self.logger = logging.getLogger(__name__)
        if not self.session_id:
            raise ValueError("Session ID cannot be empty")
        if not self.template_id:
            raise ValueError("Template ID cannot be empty")
        if not self.template_data:
            raise ValueError("Template data cannot be empty")
            
        if self.metadata is None:
            self.metadata = {
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        if self.history is None:
            self.history = []
        if self.redo_stack is None:
            self.redo_stack = []
            
    def __getitem__(self, key: str) -> Any:
        """支持下标访问"""
        if key == "session_id":
            return self.session_id
        elif key == "template_id":
            return self.template_id
        elif key == "template_data":
            return self.template_data
        elif key == "template":
            return Template(
                template_id=self.template_id,
                name=self.template_data.get("name", ""),
                description=self.template_data.get("description", ""),
                structure=self.template_data.get("structure", {}),
                elements=self.template_data.get("elements", {}),
                relations=self.template_data.get("relations", {}),
                content=self.template_data.get("content", {}),
                metadata=self.metadata.copy(),
                template_data=self.template_data.copy(),
                style=self.template_data.get("style", {}),
                version=self.template_data.get("version", "1.0.0")
            )
        elif key == "metadata":
            return self.metadata
        elif key == "history":
            return self.history
        elif key == "redo_stack":
            return self.redo_stack
        elif key == "current_version":
            return self.current_version
        else:
            raise KeyError(f"Key {key} not found")
            
    def add_history(self, operation: EditOperation) -> None:
        """添加历史记录"""
        if not isinstance(operation, EditOperation):
            raise ValueError("Operation must be an instance of EditOperation")
            
        # 删除当前版本之后的历史记录
        self.history = self.history[:self.current_version]
        
        # 添加新的操作
        self.history.append(operation)
        self.current_version += 1
        
        # 更新元数据
        self.metadata["updated_at"] = datetime.now()
        
    def undo(self) -> bool:
        """撤销操作"""
        if self.current_version > 0:
            self.current_version -= 1
            return True
        return False
        
    def redo(self) -> bool:
        """重做操作"""
        if self.current_version < len(self.history):
            self.current_version += 1
            return True
        return False
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        # 如果 template_data 是 Template 对象，转换为字典
        if isinstance(self.template_data, Template):
            template_dict = self.template_data.to_dict()
        else:
            template_dict = self.template_data.copy() if isinstance(self.template_data, dict) else self.template_data

        # 处理字典中的 Template 对象
        def process_dict(d):
            if isinstance(d, dict):
                return {k: process_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [process_dict(item) for item in d]
            elif isinstance(d, Template):
                return d.to_dict()
            elif isinstance(d, datetime):
                return d.isoformat()
            elif isinstance(d, EditOperation):
                return d.to_dict()
            return d

        # 处理元数据
        metadata = process_dict(self.metadata)

        # 处理历史记录
        history = []
        for op in self.history:
            op_dict = op.to_dict()
            op_dict = process_dict(op_dict)
            history.append(op_dict)

        # 处理重做栈
        redo_stack = []
        for op in self.redo_stack:
            op_dict = op.to_dict()
            op_dict = process_dict(op_dict)
            redo_stack.append(op_dict)

        return {
            'session_id': self.session_id,
            'template_id': self.template_id,
            'template_data': process_dict(template_dict),
            'metadata': metadata,
            'history': history,
            'redo_stack': redo_stack,
            'current_version': self.current_version
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EditSession":
        """从字典创建实例"""
        if not data:
            raise ValueError("Session data cannot be empty")
            
        return cls(
            session_id=data["session_id"],
            template_id=data["template_id"],
            template_data=data["template_data"],
            metadata=data.get("metadata"),
            history=[EditOperation.from_dict(op) for op in data.get("history", [])],
            redo_stack=[EditOperation.from_dict(op) for op in data.get("redo_stack", [])],
            current_version=data.get("current_version", 0)
        )

class SessionData:
    """会话数据类"""
    
    def __init__(self, session_id: str, template_id: str, template_data: Dict[str, Any],
                 metadata: Dict[str, Any] = None):
        """初始化会话数据
        
        Args:
            session_id: 会话ID
            template_id: 模板ID
            template_data: 模板数据
            metadata: 元数据
        """
        self.session_id = session_id
        self.template_id = template_id
        self.template_data = template_data
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.edit_history = []
        self.current_index = -1

class TemplateEditor:
    """模板编辑器

    Attributes:
        temp_dir: 临时目录
        sessions: 会话字典
    """
    
    def __init__(self, temp_dir: Optional[str] = None):
        """初始化

        Args:
            temp_dir: 临时目录
        """
        self.temp_dir = temp_dir or os.path.join(os.getcwd(), "temp")
        self.sessions = {}
        
        # 确保临时目录存在
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def create_session(self, template_id: str, template_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
        """创建会话(兼容旧接口)"""
        return self.create_edit_session(template_id, template_data, metadata)
        
    def create_edit_session(self, template_id: str, template: Union[Dict[str, Any], Template], metadata: Optional[Dict[str, Any]] = None) -> str:
        """创建编辑会话"""
        session_id = str(uuid.uuid4())
        
        # 如果传入的是字典，创建 Template 对象
        if isinstance(template, dict):
            template_obj = Template(
                template_id=template_id,
                name=template.get('name', '未命名模板'),
                description=template.get('description', ''),
                structure=template.get('structure', {}),
                elements=template.get('elements', {}),
                relations=template.get('relations', {}),
                content=template.get('content', {}),
                metadata=template.get('metadata', {}),
                template_data=template.copy(),
                style=template.get('style', {}),
                version=template.get('version', '1.0.0')
            )
        else:
            template_obj = template

        # 创建会话
        session = EditSession(
            session_id=session_id,
            template_id=template_id,
            template_data=template_obj.to_dict(),  # 存储字典形式
            metadata=metadata.copy() if metadata else {}
        )
        
        # 保存会话
        self.sessions[session_id] = session
        
        # 将会话转换为字典
        session_dict = session.to_dict()
        
        # 确保临时目录存在
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # 保存会话文件
        session_file = os.path.join(self.temp_dir, f"{session_id}.json")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_dict, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
            
        return session_id
        
    def close_session(self, session_id: str) -> None:
        """关闭会话
        
        Args:
            session_id: 会话ID
            
        Raises:
            ValueError: 如果会话不存在
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # 从内存中移除
        del self.sessions[session_id]
        
        # 删除会话文件
        session_file = os.path.join(self.temp_dir, f"{session_id}.json")
        if os.path.exists(session_file):
            os.remove(session_file)

    def get_edit_session(self, session_id: str) -> Dict[str, Any]:
        """获取编辑会话"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 创建 Template 对象
        template = Template(
            template_id=session.template_id,
            name=session.template_data.get('name', '未命名模板'),
            description=session.template_data.get('description', ''),
            structure=session.template_data.get('structure', {}),
            elements=session.template_data.get('elements', {}),
            relations=session.template_data.get('relations', {}),
            content=session.template_data.get('content', {}),
            metadata=session.metadata.copy(),
            template_data=session.template_data.copy(),
            style=session.template_data.get('style', {}),
            version=session.template_data.get('version', '1.0.0')
        )
        
        return {
            'session_id': session.session_id,
            'template_id': session.template_id,
            'template': template,
            'metadata': session.metadata,
            'current_version': session.current_version
        }
        
    def list_sessions(self) -> List[EditSession]:
        """列出所有会话
        
        Returns:
            List[EditSession]: 会话列表
        """
        return list(self.sessions.values())
        
    def update_template_content(self, session_id: str, content: Dict[str, Any]) -> None:
        """更新模板内容"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 更新模板结构
        template_data = session.template_data
        template_data['structure'] = content
        
        # 创建编辑操作
        operation = EditOperation(
            operation_id=str(uuid.uuid4()),
            operation_type='update_content',
            target_path='structure',
            value=content,
            timestamp=datetime.now(),
            description='更新模板内容',
            old_data=session.template_data.get('structure', {}),
            new_data=content
        )
        
        # 添加到历史记录
        session.history.append(operation)
        session.current_version = len(session.history)
        
        # 保存会话
        self.save_session(session_id)

    def import_session(self, data: Dict[str, Any]) -> str:
        """导入会话

        Args:
            data: 包含template_id和template_data的字典

        Returns:
            str: 会话ID

        Raises:
            ValueError: 如果数据格式不正确
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        if "template_id" not in data or "template_data" not in data:
            raise ValueError("Data must contain template_id and template_data")
            
        return self.create_session(
            template_id=data["template_id"],
            template_data=data["template_data"],
            metadata=data.get("metadata")
        )
        
    def update_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> None:
        """更新会话元数据"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 只更新提供的元数据字段,不添加默认字段
        session.metadata.update(metadata)
        
        # 保存会话
        self.save_session(session_id)

    def validate_template(self, session_id: str) -> Dict[str, Any]:
        """验证模板

        Args:
            session_id: 会话ID

        Returns:
            Dict[str, Any]: 包含验证结果和元数据的字典

        Raises:
            ValueError: 如果会话不存在
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
            
        # 更新元数据
        session.metadata["updated_at"] = datetime.now()
        session.metadata["status"] = "validated"
        
        # 处理字典中的 Template 对象
        def process_dict(d):
            if isinstance(d, dict):
                return {k: process_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [process_dict(item) for item in d]
            elif isinstance(d, Template):
                return d.to_dict()
            elif isinstance(d, datetime):
                return d.isoformat()
            return d
            
        metadata = process_dict(session.metadata)
        
        # 验证模板
        is_valid = True
        errors = []
        
        # 检查必要字段
        if isinstance(session.template_data, Template):
            template = session.template_data
            if not template.structure:
                is_valid = False
                errors.append("模板缺少必要结构")
            if not template.name:
                is_valid = False
                errors.append("模板缺少名称")
        else:
            template_dict = session.template_data
            if not template_dict.get('structure'):
                is_valid = False
                errors.append("模板缺少必要结构")
            if not template_dict.get('name'):
                is_valid = False
                errors.append("模板缺少名称")
        
        # 保存会话
        self.save_session(session_id)
        
        return {
            "template_id": session.template_id,
            "metadata": metadata,
            "is_valid": is_valid,
            "errors": errors
        }
        
    def export_template(self, session_id: str) -> Dict[str, Any]:
        """导出模板

        Args:
            session_id: 会话ID

        Returns:
            Dict[str, Any]: 包含模板数据的字典

        Raises:
            ValueError: 如果会话不存在
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 更新元数据
        session.metadata["status"] = "exported"
        session.metadata["exported_at"] = datetime.now().isoformat()
        
        # 创建模板对象
        template = Template(
            template_id=session.template_id,
            name=session.template_data.get("name", "未命名模板"),
            description=session.template_data.get("description", ""),
            structure=session.template_data.get("structure", {}),
            metadata=session.metadata,
            template_data=session.template_data
        )
        
        # 保存会话
        self.save_session(session_id)
        
        return {
            "session_id": session_id,
            "template_id": session.template_id,
            "template": template,
            "metadata": session.metadata,
            "created_time": session.metadata.get("timestamp", ""),
            "updated_time": session.metadata.get("updated_at", "")
        }
        
    def save_session(self, session_id: str) -> None:
        """保存编辑会话到文件

        Args:
            session_id: 会话ID

        Raises:
            ValueError: 如果会话不存在
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
            
        # 确保temp_dir目录存在
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # 将会话转换为字典
        session_dict = session.to_dict()
        
        # 保存会话文件
        session_file = os.path.join(self.temp_dir, f"{session_id}.json")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_dict, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
            
    def apply_edit(self, session_id: str, edit_data: Dict[str, Any]) -> None:
        """应用编辑操作"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        if not isinstance(edit_data, dict):
            raise ValueError("Edit data must be a dictionary")
        
        # 保存当前状态
        current_state = copy.deepcopy(session.template_data)
        
        try:
            # 获取编辑路径和值
            path = edit_data.get("path", [])
            value = edit_data.get("value")
            
            # 更新指定路径的值
            target = session.template_data
            for i, key in enumerate(path[:-1]):
                if isinstance(key, int):
                    if not isinstance(target, dict):
                        target = target[key]
                    else:
                        if key not in target:
                            target[key] = {}
                        target = target[key]
                else:
                    if key not in target:
                        target[key] = {}
                    target = target[key]
                    
            if path:
                if isinstance(path[-1], int):
                    target[path[-1]] = value
                else:
                    if path[-1] not in target:
                        target[path[-1]] = {}
                    target[path[-1]] = value
                
            # 创建编辑操作
            operation = EditOperation(
                operation_id=str(uuid.uuid4()),
                operation_type=edit_data.get("type", "modify"),
                target_path=path,
                value=value,
                timestamp=datetime.now(),
                description="Apply edit",
                old_data=current_state,
                new_data=copy.deepcopy(session.template_data)
            )
            
            # 添加到历史记录
            session.history.append(operation)
            session.current_version = len(session.history)
            
            # 更新元数据
            session.metadata["updated_at"] = datetime.now().isoformat()
            
            # 保存会话
            self.save_session(session_id)
            
        except Exception as e:
            # 恢复原始状态
            session.template_data = current_state
            raise ValueError(f"Failed to apply edit: {str(e)}")

    def undo_edit(self, session_id: str) -> Dict[str, Any]:
        """撤销编辑操作
        
        Args:
            session_id: 会话ID
        
        Returns:
            Dict[str, Any]: 包含会话ID、模板ID、当前版本和元数据的字典
        
        Raises:
            ValueError: 如果会话不存在或没有可撤销的操作
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        if not session.history or session.current_version <= 0:
            raise ValueError("No operations to undo")
        
        # 获取当前操作
        operation = session.history[session.current_version - 1]
        
        # 恢复旧数据
        session.template_data = copy.deepcopy(operation.old_data)
        
        # 更新版本
        session.current_version -= 1
        
        # 更新元数据
        session.metadata["updated_at"] = datetime.now().isoformat()
        
        # 保存会话
        self.save_session(session_id)
        
        return {
            "session_id": session_id,
            "template_id": session.template_id,
            "current_version": session.current_version,
            "metadata": session.metadata
        }
            
    def redo_edit(self, session_id: str) -> Dict[str, Any]:
        """重做编辑操作
        
        Args:
            session_id: 会话ID
        
        Returns:
            Dict[str, Any]: 包含会话ID、模板ID、当前版本和元数据的字典
        
        Raises:
            ValueError: 如果会话不存在或没有可重做的操作
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        if not session.history or session.current_version >= len(session.history):
            raise ValueError("No operations to redo")
        
        # 获取当前操作
        operation = session.history[session.current_version]
        
        # 应用新数据
        session.template_data = copy.deepcopy(operation.new_data)
        
        # 更新版本
        session.current_version += 1
        
        # 更新元数据
        session.metadata["updated_at"] = datetime.now().isoformat()
        
        # 保存会话
        self.save_session(session_id)
        
        return {
            "session_id": session_id,
            "template_id": session.template_id,
            "current_version": session.current_version,
            "metadata": session.metadata
        }
            
    def get_session(self, session_id: str) -> EditSession:
        """获取会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            EditSession: 会话对象
            
        Raises:
            ValueError: 如果会话不存在
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        return self.sessions[session_id]
        
    def export_session(self, session_id: str) -> Dict[str, Any]:
        """导出会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            Dict[str, Any]: 包含会话数据的字典
        
        Raises:
            ValueError: 如果会话不存在
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 更新元数据
        session.metadata["status"] = "exported"
        session.metadata["exported_at"] = datetime.now().isoformat()
        
        # 保存会话
        self.save_session(session_id)
        
        return {
            "session_id": session_id,
            "template_id": session.template_id,
            "template_data": session.template_data,
            "metadata": session.metadata,
            "history": [op.to_dict() for op in session.history],
            "current_version": session.current_version
        }
        
    def import_template(self, data: Dict[str, Any]) -> str:
        """从数据导入模板"""
        required_keys = ['template_id', 'template']
        if not all(key in data for key in required_keys):
            raise ValueError("Missing required keys in import data")
        
        template_id = data['template_id']
        template_data = data['template']
        metadata = data.get('metadata', {})
        
        # 创建新的编辑会话
        session_id = self.create_edit_session(
            template_id=template_id,
            template=template_data,
            metadata=metadata
        )
        
        return session_id
        
    def save_template(self, session_id: str) -> Template:
        """保存模板"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # 创建新的Template对象
        template = Template(
            template_id=session.template_id,
            name=session.template_data.get('name', '未命名模板'),
            description=session.template_data.get('description', ''),
            structure=session.template_data.get('structure', {}),
            elements=session.template_data.get('elements', {}),
            relations=session.template_data.get('relations', {}),
            content=session.template_data.get('content', {}),
            metadata=session.metadata.copy(),  # 复制元数据以避免引用
            template_data=session.template_data.copy(),
            style=session.template_data.get('style', {}),
            version=session.template_data.get('version', '1.0.0')
        )
        
        return template
        
    def get_template_history(self, session_id: str) -> List[Dict[str, Any]]:
        """获取模板历史记录"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        history = []
        
        for operation in session.history:
            if operation.operation_type == 'update_content':
                history.append({
                    'operation_id': operation.operation_id,
                    'timestamp': operation.timestamp,
                    'description': operation.description,
                    'content': operation.new_data
                })
        
        return history

    def rollback_to_version(self, session_id: str, version: int) -> None:
        """回滚到指定版本"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        if version < 0 or version >= len(session.history):
            raise ValueError(f"Invalid version number: {version}")
        
        # 获取目标版本的操作
        operation = session.history[version]
        
        # 更新模板数据
        if operation.operation_type == 'update_content':
            session.template_data['structure'] = operation.new_data
        
        # 更新当前版本
        session.current_version = version + 1
        
        # 保存会话
        self.save_session(session_id)

class Template:
    """模板类"""
    
    def __init__(
        self,
        template_id: str,
        name: str = "未命名模板",
        description: str = "",
        structure: Dict[str, Any] = None,
        elements: Dict[str, Any] = None,
        relations: Dict[str, Any] = None,
        content: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
        template_data: Dict[str, Any] = None,
        style: Dict[str, Any] = None,
        version: str = "1.0.0"
    ):
        self.template_id = template_id
        self.name = name
        self.description = description
        self.structure = structure or {}
        self.elements = elements or {}
        self.relations = relations or {}
        self.content = content or {}
        self.metadata = metadata or {}  # 不添加默认字段
        self.template_data = template_data or {}
        self.style = style or {}
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'template_id': self.template_id,
            'name': self.name,
            'description': self.description,
            'structure': self.structure,
            'elements': self.elements,
            'relations': self.relations,
            'content': self.content,
            'metadata': self.metadata,
            'template_data': self.template_data,
            'style': self.style,
            'version': self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """从字典创建模板"""
        return cls(
            template_id=data['template_id'],
            name=data.get('name', '未命名模板'),
            description=data.get('description', ''),
            structure=data.get('structure', {}),
            elements=data.get('elements', {}),
            relations=data.get('relations', {}),
            content=data.get('content', {}),
            metadata=data.get('metadata', {}),
            template_data=data.get('template_data', {}),
            style=data.get('style', {}),
            version=data.get('version', '1.0.0')
        ) 