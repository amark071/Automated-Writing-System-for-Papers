import React, { useState } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Paper,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { AgentMessage } from '../../../services/api';

interface AgentDialogProps {
  messages: AgentMessage[];
  onMessageSend: (message: string) => void;
  isLoading: boolean;
}

export const AgentDialog: React.FC<AgentDialogProps> = ({
  messages,
  onMessageSend,
  isLoading,
}) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onMessageSend(input.trim());
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
      bgcolor: 'background.paper',
    }}>
      {/* 标题 */}
      <Box sx={{ 
        p: 2, 
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}>
        <Typography variant="h6">智能助手</Typography>
      </Box>

      {/* 消息列表 */}
      <Box sx={{ 
        flex: 1, 
        overflow: 'auto',
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
      }}>
        {messages.map((message, index) => (
          <Paper
            key={index}
            elevation={0}
            sx={{
              p: 2,
              maxWidth: '80%',
              alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
              bgcolor: message.role === 'user' ? 'primary.light' : 'grey.100',
              color: message.role === 'user' ? 'primary.contrastText' : 'text.primary',
              borderRadius: 2,
            }}
          >
            <Typography variant="body1">{message.content}</Typography>
          </Paper>
        ))}
      </Box>

      {/* 输入框 */}
      <Box sx={{ 
        p: 2, 
        borderTop: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        gap: 1,
      }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="输入消息..."
          disabled={isLoading}
          sx={{ flex: 1 }}
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