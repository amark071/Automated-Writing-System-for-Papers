import React, { useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
  Menu,
  MenuItem,
} from '@mui/material';
import { writingApi } from '../../../services/api';
import { previewAnalysis, exportAnalysis, PreviewResponse, ExportResponse, IntroductionData } from '../../../services/api';
import { generateIntroductionContent } from './AgentDialog';

interface PreviewAndExportProps {
  sectionId: string;
  content: string;
  onPreview?: () => void;
  onExport?: () => void;
  type?: 'writing' | 'empirical';
  introductionData?: IntroductionData;
}

const PreviewAndExport: React.FC<PreviewAndExportProps> = ({
  sectionId,
  content,
  onPreview,
  onExport,
  type = 'writing',
  introductionData,
}) => {
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewContent, setPreviewContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [exportAnchorEl, setExportAnchorEl] = useState<null | HTMLElement>(null);

  const handlePreview = async () => {
    setLoading(true);
    setError(null);
    try {
      let response: string | PreviewResponse;
      if (type === 'writing') {
        response = await writingApi.getPreview(sectionId);
      } else {
        response = await previewAnalysis({
          sectionId,
          content,
        });
      }
      
      // 处理响应数据
      if (typeof response === 'string') {
        setPreviewContent(response);
      } else if (response.success && response.data?.html) {
        setPreviewContent(response.data.html);
      } else {
        throw new Error('预览内容获取失败');
      }
      
      setPreviewOpen(true);
      onPreview?.();
    } catch (err) {
      setError('获取预览内容失败');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: 'docx' | 'pdf') => {
    setLoading(true);
    setError(null);
    try {
      let response: Blob | ExportResponse;
      if (type === 'writing') {
        response = await writingApi.exportToWord(sectionId);
      } else {
        response = await exportAnalysis({
          sectionId,
          content,
          format,
        });
      }

      // 处理响应数据
      if (response instanceof Blob) {
        const url = window.URL.createObjectURL(response);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${type === 'writing' ? '论文' : '实证分析'}_${sectionId}.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } else if (response.success && response.data?.fileUrl) {
        window.open(response.data.fileUrl, '_blank');
      } else {
        throw new Error('导出失败');
      }
      
      onExport?.();
    } catch (err) {
      setError('导出文档失败');
    } finally {
      setLoading(false);
      setExportAnchorEl(null);
    }
  };

  return (
    <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
      {error && (
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      <Button
        variant="outlined"
        onClick={handlePreview}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : '预览'}
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={(e) => setExportAnchorEl(e.currentTarget)}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : '导出'}
      </Button>

      <Menu
        anchorEl={exportAnchorEl}
        open={Boolean(exportAnchorEl)}
        onClose={() => setExportAnchorEl(null)}
      >
        <MenuItem onClick={() => handleExport('docx')}>
          导出为Word文档
        </MenuItem>
        <MenuItem onClick={() => handleExport('pdf')}>
          导出为PDF文档
        </MenuItem>
      </Menu>

      <Dialog
        open={previewOpen}
        onClose={() => setPreviewOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{type === 'writing' ? '论文预览' : '实证分析预览'}</DialogTitle>
        <DialogContent>
          <div dangerouslySetInnerHTML={{ __html: previewContent }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewOpen(false)}>关闭</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PreviewAndExport; 