import React from 'react';
import {
  Box,
  IconButton,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  FormatBold,
  FormatItalic,
  FormatUnderlined,
  FormatListBulleted,
  FormatListNumbered,
  FormatQuote,
  TableChart,
  Image,
  Functions,
} from '@mui/icons-material';

interface EditorToolbarProps {
  onFormat: (format: string) => void;
  onInsert: (type: string) => void;
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
}

const EditorToolbar: React.FC<EditorToolbarProps> = ({
  onFormat,
  onInsert,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        p: 1,
        borderBottom: 1,
        borderColor: 'divider',
        bgcolor: 'background.paper',
      }}
    >
      {/* 撤销/重做 */}
      <Tooltip title="撤销">
        <span>
          <IconButton
            size="small"
            onClick={onUndo}
            disabled={!canUndo}
          >
            <FormatBold />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="重做">
        <span>
          <IconButton
            size="small"
            onClick={onRedo}
            disabled={!canRedo}
          >
            <FormatBold />
          </IconButton>
        </span>
      </Tooltip>

      <Divider orientation="vertical" flexItem />

      {/* 文本格式 */}
      <Tooltip title="加粗">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('bold')}
          >
            <FormatBold />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="斜体">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('italic')}
          >
            <FormatItalic />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="下划线">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('underline')}
          >
            <FormatUnderlined />
          </IconButton>
        </span>
      </Tooltip>

      <Divider orientation="vertical" flexItem />

      {/* 列表格式 */}
      <Tooltip title="无序列表">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('bulletList')}
          >
            <FormatListBulleted />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="有序列表">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('orderedList')}
          >
            <FormatListNumbered />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="引用">
        <span>
          <IconButton
            size="small"
            onClick={() => onFormat('blockquote')}
          >
            <FormatQuote />
          </IconButton>
        </span>
      </Tooltip>

      <Divider orientation="vertical" flexItem />

      {/* 插入功能 */}
      <Tooltip title="插入表格">
        <span>
          <IconButton
            size="small"
            onClick={() => onInsert('table')}
          >
            <TableChart />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="插入图片">
        <span>
          <IconButton
            size="small"
            onClick={() => onInsert('image')}
          >
            <Image />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="插入公式">
        <span>
          <IconButton
            size="small"
            onClick={() => onInsert('formula')}
          >
            <Functions />
          </IconButton>
        </span>
      </Tooltip>
    </Box>
  );
};

export default EditorToolbar; 