import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Container,
  Paper,
  TextField,
  Typography,
  CircularProgress,
  Button,
} from '@mui/material';
import WritingProgress, { Section } from '../../../components/writing/WritingProgress';
import { AgentDialog } from '../components/AgentDialog';
import IntroductionEditor, { IntroductionData } from '../components/IntroductionEditor';
import LiteratureReviewEditor, { LiteratureReviewData } from '../components/LiteratureReviewEditor';
import TheoreticalAnalysisEditor, { TheoreticalAnalysisData } from '../components/TheoreticalAnalysisEditor';
import DataAnalysisEditor, { DataAnalysisData } from '../components/DataAnalysisEditor';
import { EmpiricalResults } from '../components/EmpiricalResults';
import { useApi } from '../../../hooks/useApi';
import {
  writingApi,
  agentApi,
  empiricalApi,
  AgentMessage,
  SectionData,
  SectionRequest,
  UpdateSectionRequest,
  SendMessageRequest,
  SendMessageResponse,
  SectionMessagesRequest,
  SectionMessagesResponse,
  EmpiricalAnalysisResult
} from '../../../services/api';
import message from 'antd/lib/message';
import PreviewAndExport from '../components/PreviewAndExport';
import SectionEditor from '../components/SectionEditor';
import DiscussionEditor from '../components/DiscussionEditor';
import ConclusionEditor from '../components/ConclusionEditor';

const defaultSections: Section[] = [
  { id: '1', title: '引言', completed: false },
  { id: '2', title: '文献综述', completed: false },
  { id: '3', title: '理论分析', completed: false },
  { id: '4', title: '数据分析', completed: false },
  { id: '5', title: '实证分析', completed: false },
  { id: '6', title: '讨论', completed: false },
  { id: '7', title: '结论', completed: false },
];

export const WritingEditor: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeSection, setActiveSection] = useState('1');
  const [sections, setSections] = useState<Section[]>(defaultSections);
  const [content, setContent] = useState('');
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [discipline, setDiscipline] = useState<string>('');
  const [paperType, setPaperType] = useState<string>('');
  const [introductionData, setIntroductionData] = useState<IntroductionData | undefined>();
  const [empiricalResults, setEmpiricalResults] = useState<EmpiricalAnalysisResult | null>(null);
  const [empiricalLoading, setEmpiricalLoading] = useState(false);

  const { data: sectionData, isLoading: writingLoading, error: writingError, execute: fetchWriting } = useApi<SectionData, SectionRequest>(writingApi.getSection);
  const { execute: updateWriting } = useApi<SectionData, UpdateSectionRequest>(writingApi.updateSection);
  const { execute: sendMessage } = useApi<SendMessageResponse, SendMessageRequest>(agentApi.sendMessage);
  const { execute: fetchMessages } = useApi<SectionMessagesResponse, SectionMessagesRequest>(agentApi.getMessages);

  useEffect(() => {
    if (id === 'new') {
      const selectedDiscipline = localStorage.getItem('selectedDiscipline') || '经济学';
      const selectedPaperType = localStorage.getItem('selectedPaperType') || '期刊论文';
      setDiscipline(selectedDiscipline);
      setPaperType(selectedPaperType);
    }
  }, [id]);

  useEffect(() => {
    if (id && activeSection && id !== 'new') {
      loadSection();
      loadMessages();
    }
  }, [id, activeSection]);

  const loadSection = async () => {
    if (!id || !activeSection || id === 'new') return;
    const result = await fetchWriting({
      writingId: id,
      sectionId: activeSection,
    });
    if (result) {
      if (activeSection === '1' && result.content) {
        try {
          const parsedData = JSON.parse(result.content);
          setIntroductionData(parsedData);
        } catch (e) {
          console.error('解析引言数据失败:', e);
          setIntroductionData(undefined);
        }
      } else {
        setContent(result.content || '');
      }
      setSections(prev => prev.map(section => ({
        ...section,
        completed: section.id === activeSection ? result.completed : section.completed
      })));
    }
  };

  const loadMessages = async () => {
    if (!id || !activeSection || id === 'new') return;
    const result = await fetchMessages({
      writingId: id,
      sectionId: activeSection,
    });
    if (result && result.messages) {
      setMessages(result.messages);
    }
  };

  const handleSectionChange = async (sectionId: string) => {
    if (id && activeSection && content) {
      await updateWriting({
        writingId: id,
        sectionId: activeSection,
        content,
      });
    }
    setActiveSection(sectionId);
  };

  const handleContentChange = (newContent: string) => {
    setContent(newContent);
  };

  const handleMessageSend = async (message: string) => {
    if (!id || !activeSection) return;
    await sendMessage({
      writingId: id,
      sectionId: activeSection,
      content: message,
    });
    await loadMessages();
  };

  const handleSave = async () => {
    if (!id || !activeSection) return;
    try {
      const contentToSave = activeSection === '1' 
        ? JSON.stringify(introductionData)
        : content;
      await updateWriting({
        writingId: id,
        sectionId: activeSection,
        content: contentToSave,
      });
      message.success('保存成功');
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    }
  };

  const handleNext = () => {
    const currentIndex = sections.findIndex(s => s.id === activeSection);
    if (currentIndex < sections.length - 1) {
      handleSectionChange(sections[currentIndex + 1].id);
    }
  };

  const handlePrev = () => {
    const currentIndex = sections.findIndex(s => s.id === activeSection);
    if (currentIndex > 0) {
      handleSectionChange(sections[currentIndex - 1].id);
    }
  };

  const fetchEmpiricalResults = async () => {
    if (!id || !activeSection) return;
    
    try {
      setEmpiricalLoading(true);
      const response = await empiricalApi.getResults({
        writingId: id,
        sectionId: activeSection
      });
      
      if (response.data) {
        setEmpiricalResults(response.data);
        setSections(prev => prev.map(section => ({
          ...section,
          completed: section.id === activeSection ? true : section.completed
        })));
      }
    } catch (error) {
      console.error('获取实证分析结果失败:', error);
      message.error('获取实证分析结果失败');
    } finally {
      setEmpiricalLoading(false);
    }
  };

  useEffect(() => {
    if (activeSection === '5') {
      fetchEmpiricalResults();
    }
  }, [activeSection]);

  const renderEditor = () => {
    if (activeSection === '1') {
      return (
        <IntroductionEditor
          onSave={handleSave}
          initialData={introductionData}
          writingId={id || ''}
          sectionId={activeSection}
          onNext={handleNext}
        />
      );
    }

    if (activeSection === '2') {
      let literatureReviewData: LiteratureReviewData | undefined;
      if (content) {
        try {
          literatureReviewData = JSON.parse(content);
        } catch (e) {
          console.error('解析文献综述数据失败:', e);
        }
      }
      
      return (
        <LiteratureReviewEditor
          onSave={async (data) => {
            setContent(JSON.stringify(data));
            await handleSave();
          }}
          initialData={literatureReviewData}
          title={sections[1].title}
          writingId={id || ''}
          sectionId={activeSection}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      );
    }

    if (activeSection === '3') {
      let theoreticalAnalysisData: TheoreticalAnalysisData | undefined;
      if (content) {
        try {
          theoreticalAnalysisData = JSON.parse(content);
        } catch (e) {
          console.error('解析理论分析数据失败:', e);
        }
      }
      
      return (
        <TheoreticalAnalysisEditor
          onSave={async (data) => {
            setContent(JSON.stringify(data));
            await handleSave();
          }}
          initialData={theoreticalAnalysisData}
          writingId={id || ''}
          sectionId={activeSection}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      );
    }

    if (activeSection === '4') {
      let dataAnalysisData: DataAnalysisData | undefined;
      if (content) {
        try {
          dataAnalysisData = JSON.parse(content);
        } catch (e) {
          console.error('解析数据分析数据失败:', e);
        }
      }
      
      return (
        <DataAnalysisEditor
          onSave={async (data) => {
            setContent(JSON.stringify(data));
            await handleSave();
          }}
          initialData={dataAnalysisData}
          writingId={id || ''}
          sectionId={activeSection}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      );
    }

    if (activeSection === '5') {
      if (empiricalLoading) {
        return (
          <Box display="flex" flexDirection="column" alignItems="center" gap={2} py={4}>
            <CircularProgress />
            <Typography>正在获取实证分析结果...</Typography>
          </Box>
        );
      }

      if (!empiricalResults) {
        return (
          <Box display="flex" flexDirection="column" alignItems="center" gap={2} py={4}>
            <Typography variant="h6" color="error">
              未找到实证分析结果
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={fetchEmpiricalResults}
            >
              重新获取
            </Button>
          </Box>
        );
      }

      return (
        <EmpiricalResults
          sectionId={activeSection}
          regressionResults={empiricalResults.regressionResults}
          heterogeneityResults={empiricalResults.heterogeneityResults}
          diagnosticTests={empiricalResults.diagnosticTests}
          robustnessTests={empiricalResults.robustnessTests}
          timeSeriesResults={empiricalResults.timeSeriesResults}
          mediationResults={empiricalResults.mediationResults}
          moderationResults={empiricalResults.moderationResults}
          endogeneityResults={empiricalResults.endogeneityResults}
          panelDataResults={empiricalResults.panelDataResults}
          selectedMethods={empiricalResults.selectedMethods}
          onSave={handleSave}
          onPrev={handlePrev}
          onNext={handleNext}
          onEditText={async (section, text) => {
            try {
              await empiricalApi.updateAnalysis({
                writingId: id || '',
                sectionId: activeSection,
                section,
                content: text
              });
              message.success('保存成功');
            } catch (error) {
              console.error('保存失败:', error);
              message.error('保存失败');
            }
          }}
          onRunRobustnessTest={async (testName) => {
            try {
              const response = await empiricalApi.runRobustnessTest({
                writingId: id || '',
                sectionId: activeSection,
                testName
              });
              if (response.data.success) {
                message.success('稳健性检验执行成功');
                fetchEmpiricalResults();
              } else {
                message.error(response.data.message || '稳健性检验执行失败');
              }
            } catch (error) {
              console.error('稳健性检验执行失败:', error);
              message.error('稳健性检验执行失败');
            }
          }}
        />
      );
    }

    if (activeSection === '6') {
      return (
        <DiscussionEditor
          writingId={id || ''}
          sectionId={activeSection}
          onSave={handleSave}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      );
    }

    if (activeSection === '7') {
      return (
        <ConclusionEditor
          writingId={id || ''}
          sectionId={activeSection}
          onSave={handleSave}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      );
    }

    const currentSection = sections.find(s => s.id === activeSection);
    if (!currentSection) return null;

    const currentIndex = sections.findIndex(s => s.id === activeSection);
    const isLastSection = currentIndex === sections.length - 1;

    return (
      <SectionEditor
        title={currentSection.title}
        content={content}
        onContentChange={handleContentChange}
        onSave={handleSave}
        writingId={id || ''}
        sectionId={activeSection}
        onPrev={handlePrev}
        onNext={!isLastSection ? handleNext : undefined}
        isLastSection={isLastSection}
      />
    );
  };

  if (writingLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (writingError) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography color="error">加载失败，请重试</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ 
          position: 'sticky',
          top: 0,
          bgcolor: 'background.paper',
          zIndex: 1,
          borderBottom: '1px solid #e0e0e0',
          p: 2,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start'
        }}>
          <WritingProgress
            sections={sections}
            activeSection={activeSection}
            onSectionChange={handleSectionChange}
          />
          <Box sx={{ 
            display: 'flex', 
            flexDirection: 'column',
            gap: 1,
            ml: 2
          }}>
            <PreviewAndExport
              sectionId={id || ''}
              content={content}
              type="writing"
              introductionData={activeSection === '1' ? introductionData : undefined}
            />
          </Box>
        </Box>
        <Box sx={{ flex: 1, overflow: 'auto', p: 4, pt: 2 }}>
          {renderEditor()}
        </Box>
      </Box>
      <Box sx={{ 
        width: 400, 
        borderLeft: '1px solid #e0e0e0',
        height: '100vh',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <AgentDialog
          messages={messages}
          onMessageSend={handleMessageSend}
          isLoading={false}
        />
      </Box>
    </Box>
  );
};

export default WritingEditor; 