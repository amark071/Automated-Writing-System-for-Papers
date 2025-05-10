from flask import Blueprint, request, jsonify
from paper_automation.agent_system.paper_agent.content.introduction.policy_processor import PolicyProcessor

introduction_bp = Blueprint('introduction', __name__)

POLICY_DIR = "/Users/yorge/Desktop/未命名文件夹/data/raw/政策文件"
policy_processor = PolicyProcessor(POLICY_DIR)
policy_processor.load_policies()  # 预加载所有政策文件

@introduction_bp.route('/api/introduction/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'field' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
            
        title = data['title']
        field = data['field']
        
        if field == 'policyBackground':
            # 使用PolicyProcessor生成政策背景
            content = policy_processor.generate_policy_background(title)
            return jsonify({'content': content})
        else:
            # 其他字段的生成逻辑...
            return jsonify({'error': '暂不支持该字段的生成'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500 