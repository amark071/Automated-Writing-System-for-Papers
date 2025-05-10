import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Paper,
} from '@mui/material';
import {
  Description as DescriptionIcon,
  Search as SearchIcon,
  Timeline as TimelineIcon,
  School as SchoolIcon,
} from '@mui/icons-material';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: '智能写作',
      description: '基于AI的论文写作助手，帮助您快速完成论文写作',
      icon: <DescriptionIcon sx={{ fontSize: 40 }} />,
      path: '/writing',
    },
    {
      title: '文献分析',
      description: '智能分析文献，提取关键信息，生成文献综述',
      icon: <SearchIcon sx={{ fontSize: 40 }} />,
      path: '/literature',
    },
    {
      title: '数据分析',
      description: '强大的数据分析工具，支持多种统计方法',
      icon: <TimelineIcon sx={{ fontSize: 40 }} />,
      path: '/analysis',
    },
    {
      title: '学术指导',
      description: '专业的学术指导服务，提供论文修改建议',
      icon: <SchoolIcon sx={{ fontSize: 40 }} />,
      path: '/guidance',
    },
  ];

  return (
    <Box>
      <Paper
        sx={{
          position: 'relative',
          backgroundColor: 'white',
          color: 'text.primary',
          mb: 4,
          backgroundSize: 'cover',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
        }}
      >
        <Box
          sx={{
            position: 'relative',
            p: { xs: 3, md: 6 },
            pr: { md: 0 },
          }}
        >
          <Typography component="h1" variant="h3" color="primary" gutterBottom>
            燎原智能写作系统
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            让AI助力您的学术研究，提升论文写作效率
          </Typography>
          <Button variant="contained" size="large" onClick={() => navigate('/writing')}>
            开始写作
          </Button>
        </Box>
      </Paper>

      <Container maxWidth="lg">
        <Grid container spacing={4}>
          {features.map((feature) => (
            <Grid item key={feature.title} xs={12} sm={6} md={3}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography gutterBottom variant="h5" component="h2">
                    {feature.title}
                  </Typography>
                  <Typography>
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(feature.path)}>
                    了解更多
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Home; 