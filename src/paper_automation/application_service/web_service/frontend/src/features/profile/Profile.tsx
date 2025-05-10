import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Avatar,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  TextField,
} from '@mui/material';
import {
  Person as PersonIcon,
  Edit as EditIcon,
  School as SchoolIcon,
  Work as WorkIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';

const Profile: React.FC = () => {
  // 模拟的用户数据
  const user = {
    name: '张三',
    avatar: '/images/avatar.jpg',
    title: '博士研究生',
    institution: '北京大学',
    department: '经济学院',
    email: 'zhangsan@example.com',
    phone: '13800138000',
    location: '北京市海淀区',
    bio: '主要从事宏观经济学研究，对货币政策和经济周期有深入研究。',
  };

  // 模拟的统计数据
  const stats = [
    { label: '论文数', value: 5 },
    { label: '引用数', value: 128 },
    { label: '关注者', value: 42 },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Avatar
                src={user.avatar}
                sx={{ width: 120, height: 120, mx: 'auto', mb: 2 }}
              >
                <PersonIcon sx={{ fontSize: 60 }} />
              </Avatar>
              <Typography variant="h5" gutterBottom>
                {user.name}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                {user.title}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user.institution} · {user.department}
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  startIcon={<EditIcon />}
                  fullWidth
                >
                  编辑资料
                </Button>
              </Box>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                统计信息
              </Typography>
              <Grid container spacing={2}>
                {stats.map((stat) => (
                  <Grid item xs={4} key={stat.label}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="primary">
                        {stat.value}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {stat.label}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                个人简介
              </Typography>
              <Typography variant="body1" paragraph>
                {user.bio}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <List>
                <ListItem>
                  <ListItemIcon>
                    <EmailIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="邮箱"
                    secondary={user.email}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <PhoneIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="电话"
                    secondary={user.phone}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <LocationIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="地址"
                    secondary={user.location}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                修改密码
              </Typography>
              <Box component="form" sx={{ mt: 2 }}>
                <TextField
                  fullWidth
                  label="当前密码"
                  type="password"
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="新密码"
                  type="password"
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="确认新密码"
                  type="password"
                  margin="normal"
                />
                <Button
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                >
                  更新密码
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile; 