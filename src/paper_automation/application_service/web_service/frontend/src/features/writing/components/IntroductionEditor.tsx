import React, { useState } from 'react';
import {
  Box,
  TextField,
  Typography,
  Button,
  CircularProgress,
} from '@mui/material';
import { agentApi } from '../../../services/api';

interface IntroductionEditorProps {
  onSave: (data: IntroductionData) => void;
  initialData?: IntroductionData;
  writingId: string;
  sectionId: string;
  onNext: () => void;
}

export interface IntroductionData {
  title: string;
  subtitle?: string;
  point: string;
  socialBackground: string;
  policyBackground: string;
  theoreticalBackground: string;
  researchConclusion: string;
  marginalContribution: string;
}

const IntroductionEditor: React.FC<IntroductionEditorProps> = ({
  onSave,
  initialData,
  writingId,
  sectionId,
  onNext,
}) => {
  const [data, setData] = useState<IntroductionData>(
    initialData || {
      title: '',
      subtitle: '',
      point: '',
      socialBackground: '',
      policyBackground: '',
      theoreticalBackground: '',
      researchConclusion: '',
      marginalContribution: '',
    }
  );
  const [isGenerating, setIsGenerating] = useState(false);

  const handleChange = (field: keyof IntroductionData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setData({ ...data, [field]: event.target.value });
  };

  const generateIntroductionContent = () => {
    return `
      <h2>引言</h2>
      <h3>1. 标题</h3>
      <p>${data.title}</p>
      ${data.subtitle ? `<h3>2. 副标题</h3><p>${data.subtitle}</p>` : ''}
      <h3>${data.subtitle ? '3' : '2'}. 点题</h3>
      <p>${data.point}</p>
      <h3>${data.subtitle ? '4' : '3'}. 社会背景</h3>
      <p>${data.socialBackground}</p>
      <h3>${data.subtitle ? '5' : '4'}. 政策背景</h3>
      <p>${data.policyBackground}</p>
      <h3>${data.subtitle ? '6' : '5'}. 理论背景</h3>
      <p>${data.theoreticalBackground}</p>
      <h3>${data.subtitle ? '7' : '6'}. 研究结论</h3>
      <p>${data.researchConclusion}</p>
      <h3>${data.subtitle ? '8' : '7'}. 边际贡献</h3>
      <p>${data.marginalContribution}</p>
    `;
  };

  const handleGenerateContent = async () => {
    setIsGenerating(true);
    try {
      const response = await agentApi.generate(writingId, sectionId);
      if (response && response.data) {
        setData(response.data);
        onSave(response.data);
      }
    } catch (error) {
      console.error('生成内容失败:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const renderField = (field: keyof IntroductionData, label: string, rows: number = 4) => (
    <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
      <TextField
        fullWidth
        multiline={rows > 1}
        rows={rows}
        label={label}
        value={data[field]}
        onChange={handleChange(field)}
        variant="outlined"
      />
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
  );

  return (
    <Box sx={{ p: 3, display: 'flex', flexDirection: 'column', gap: 3 }}>
      {renderField('title', '标题', 1)}
      {renderField('subtitle', '副标题', 1)}
      {renderField('point', '点题')}
      {renderField('socialBackground', '社会背景')}
      {renderField('policyBackground', '政策背景')}
      {renderField('theoreticalBackground', '理论背景')}
      {renderField('researchConclusion', '研究结论')}
      {renderField('marginalContribution', '边际贡献')}
      
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'flex-end',
        gap: 2,
        mt: 2
      }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => onSave(data)}
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
  );
};

export default IntroductionEditor; 