import React, { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

interface DiscussionEditorProps {
  onSave?: () => void;
  onPrev?: () => void;
  onNext?: () => void;
  writingId: string;
  sectionId: string;
}

export const DiscussionEditor: React.FC<DiscussionEditorProps> = ({
  onSave,
  onPrev,
  onNext,
  writingId,
  sectionId
}) => {
  const [content, setContent] = useState({
    resultInterpretation: '',
    researchComparison: '',
    theoreticalImplications: '',
    practicalImplications: ''
  });

  const handleContentChange = (field: string) => (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  return (
    <Box sx={{ padding: '24px' }}>
      <Typography variant="h4" gutterBottom>讨论</Typography>
      
      <Alert 
        severity="info"
        icon={<InfoIcon />}
        sx={{ mb: 3 }}
      >
        讨论Agent开发中，用户可以自行输入文本，后续将支持根据实证结果自动生成讨论内容。
      </Alert>

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr', gap: 3 }}>
        <Box>
          <Typography variant="h6" gutterBottom>结果解释</Typography>
          <TextField
            fullWidth
            multiline
            rows={6}
            placeholder="请解释实证分析的主要发现，包括各变量的影响方向、显著性及其经济含义..."
            variant="outlined"
            value={content.resultInterpretation}
            onChange={handleContentChange('resultInterpretation')}
          />
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>研究比较</Typography>
          <TextField
            fullWidth
            multiline
            rows={6}
            placeholder="请将本研究的发现与现有文献进行比较，说明异同点及可能的原因..."
            variant="outlined"
            value={content.researchComparison}
            onChange={handleContentChange('researchComparison')}
          />
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>理论意义</Typography>
          <TextField
            fullWidth
            multiline
            rows={6}
            placeholder="请讨论本研究对现有理论的贡献，包括理论验证、理论扩展或理论创新..."
            variant="outlined"
            value={content.theoreticalImplications}
            onChange={handleContentChange('theoreticalImplications')}
          />
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>实践启示</Typography>
          <TextField
            fullWidth
            multiline
            rows={6}
            placeholder="请讨论本研究的实践意义，包括对政策制定、企业管理等方面的启示..."
            variant="outlined"
            value={content.practicalImplications}
            onChange={handleContentChange('practicalImplications')}
          />
        </Box>

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
              下一步
            </Button>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default DiscussionEditor; 