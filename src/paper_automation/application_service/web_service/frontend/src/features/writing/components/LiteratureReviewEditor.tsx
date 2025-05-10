// TODO: 文献综述组件待完成功能
// 1. 文献搜索功能
//    - 基于标题搜索文献库
//    - 支持高级搜索选项（时间范围、期刊级别等）
//    - 搜索结果展示和筛选
//
// 2. 文献组织方式
//    - 时间顺序
//    - 主题分类
//    - 研究方法
//    - 研究结论
//
// 3. 文献综述Agent集成
//    - 研究现状生成
//    - 研究差距识别
//    - 文献评价总结
//
// 4. 文献管理功能
//    - 文献收藏
//    - 文献分类
//    - 文献笔记
//
// 5. 导出功能
//    - 导出文献列表
//    - 导出文献综述
//    - 导出参考文献

import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Typography,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  SelectChangeEvent,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material';
import { AgentMessage, apiService } from '../../../services/api';

interface LiteratureReviewEditorProps {
  onSave: (data: LiteratureReviewData) => void;
  initialData?: LiteratureReviewData;
  title: string;
  writingId: string;
  sectionId: string;
  onPrev?: () => void;
  onNext?: () => void;
}

export interface LiteratureReviewData {
  organizationMethod: string;
  researchStatus: string;
  researchGaps: string;
  literatureEvaluation: string;
  references: string[];
}

const organizationMethods = [
  '时间顺序',
  '主题分类',
  '研究方法',
  '研究结论',
];

const LiteratureReviewEditor: React.FC<LiteratureReviewEditorProps> = ({
  onSave,
  initialData,
  title,
  writingId,
  sectionId,
  onPrev,
  onNext,
}) => {
  const [data, setData] = useState<LiteratureReviewData>(
    initialData || {
      organizationMethod: '',
      researchStatus: '',
      researchGaps: '',
      literatureEvaluation: '',
      references: [],
    }
  );

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof LiteratureReviewData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent
  ) => {
    setData({ ...data, [field]: event.target.value });
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.agent.generate(writingId, sectionId);
      setData({
        ...data,
        researchStatus: response.researchStatus,
        researchGaps: response.researchGaps,
        literatureEvaluation: response.literatureEvaluation,
        references: response.references || [],
      });
    } catch (err) {
      setError('生成文献综述失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {error && (
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>文献组织方式</InputLabel>
          <Select
            value={data.organizationMethod}
            onChange={handleChange('organizationMethod')}
            label="文献组织方式"
          >
            {organizationMethods.map(method => (
              <MenuItem key={method} value={method}>
                {method}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
          
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerate}
          disabled={loading || !data.organizationMethod}
        >
          {loading ? <CircularProgress size={24} /> : '生成文献综述'}
        </Button>
      </Box>

      <TextField
        fullWidth
        multiline
        rows={8}
        label="研究现状"
        value={data.researchStatus}
        onChange={handleChange('researchStatus')}
        variant="outlined"
        helperText="描述当前研究领域的主要进展和成果"
      />

      <TextField
        fullWidth
        multiline
        rows={6}
        label="研究差距"
        value={data.researchGaps}
        onChange={handleChange('researchGaps')}
        variant="outlined"
        helperText="指出现有研究的不足和需要进一步研究的方向"
      />

      <TextField
        fullWidth
        multiline
        rows={6}
        label="文献评价"
        value={data.literatureEvaluation}
        onChange={handleChange('literatureEvaluation')}
        variant="outlined"
        helperText="对现有文献进行综合评价，总结研究趋势"
      />

      <Divider />

      <Paper 
        variant="outlined" 
        sx={{ 
          p: 2, 
          maxHeight: '300px', 
          overflowY: 'auto',
          bgcolor: 'background.default' 
        }}
      >
        <Typography variant="h6" gutterBottom>
          参考文献列表
        </Typography>
        {data.references.map((reference, index) => (
          <Typography key={index} paragraph>
            [{index + 1}] {reference}
          </Typography>
        ))}
      </Paper>

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
            onClick={() => onSave(data)}
          >
            保存
          </Button>
          {onNext && (
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
    </Box>
  );
};

export default LiteratureReviewEditor; 