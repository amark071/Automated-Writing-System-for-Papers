import React from 'react';
import { Button, CircularProgress } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';

interface SaveButtonProps {
  onSave: () => void;
  isSaving: boolean;
  isDirty: boolean;
  autoSave?: boolean;
  autoSaveInterval?: number;
}

const SaveButton: React.FC<SaveButtonProps> = ({
  onSave,
  isSaving,
  isDirty,
  autoSave = false,
  autoSaveInterval = 30000, // 默认30秒
}) => {
  React.useEffect(() => {
    let timer: NodeJS.Timeout;

    if (autoSave && isDirty) {
      timer = setInterval(() => {
        onSave();
      }, autoSaveInterval);
    }

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [autoSave, isDirty, onSave, autoSaveInterval]);

  return (
    <Button
      variant="contained"
      color="primary"
      startIcon={isSaving ? <CircularProgress size={20} /> : <SaveIcon />}
      onClick={onSave}
      disabled={isSaving || !isDirty}
    >
      {isSaving ? '保存中...' : '保存'}
    </Button>
  );
};

export default SaveButton; 