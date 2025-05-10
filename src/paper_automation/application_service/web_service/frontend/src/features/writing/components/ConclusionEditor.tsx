import React, { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

interface ConclusionEditorProps {
  onSave?: () => void;
  onPrev?: () => void;
  onNext?: () => void;
  writingId: string;
  sectionId: string;
}

export const ConclusionEditor: React.FC<ConclusionEditorProps> = ({
  onSave,
  onPrev,
  onNext,
  writingId,
  sectionId
}) => {
  const [content, setContent] = useState({
    researchConclusion: '',
    policyRecommendations: ''
  });

  const handleContentChange = (field: string) => (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  return (
    <Box sx={{ padding: '24px' }}>
      <Typography variant="h4" gutterBottom>结论</Typography>
      
      <Alert 
        severity="info"
        icon={<InfoIcon />}
        sx={{ mb: 3 }}
      >
        结论Agent开发中，用户可以自行输入文本。后续将支持根据研究背景、数据来源、研究方法、实证分析结果和讨论内容自动生成结论。
      </Alert>

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr', gap: 3 }}>
        <Box>
          <Typography variant="h6" gutterBottom>研究结论</Typography>
          <TextField
            fullWidth
            multiline
            rows={10}
            placeholder="请按照以下结构撰写研究结论：
1. 第一句总结本文的研究背景（来自引言）
2. 第二句说明使用的数据来源、研究方法和研究问题
3. 详细阐述研究发现（来自实证分析结果和讨论）"
            variant="outlined"
            value={content.researchConclusion}
            onChange={handleContentChange('researchConclusion')}
          />
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>政策建议</Typography>
          <TextField
            fullWidth
            multiline
            rows={10}
            placeholder="请根据上述研究发现，提出相应的政策建议..."
            variant="outlined"
            value={content.policyRecommendations}
            onChange={handleContentChange('policyRecommendations')}
          />
        </Box>

        {/* 底部导航按钮 */}
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={onPrev}
          >
            上一步
          </Button>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={onSave}
            >
              保存
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={onNext}
            >
              完成
            </Button>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default ConclusionEditor; 