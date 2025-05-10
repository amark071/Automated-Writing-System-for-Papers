import React, { Component, ErrorInfo } from 'react';
import { Box, Typography, Button, Alert } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      error,
      errorInfo,
    });
    // 这里可以添加错误日志上报逻辑
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <ErrorOutlineIcon color="error" sx={{ fontSize: 48 }} />
          <Typography variant="h5" color="error">
            出错了
          </Typography>
          <Alert severity="error" sx={{ width: '100%' }}>
            {this.state.error?.message || '发生未知错误'}
          </Alert>
          {this.state.errorInfo && (
            <Box
              sx={{
                p: 2,
                bgcolor: 'grey.100',
                borderRadius: 1,
                width: '100%',
                overflow: 'auto',
              }}
            >
              <Typography variant="body2" component="pre">
                {this.state.errorInfo.componentStack}
              </Typography>
            </Box>
          )}
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleReset}
          >
            重试
          </Button>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 