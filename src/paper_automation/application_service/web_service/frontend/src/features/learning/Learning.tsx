import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  School,
  MenuBook,
  Assignment,
  PlayCircle,
  CheckCircle,
  ArrowForward,
} from '@mui/icons-material';

const Learning: React.FC = () => {
  const courses = [
    {
      title: '论文写作基础',
      description: '掌握学术论文写作的基本要求和规范',
      image: '/images/course1.jpg',
      lessons: 12,
      duration: '6小时',
      progress: 0,
    },
    {
      title: '研究方法论',
      description: '学习科学研究方法和研究设计',
      image: '/images/course2.jpg',
      lessons: 8,
      duration: '4小时',
      progress: 30,
    },
    {
      title: '数据分析与实证研究',
      description: '掌握数据分析和实证研究的方法',
      image: '/images/course3.jpg',
      lessons: 15,
      duration: '7.5小时',
      progress: 0,
    },
  ];

  const resources = [
    {
      title: '论文写作模板',
      description: '各类型论文的标准模板',
      icon: <MenuBook />,
    },
    {
      title: '写作指南',
      description: '详细的论文写作指南和技巧',
      icon: <Assignment />,
    },
    {
      title: '视频教程',
      description: '专业的视频教学资源',
      icon: <PlayCircle />,
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          <School sx={{ mr: 1, verticalAlign: 'bottom' }} />
          学习中心
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          提供全面的论文写作学习资源和指导
        </Typography>
      </Box>

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        推荐课程
      </Typography>
      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item xs={12} md={4} key={course.title}>
            <Card>
              <CardMedia
                component="div"
                sx={{
                  height: 140,
                  backgroundColor: 'grey.300',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <School sx={{ fontSize: 40, color: 'grey.500' }} />
              </CardMedia>
              <CardContent>
                <Typography gutterBottom variant="h6">
                  {course.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {course.description}
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    {course.lessons} 课时 · {course.duration}
                  </Typography>
                  <Typography variant="body2" color="primary">
                    完成度：{course.progress}%
                  </Typography>
                </Box>
                <Button
                  variant="contained"
                  endIcon={<ArrowForward />}
                  fullWidth
                >
                  {course.progress > 0 ? '继续学习' : '开始学习'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        学习资源
      </Typography>
      <Grid container spacing={3}>
        {resources.map((resource) => (
          <Grid item xs={12} md={4} key={resource.title}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {React.cloneElement(resource.icon as React.ReactElement, {
                    sx: { fontSize: 40, color: 'primary.main', mr: 2 }
                  })}
                  <Typography variant="h6">
                    {resource.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {resource.description}
                </Typography>
                <Button
                  variant="outlined"
                  endIcon={<ArrowForward />}
                  fullWidth
                >
                  查看详情
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card sx={{ mt: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            学习路径
          </Typography>
          <List>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="success" />
              </ListItemIcon>
              <ListItemText
                primary="第一步：论文写作基础"
                secondary="了解论文的基本结构和写作规范"
              />
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="disabled" />
              </ListItemIcon>
              <ListItemText
                primary="第二步：研究方法学习"
                secondary="掌握科学的研究方法和研究设计"
              />
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="disabled" />
              </ListItemIcon>
              <ListItemText
                primary="第三步：实践与提高"
                secondary="通过实践练习提升论文写作能力"
              />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Learning; 