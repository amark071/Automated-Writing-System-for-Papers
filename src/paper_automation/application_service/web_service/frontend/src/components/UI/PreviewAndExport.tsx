import React from 'react';
import { Box, Button } from '@mui/material';
import PreviewIcon from '@mui/icons-material/Preview';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

interface PreviewAndExportProps {
  sectionId: string;
  content: string;
  type: 'writing' | 'section';
  introductionData?: any;
}

export const PreviewAndExport: React.FC<PreviewAndExportProps> = ({
  sectionId,
  content,
  type,
  introductionData,
}) => {
  const handlePreview = () => {
    // TODO: 实现预览功能
    console.log('Preview:', { sectionId, content, type, introductionData });
  };

  const handleExport = () => {
    // TODO: 实现导出功能
    console.log('Export:', { sectionId, content, type, introductionData });
  };

  return (
    <Box sx={{ display: 'flex', gap: 1 }}>
      <Button
        variant="outlined"
        startIcon={<PreviewIcon />}
        onClick={handlePreview}
      >
        预览
      </Button>
      <Button
        variant="contained"
        startIcon={<FileDownloadIcon />}
        onClick={handleExport}
      >
        导出
      </Button>
    </Box>
  );
}; 