import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Typography,
  Button,
  CircularProgress,
} from '@mui/material';
import { agentApi } from '../../../services/api';

interface SectionEditorProps {
  title: string;
  content: string;
  onContentChange: (content: string) => void;
  onSave: () => void;
  writingId: string;
  sectionId: string;
  onPrev?: () => void;
  onNext?: () => void;
  isLastSection?: boolean;
}

const SectionEditor: React.FC<SectionEditorProps> = ({
  title,
  content,
  onContentChange,
  onSave,
  writingId,
  sectionId,
  onPrev,
  onNext,
  isLastSection = false,
}) => {
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateContent = async () => {
    setIsGenerating(true);
    try {
      const response = await agentApi.generate(writingId, sectionId);
      if (response && response.data) {
        onContentChange(response.data);
        onSave();
      }
    } catch (error) {
      console.error('生成内容失败:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5">
          {title}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerateContent}
          disabled={isGenerating}
          sx={{ minWidth: 120 }}
        >
          {isGenerating ? <CircularProgress size={24} /> : '生成内容'}
        </Button>
      </Box>
      
      <TextField
        fullWidth
        multiline
        minRows={10}
        maxRows={20}
        value={content}
        onChange={(e) => onContentChange(e.target.value)}
        variant="outlined"
        placeholder="在这里开始写作..."
      />
      
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        mt: 2,
        gap: 2
      }}>
        <Box>
          {onPrev && (
            <Button
              variant="contained"
              color="primary"
              onClick={onPrev}
            >
              上一步
            </Button>
          )}
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={onSave}
          >
            保存
          </Button>
          {!isLastSection && onNext && (
            <Button
              variant="contained"
              color="primary"
              onClick={onNext}
            >
              下一步
            </Button>
          )}
        </Box>
      </Box>
    </Paper>
  );
};

export default SectionEditor; 