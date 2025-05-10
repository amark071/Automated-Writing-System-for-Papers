import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
} from '@mui/material';
import { writingApi } from '../../../services/api';
import { useApi } from '../../../hooks/useApi';

const disciplines = [
  '经济学',
  '管理学',
  '社会学',
  '政治学',
  '法学',
  '教育学',
  '心理学',
  '历史学',
  '哲学',
  '文学',
];

const paperTypes = [
  '期刊论文',
  '学位论文',
  '研究报告',
];

const WritingTemplate = () => {
  const navigate = useNavigate();
  const [discipline, setDiscipline] = useState('经济学');
  const [paperType, setPaperType] = useState('期刊论文');

  const handleCreate = async () => {
    try {
      // 保存选择的学科和论文类型到 localStorage，为将来扩展做准备
      localStorage.setItem('selectedDiscipline', discipline);
      localStorage.setItem('selectedPaperType', paperType);
      
      // 由于目前只有一套模板，直接创建一个新的写作并跳转
      navigate('/writing/editor/new');
    } catch (err) {
      console.error('创建失败:', err);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
          <Typography variant="h4" align="center" gutterBottom sx={{ mb: 4 }}>
            选择论文模板
          </Typography>
          
          <Stack spacing={3}>
            <FormControl fullWidth size="small">
              <InputLabel>学科</InputLabel>
              <Select
                value={discipline}
                label="学科"
                onChange={(e) => setDiscipline(e.target.value)}
              >
                {disciplines.map((item) => (
                  <MenuItem key={item} value={item}>
                    {item}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth size="small">
              <InputLabel>论文类型</InputLabel>
              <Select
                value={paperType}
                label="论文类型"
                onChange={(e) => setPaperType(e.target.value)}
              >
                {paperTypes.map((item) => (
                  <MenuItem key={item} value={item}>
                    {item}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Button
              fullWidth
              variant="contained"
              onClick={handleCreate}
              sx={{
                mt: 2,
                py: 1.5,
                backgroundColor: '#1976d2',
                '&:hover': {
                  backgroundColor: '#1565c0',
                },
              }}
            >
              开始写作
            </Button>
          </Stack>
        </Paper>
      </Box>
    </Container>
  );
};

export default WritingTemplate; 