import React, { useState, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Typography,
  Paper,
} from '@mui/material';
import { apiService } from '../../../services/api';
import { MathComponent } from 'mathjax-react';

// TODO: 待实现功能
// 1. 理论基础分析Agent训练
//    - 使用清洗数据中的理论模型构建、假设提出等部分进行训练
//    - 开发理论基础分析生成模板
//    - 实现理论基础分析内容生成功能
// 2. 模型构建Agent训练
//    - 开发模型构建生成模板
//    - 实现模型框架内容生成功能
// 3. 研究假设Agent训练
//    - 开发研究假设生成模板
//    - 实现研究假设内容生成功能
// 4. 理论推导Agent训练
//    - 开发理论推导生成模板
//    - 实现理论推导内容生成功能
// 5. 公式编辑功能
//    - 实现LaTeX公式编辑器
//    - 支持公式预览和编辑
//    - 支持公式导出

interface TheoreticalAnalysisEditorProps {
  onSave: (data: TheoreticalAnalysisData) => void;
  initialData?: TheoreticalAnalysisData;
  writingId: string;
  sectionId: string;
  onPrev?: () => void;
  onNext?: () => void;
}

export interface TheoreticalAnalysisData {
  theoreticalBasis: string;
  concepts: string;
  modelFramework: string;
  researchHypotheses: string;
  frameworkImage?: string;
}

const TheoreticalAnalysisEditor: React.FC<TheoreticalAnalysisEditorProps> = ({
  onSave,
  initialData,
  writingId,
  sectionId,
  onPrev,
  onNext,
}) => {
  const [data, setData] = useState<TheoreticalAnalysisData>(
    initialData || {
      theoreticalBasis: '',
      concepts: '',
      modelFramework: '',
      researchHypotheses: '',
    }
  );

  const [loading, setLoading] = useState<{[key: string]: boolean}>({
    theoreticalBasis: false,
    model: false,
    hypotheses: false,
    framework: false,
  });
  const [error, setError] = useState<string | null>(null);
  const [currentFormula, setCurrentFormula] = useState('');
  const modelEditorRef = useRef<HTMLTextAreaElement>(null);
  const [selectedFormula, setSelectedFormula] = useState<{
    text: string,
    start: number,
    end: number,
  } | null>(null);
  const [cursorPosition, setCursorPosition] = useState<number | null>(null);
  const [selectionHighlight, setSelectionHighlight] = useState<{
    text: string;
    start: number;
    end: number;
  } | null>(null);

  const handleChange = (field: keyof TheoreticalAnalysisData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setData({ ...data, [field]: event.target.value });
  };

  const handleGenerateTheoretical = async () => {
    setLoading(prev => ({ ...prev, theoreticalBasis: true }));
    setError(null);
    try {
      const response = await apiService.agent.generateTheoretical(writingId, sectionId);
      setData(prev => ({
        ...prev,
        theoreticalBasis: response.theoreticalBasis,
        concepts: response.concepts,
      }));
    } catch (err) {
      setError('生成理论基础分析内容失败');
    } finally {
      setLoading(prev => ({ ...prev, theoreticalBasis: false }));
    }
  };

  const handleGenerateModel = async () => {
    setLoading(prev => ({ ...prev, model: true }));
    setError(null);
    try {
      const response = await apiService.agent.generateModel(writingId, sectionId, {
        theoreticalBasis: data.theoreticalBasis,
        concepts: data.concepts,
      });
      setData(prev => ({
        ...prev,
        modelFramework: response.modelFramework,
      }));
    } catch (err) {
      setError('生成模型失败');
    } finally {
      setLoading(prev => ({ ...prev, model: false }));
    }
  };

  const handleGenerateHypotheses = async () => {
    setLoading(prev => ({ ...prev, hypotheses: true }));
    setError(null);
    try {
      const response = await apiService.agent.generateHypotheses(writingId, sectionId, {
        theoreticalBasis: data.theoreticalBasis,
        modelFramework: data.modelFramework,
      });
      setData(prev => ({
        ...prev,
        researchHypotheses: response.researchHypotheses,
      }));
    } catch (err) {
      setError('生成研究假设失败');
    } finally {
      setLoading(prev => ({ ...prev, hypotheses: false }));
    }
  };

  const handleGenerateFramework = async () => {
    setLoading(prev => ({ ...prev, framework: true }));
    setError(null);
    try {
      const response = await apiService.agent.generateFramework(writingId, sectionId, {
        hypotheses: data.researchHypotheses,
        modelFramework: data.modelFramework,
      });
      setData(prev => ({
        ...prev,
        frameworkImage: response.frameworkImage,
      }));
    } catch (err) {
      setError('生成研究框架图失败');
    } finally {
      setLoading(prev => ({ ...prev, framework: false }));
    }
  };

  const handleModelSelect = () => {
    if (modelEditorRef.current) {
      const start = modelEditorRef.current.selectionStart;
      const end = modelEditorRef.current.selectionEnd;
      
      // 如果是点击而不是选中，清除选中状态
      if (start === end) {
        setSelectedFormula(null);
        setSelectionHighlight(null);
        setCursorPosition(start);
        setCurrentFormula('');
        return;
      }

      // 检查选中的文本是否包含完整的公式
      const selectedText = data.modelFramework.substring(start, end);
      const formulaMatch = selectedText.match(/\$\$(.*?)\$\$|\$(.*?)\$/);
      
      if (formulaMatch) {
        const formula = formulaMatch[0];
        const formulaStart = start + selectedText.indexOf(formula);
        const formulaEnd = formulaStart + formula.length;
        
        setSelectedFormula({
          text: formula,
          start: formulaStart,
          end: formulaEnd,
        });
        setSelectionHighlight({
          text: formula,
          start: formulaStart,
          end: formulaEnd,
        });
        setCurrentFormula(formula.replace(/^\$\$|\$\$$/g, '').replace(/^\$|\$$/g, ''));
        setCursorPosition(null);
      } else {
        setSelectedFormula(null);
        setSelectionHighlight(null);
        setCursorPosition(start);
        setCurrentFormula('');
      }
    }
  };

  const handleFormulaUpdate = () => {
    if (!currentFormula.trim() || !modelEditorRef.current) return;

    // 自动添加公式分隔符
    const formulaWithDelimiters = currentFormula.trim().startsWith('\\[') || 
                                currentFormula.trim().startsWith('\\begin{equation}') ||
                                currentFormula.trim().includes('\\\\') 
      ? `$$${currentFormula.trim()}$$` 
      : `$${currentFormula.trim()}$`;

    const newModelFramework = selectedFormula
      ? data.modelFramework.substring(0, selectedFormula.start) +
        formulaWithDelimiters +
        data.modelFramework.substring(selectedFormula.end)
      : data.modelFramework.substring(0, cursorPosition || modelEditorRef.current.selectionStart) +
        formulaWithDelimiters +
        data.modelFramework.substring(cursorPosition || modelEditorRef.current.selectionStart);

    setData(prev => ({
      ...prev,
      modelFramework: newModelFramework,
    }));
    setCurrentFormula('');
    setSelectedFormula(null);
    setSelectionHighlight(null);
    setCursorPosition(null);
  };

  const renderModelContent = () => {
    if (!data.modelFramework) return null;

    const parts = [];
    let lastIndex = 0;
    let textContent = '';

    // 处理选中的公式高亮
    if (selectionHighlight) {
      parts.push(
        <span key="before">
          {data.modelFramework.substring(0, selectionHighlight.start)}
        </span>
      );
      parts.push(
        <span 
          key="highlight" 
          style={{ 
            backgroundColor: '#e3f2fd',
            padding: '2px 4px',
            margin: '0 2px',
            borderRadius: '2px',
            border: '1px solid #90caf9',
            display: 'inline-flex',
            alignItems: 'center',
            cursor: 'pointer',
          }}
        >
          <MathComponent tex={selectionHighlight.text.replace(/^\$\$|\$\$$/g, '').replace(/^\$|\$$/g, '')} display={selectionHighlight.text.startsWith('$$')} />
        </span>
      );
      parts.push(
        <span key="after">
          {data.modelFramework.substring(selectionHighlight.end)}
        </span>
      );
      textContent = data.modelFramework;
    } else {
      // 处理普通公式显示
      const text = data.modelFramework;
      let currentPosition = 0;
      
      // 使用正则表达式匹配所有公式
      const formulaPattern = /\$\$(.*?)\$\$|\$(.*?)\$/g;
      let match;
      
      while ((match = formulaPattern.exec(text)) !== null) {
        // 添加公式前的文本
        if (match.index > currentPosition) {
          const beforeText = text.substring(currentPosition, match.index);
          parts.push(
            <span key={`text-${currentPosition}`}>
              {beforeText}
            </span>
          );
          textContent += beforeText;
        }

        // 获取公式内容和类型
        const formula = match[0];
        const isDisplayMode = formula.startsWith('$$');
        const formulaContent = formula.replace(/^\$\$|\$\$$/g, '').replace(/^\$|\$$/g, '');
        
        // 添加公式
        parts.push(
          <span 
            key={`formula-${match.index}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              margin: '0 2px',
              padding: '2px 4px',
              backgroundColor: '#f8f9fa',
              borderRadius: '2px',
              border: '1px solid #e9ecef',
              cursor: 'pointer',
            }}
          >
            <MathComponent 
              tex={formulaContent} 
              display={isDisplayMode}
            />
          </span>
        );
        textContent += formula;
        currentPosition = match.index + formula.length;
      }

      // 添加剩余文本
      if (currentPosition < text.length) {
        const remainingText = text.substring(currentPosition);
        parts.push(
          <span key={`text-end-${currentPosition}`}>
            {remainingText}
          </span>
        );
        textContent += remainingText;
      }
    }

    const cursorLeft = cursorPosition !== null 
      ? `${getVisualPosition(textContent, cursorPosition)}ch`
      : '0';

    return (
      <Box sx={{ 
        position: 'relative',
        minHeight: '300px',
        padding: '12px',
        fontFamily: 'inherit',
        fontSize: 'inherit',
        lineHeight: '1.75',
        whiteSpace: 'pre-wrap',
        overflowWrap: 'break-word',
        '& .MathJax': {
          fontSize: '16px !important',
        },
        '& .cursor-indicator': {
          display: cursorPosition !== null ? 'block' : 'none',
          position: 'absolute',
          width: '2px',
          height: '1.2em',
          backgroundColor: '#1976d2',
          animation: 'blink 1s infinite',
          top: cursorPosition !== null 
            ? `${Math.floor(getVisualPosition(textContent, cursorPosition) / 80) * 1.75 + 0.75}em`
            : '0.75em',
        },
        '@keyframes blink': {
          '0%': { opacity: 1 },
          '50%': { opacity: 0 },
          '100%': { opacity: 1 },
        }
      }}>
        {parts}
        <span 
          className="cursor-indicator"
          style={{ 
            left: cursorLeft,
          }}
        />
      </Box>
    );
  };

  // 计算光标的可视位置
  const getVisualPosition = (text: string, position: number): number => {
    if (position === 0) return 0;
    
    const beforeText = text.substring(0, position);
    let visualPosition = 0;
    let currentPosition = 0;
    
    // 使用正则表达式匹配所有公式
    const formulaPattern = /\$\$(.*?)\$\$|\$(.*?)\$/g;
    let match;
    
    while ((match = formulaPattern.exec(beforeText)) !== null) {
      // 添加公式前的普通文本长度
      visualPosition += match.index - currentPosition;
      
      // 计算公式的视觉宽度
      const formula = match[0];
      const formulaContent = formula.replace(/^\$\$|\$\$$/g, '').replace(/^\$|\$$/g, '');
      const isDisplayMode = formula.startsWith('$$');
      
      // 根据公式内容和类型计算视觉宽度
      const visualWidth = Math.max(
        formulaContent.length * 0.8, // 基础宽度
        isDisplayMode ? 4 : 2 // 最小宽度
      );
      
      visualPosition += visualWidth;
      currentPosition = match.index + formula.length;
    }
    
    // 添加剩余文本的长度
    visualPosition += position - currentPosition;
    
    return visualPosition;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {error && (
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* 理论基础分析部分 */}
      <Paper variant="outlined" sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6">理论基础分析</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleGenerateTheoretical}
            disabled={loading.theoreticalBasis}
          >
            {loading.theoreticalBasis ? <CircularProgress size={24} /> : '生成理论基础分析内容'}
          </Button>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="概念界定"
            value={data.concepts}
            onChange={handleChange('concepts')}
            variant="outlined"
            helperText="定义研究中涉及的主要概念"
          />
          <TextField
            fullWidth
            multiline
            rows={6}
            label="理论基础"
            value={data.theoreticalBasis}
            onChange={handleChange('theoreticalBasis')}
            variant="outlined"
            helperText="描述研究的理论基础，包括相关理论和概念的分析"
          />
        </Box>
      </Paper>

      {/* 模型构建与推导部分 */}
      <Paper variant="outlined" sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6">模型构建与推导</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleGenerateModel}
            disabled={loading.model}
          >
            {loading.model ? <CircularProgress size={24} /> : '生成模型'}
          </Button>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <Paper 
              variant="outlined" 
              sx={{ 
                position: 'relative',
                '& .MathJax': {
                  display: 'inline-flex !important',
                  margin: '0 2px',
                  verticalAlign: 'middle',
                },
                '& .MathJax-Display': {
                  margin: '0.5em 0',
                }
              }}
            >
              {renderModelContent()}
              <TextField
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  opacity: 0,
                  cursor: 'text',
                  '& .MuiInputBase-root': {
                    padding: '12px',
                    fontFamily: 'inherit',
                    fontSize: 'inherit',
                    lineHeight: '1.75',
                  }
                }}
                multiline
                fullWidth
                value={data.modelFramework}
                onChange={handleChange('modelFramework')}
                onSelect={handleModelSelect}
                inputRef={modelEditorRef}
              />
            </Paper>
            <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
              点击任意位置插入公式，或选中已有公式进行编辑
            </Typography>
          </Box>
          <Box sx={{ width: '50%', display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                公式预览
              </Typography>
              <Box sx={{ 
                minHeight: '100px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                border: '1px solid #e0e0e0',
                borderRadius: '4px',
                p: 2,
                backgroundColor: '#fafafa'
              }}>
                {currentFormula && (
                  <MathComponent tex={currentFormula} display={true} />
                )}
              </Box>
            </Paper>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="LaTeX 公式"
              value={currentFormula}
              onChange={(e) => setCurrentFormula(e.target.value)}
              variant="outlined"
              helperText="输入 LaTeX 格式的公式"
            />
            <Button
              variant="contained"
              onClick={handleFormulaUpdate}
              disabled={!currentFormula.trim()}
              fullWidth
            >
              {selectedFormula ? '更新公式' : '插入公式'}
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* 研究假设部分 */}
      <Paper variant="outlined" sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6">研究假设</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleGenerateHypotheses}
            disabled={loading.hypotheses}
          >
            {loading.hypotheses ? <CircularProgress size={24} /> : '生成研究假设'}
          </Button>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={6}
            label="研究假设"
            value={data.researchHypotheses}
            onChange={handleChange('researchHypotheses')}
            variant="outlined"
            helperText="基于理论分析和模型推导提出研究假设，说明变量间的关系"
          />
        </Box>
      </Paper>

      {/* 研究框架图部分 */}
      <Paper variant="outlined" sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6">研究框架图</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleGenerateFramework}
            disabled={loading.framework || !data.researchHypotheses || !data.modelFramework}
          >
            {loading.framework ? <CircularProgress size={24} /> : '生成研究框架图'}
          </Button>
        </Box>
        {data.frameworkImage && (
          <Box sx={{ mt: 2 }}>
            <img 
              src={data.frameworkImage} 
              alt="研究框架图"
              style={{ maxWidth: '100%', height: 'auto' }}
            />
          </Box>
        )}
      </Paper>

      {/* 底部按钮 */}
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

export default TheoreticalAnalysisEditor; 