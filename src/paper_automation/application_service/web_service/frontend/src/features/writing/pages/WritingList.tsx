import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const WritingList: React.FC = () => {
  const navigate = useNavigate();

  const handleCreate = () => {
    navigate('/writing/new');
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">我的作品</Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={handleCreate}
          >
            新建作品
          </Button>
        </Box>

        <Paper elevation={3}>
          <List>
            <ListItem>
              <ListItemText 
                primary="功能开发中..." 
                secondary="目前仅支持新建作品功能，其他功能正在开发中"
              />
            </ListItem>
          </List>
        </Paper>
      </Box>
    </Container>
  );
};

export default WritingList; 