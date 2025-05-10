import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  Chip,
  Stack,
  CircularProgress,
  Alert,
} from '@mui/material';
import { TrendingUp, LocalLibrary, Science, Search as SearchIcon } from '@mui/icons-material';

interface Topic {
  id: string;
  title: string;
  keywords: string[];
  citations: number;
  trend: 'up' | 'down' | 'stable';
}

export const Topic: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 模拟热门研究主题数据
  const mockTopics: Topic[] = [
    {
      id: '1',
      title: '人工智能在医疗诊断中的应用',
      keywords: ['AI', '医疗诊断', '深度学习'],
      citations: 1200,
      trend: 'up',
    },
    {
      id: '2',
      title: '区块链技术在供应链管理中的创新',
      keywords: ['区块链', '供应链', '创新'],
      citations: 800,
      trend: 'up',
    },
    {
      id: '3',
      title: '可持续发展与环境保护研究',
      keywords: ['可持续发展', '环境保护', '绿色技术'],
      citations: 1500,
      trend: 'stable',
    },
  ];

  useEffect(() => {
    const fetchTopics = async () => {
      setLoading(true);
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000));
        setTopics(mockTopics);
      } catch (err) {
        setError('获取研究主题失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, []);

  const filteredTopics = topics.filter(topic =>
    topic.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    topic.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        研究选题推荐
      </Typography>

      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="搜索研究主题或关键词"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredTopics.map((topic) => (
            <Grid item key={topic.id} xs={12} md={6} lg={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {topic.title}
                  </Typography>
                  <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                    {topic.keywords.map((keyword) => (
                      <Chip
                        key={keyword}
                        label={keyword}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    ))}
                  </Stack>
                  <Typography variant="body2" color="text.secondary">
                    引用次数: {topic.citations}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    趋势: {
                      topic.trend === 'up' ? '上升' :
                      topic.trend === 'down' ? '下降' : '稳定'
                    }
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" color="primary">
                    查看详情
                  </Button>
                  <Button size="small" color="primary">
                    开始研究
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Grid container spacing={3} sx={{ mt: 4 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
                热门研究方向
              </Typography>
              <Grid container spacing={3}>
                {mockTopics.map((topic) => (
                  <Grid item xs={12} md={4} key={topic.title}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {topic.title}
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                          {topic.keywords.map((keyword) => (
                            <Chip
                              key={keyword}
                              label={keyword}
                              size="small"
                              sx={{ mr: 0.5, mb: 0.5 }}
                            />
                          ))}
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          引用量：{topic.citations}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          趋势：{
                            topic.trend === 'up' ? '上升' :
                            topic.trend === 'down' ? '下降' : '稳定'
                          }
                        </Typography>
                        <Button
                          variant="outlined"
                          size="small"
                          sx={{ mt: 1 }}
                          fullWidth
                        >
                          查看详情
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <LocalLibrary sx={{ mr: 1, verticalAlign: 'middle' }} />
                文献分析
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                基于海量文献数据的智能分析，帮助您了解研究热点和趋势。
              </Typography>
              <Button variant="contained">开始分析</Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Science sx={{ mr: 1, verticalAlign: 'middle' }} />
                选题指导
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                智能助手将根据您的研究兴趣和背景，为您推荐合适的研究方向。
              </Typography>
              <Button variant="contained">获取指导</Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Topic; 