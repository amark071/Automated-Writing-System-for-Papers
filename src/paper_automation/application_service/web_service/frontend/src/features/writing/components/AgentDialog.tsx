import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  Button,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { AgentMessage, IntroductionData } from '../../../services/api';

interface AgentDialogProps {
  messages: AgentMessage[];
  onMessageSend: (message: string) => Promise<void>;
  isLoading?: boolean;
  introductionData?: IntroductionData;
}

const generateIntroductionContent = (data?: IntroductionData) => {
  if (!data) return '';
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

const AgentDialog: React.FC<AgentDialogProps> = ({
  messages,
  onMessageSend,
  isLoading = false,
  introductionData,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() && !isLoading) {
      await onMessageSend(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ 
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      bgcolor: '#fff',
      position: 'sticky',
      top: 0,
    }}>
      <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
        <Typography variant="h6">智能助手</Typography>
      </Box>

      <List
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 1,
          maxHeight: 'calc(100vh - 140px)', // 减去头部和输入框的高度
        }}
      >
        {messages.map((message) => (
          <ListItem
            key={message.id}
            sx={{
              flexDirection: 'column',
              alignItems: message.sender === 'user' ? 'flex-end' : 'flex-start',
              p: 0,
            }}
          >
            <Paper
              elevation={1}
              sx={{
                p: 1.5,
                bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                maxWidth: '80%',
                borderRadius: 2,
              }}
            >
              <ListItemText
                primary={message.content}
                secondary={new Date(message.timestamp).toLocaleTimeString()}
                sx={{
                  m: 0,
                  '& .MuiListItemText-primary': {
                    color: message.sender === 'user' ? 'white' : 'inherit',
                  },
                  '& .MuiListItemText-secondary': {
                    color: message.sender === 'user' ? 'rgba(255,255,255,0.7)' : 'inherit',
                    fontSize: '0.75rem',
                  },
                }}
              />
            </Paper>
          </ListItem>
        ))}
        <div ref={messagesEndRef} />
      </List>

      <Box sx={{ 
        p: 2, 
        display: 'flex', 
        gap: 1, 
        bgcolor: 'background.paper',
        borderTop: '1px solid #e0e0e0',
        position: 'sticky',
        bottom: 0,
      }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="输入消息..."
          size="small"
          disabled={isLoading}
        />
        <IconButton
          color="primary"
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? <CircularProgress size={24} /> : <SendIcon />}
        </IconButton>
      </Box>
    </Box>
  );
};

export type { AgentDialogProps };
export { generateIntroductionContent };
export { AgentDialog };
export default AgentDialog; 