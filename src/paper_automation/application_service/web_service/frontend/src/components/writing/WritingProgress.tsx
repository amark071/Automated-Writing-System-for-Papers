import React from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepButton,
  Typography,
} from '@mui/material';

export interface Section {
  id: string;
  title: string;
  completed: boolean;
}

interface WritingProgressProps {
  sections: Section[];
  activeSection: string;
  onSectionChange: (sectionId: string) => void;
}

const WritingProgress: React.FC<WritingProgressProps> = ({
  sections,
  activeSection,
  onSectionChange,
}) => {
  return (
    <Box sx={{ width: '100%' }}>
      <Stepper 
        nonLinear 
        activeStep={sections.findIndex(s => s.id === activeSection)}
        sx={{ 
          overflowX: 'auto',
          '& .MuiStepLabel-root': {
            cursor: 'pointer',
          },
        }}
      >
        {sections.map((section) => (
          <Step key={section.id} completed={section.completed}>
            <StepButton onClick={() => onSectionChange(section.id)}>
              <StepLabel>
                <Typography
                  variant="body2"
                  color={section.id === activeSection ? 'primary' : 'inherit'}
                  sx={{ whiteSpace: 'nowrap' }}
                >
                  {section.title}
                </Typography>
              </StepLabel>
            </StepButton>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
};

export default WritingProgress; 