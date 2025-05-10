import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
  Chip,
} from '@mui/material';
import {
  Forum as ForumIcon,
  Person as PersonIcon,
  ThumbUp as ThumbUpIcon,
  Comment as CommentIcon,
} from '@mui/icons-material';

const Community: React.FC = () => {
  // 模拟的帖子数据
  const posts = [
    {
      id: 1,
      title: '如何写好论文的引言部分？',
      author: '张三',
      content: '最近在写论文，对引言部分的结构和内容有些困惑...',
      likes: 24,
      comments: 8,
      tags: ['论文写作', '引言'],
      time: '2024-03-20 14:30',
    },
    {
      id: 2,
      title: '实证分析中的内生性问题处理',
      author: '李四',
      content: '在使用工具变量法处理内生性问题时，需要注意哪些问题？',
      likes: 18,
      comments: 12,
      tags: ['实证分析', '内生性'],
      time: '2024-03-19 16:45',
    },
  ];

  // 模拟的热门话题
  const hotTopics = [
    { name: '论文写作', count: 156 },
    { name: '研究方法', count: 98 },
    { name: '数据分析', count: 87 },
    { name: '学术规范', count: 76 },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          <ForumIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
          学术社区
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          与其他研究者交流讨论，分享经验和见解
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              placeholder="搜索帖子..."
              variant="outlined"
              sx={{ mb: 2 }}
            />
            <Box sx={{ display: 'flex', gap: 1 }}>
              {hotTopics.map((topic) => (
                <Chip
                  key={topic.name}
                  label={`${topic.name} (${topic.count})`}
                  onClick={() => {}}
                />
              ))}
            </Box>
          </Box>

          {posts.map((post) => (
            <Card key={post.id} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {post.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {post.content}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  {post.tags.map((tag) => (
                    <Chip
                      key={tag}
                      label={tag}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <PersonIcon sx={{ mr: 0.5, fontSize: 16 }} />
                    <Typography variant="body2">{post.author}</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {post.time}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<ThumbUpIcon />}
                >
                  {post.likes}
                </Button>
                <Button
                  size="small"
                  startIcon={<CommentIcon />}
                >
                  {post.comments}
                </Button>
              </CardActions>
            </Card>
          ))}
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                热门话题
              </Typography>
              <List>
                {hotTopics.map((topic) => (
                  <ListItem key={topic.name}>
                    <ListItemText
                      primary={topic.name}
                      secondary={`${topic.count} 个帖子`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                活跃用户
              </Typography>
              <List>
                {[1, 2, 3].map((i) => (
                  <ListItem key={i}>
                    <ListItemAvatar>
                      <Avatar>
                        <PersonIcon />
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={`用户${i}`}
                      secondary={`${Math.floor(Math.random() * 100)} 个帖子`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Community; 