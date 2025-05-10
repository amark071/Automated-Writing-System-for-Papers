export const WRITING_STEPS = [
  { id: 1, label: '引言' },
  { id: 2, label: '文献综述' },
  { id: 3, label: '理论分析' },
  { id: 4, label: '数据分析' },
  { id: 5, label: '实证分析' },
  { id: 6, label: '讨论' },
  { id: 7, label: '结论' },
] as const;

export type WritingStep = typeof WRITING_STEPS[number];
export type WritingStepId = WritingStep['id']; 