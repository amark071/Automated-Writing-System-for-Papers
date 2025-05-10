import React from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
} from '@mui/material';

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
  isLastSection,
}) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={20}
        value={content}
        onChange={(e) => onContentChange(e.target.value)}
        variant="outlined"
        placeholder={`请输入${title}内容...`}
      />

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', mt: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={onPrev}
          disabled={!onPrev}
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
          {onNext && (
            <Button
              variant="contained"
              color="primary"
              onClick={onNext}
            >
              {isLastSection ? '完成' : '下一步'}
            </Button>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default SectionEditor; 