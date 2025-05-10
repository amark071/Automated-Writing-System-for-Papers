import axios, { AxiosError, AxiosResponse } from 'axios';
import { message } from 'antd';

const API_BASE_URL = 'http://localhost:8000';

export const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// 请求拦截器
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          message.error('登录已过期，请重新登录');
          break;
        case 403:
          message.error('没有权限访问该资源');
          break;
        case 404:
          message.error('请求的资源不存在');
          break;
        case 500:
          message.error('服务器错误，请稍后重试');
          break;
        default:
          message.error('发生错误，请稍后重试');
      }
    } else if (error.request) {
      message.error('网络错误，请检查网络连接');
    } else {
      message.error('请求配置错误');
    }
    return Promise.reject(error);
  }
);

// 重试机制
const retryRequest = async (fn: () => Promise<any>, retries = 3, delay = 1000) => {
  try {
    return await fn();
  } catch (error) {
    if (retries === 0) {
      throw error;
    }
    await new Promise(resolve => setTimeout(resolve, delay));
    return retryRequest(fn, retries - 1, delay * 2);
  }
};

export interface Writing {
  id: string;
  title: string;
  content: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CreateWritingRequest {
  title?: string;
  content?: string;
  discipline: string;
  paperType: string;
}

export interface AgentMessage {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: string;
}

export interface SectionData {
  content: string;
  completed: boolean;
}

export interface SectionRequest {
  writingId: string;
  sectionId: string;
}

export interface UpdateSectionRequest extends SectionRequest {
  content: string;
}

export interface SendMessageRequest extends SectionRequest {
  content: string;
}

export interface PreviewResponse {
  success: boolean;
  data?: {
    html: string;
  };
}

export interface ExportResponse {
  success: boolean;
  data?: {
    fileUrl: string;
  };
}

export interface IntroductionData {
  title: string;
  subtitle?: string;
  point: string;
  socialBackground: string;
  policyBackground: string;
  theoreticalBackground: string;
  researchConclusion: string;
  marginalContribution: string;
}

export interface GenerateFrameworkRequest {
  hypotheses: string;
  modelFramework: string;
}

export interface GenerateFrameworkResponse {
  frameworkImage: string; // Base64 encoded image
}

export interface GenerateTheoreticalResponse {
  theoreticalBasis: string;
  concepts: string;
}

export interface GenerateModelRequest {
  theoreticalBasis: string;
  concepts: string;
}

export interface GenerateModelResponse {
  modelFramework: string;
}

export interface GenerateHypothesesRequest {
  theoreticalBasis: string;
  modelFramework: string;
}

export interface GenerateHypothesesResponse {
  researchHypotheses: string;
}

export interface SendMessageResponse {
  id: string;
  content: string;
  sender: string;
  timestamp: string;
}

export interface SectionMessagesRequest {
  writingId: string;
  sectionId: string;
}

export interface SectionMessagesResponse {
  messages: AgentMessage[];
}

export const writingApi = {
  getAll: async () => {
    const response = await axiosInstance.get<Writing[]>('/api/writings');
    return response.data;
  },
  get: async (id: string) => {
    const response = await axiosInstance.get<Writing>(`/api/writings/${id}`);
    return response.data;
  },
  create: async (data: CreateWritingRequest) => {
    const response = await axiosInstance.post<Writing>('/api/writings', data);
    return response.data;
  },
  update: async (id: string, data: Partial<Writing>) => {
    const response = await axiosInstance.put<Writing>(`/api/writings/${id}`, data);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await axiosInstance.delete(`/api/writings/${id}`);
    return response.data;
  },
  getSection: async (params: SectionRequest) => {
    const response = await axiosInstance.get<SectionData>(`/api/writings/${params.writingId}/sections/${params.sectionId}`);
    return response.data;
  },
  updateSection: async (params: UpdateSectionRequest) => {
    const response = await axiosInstance.put<SectionData>(`/api/writings/${params.writingId}/sections/${params.sectionId}`, { content: params.content });
    return response.data;
  },
  getPreview: async (sectionId: string): Promise<string> => {
    const response = await axiosInstance.get<string>(`/api/writings/preview/${sectionId}`);
    return response.data;
  },
  exportToWord: async (sectionId: string): Promise<Blob> => {
    const response = await axiosInstance.get(`/api/writings/export/${sectionId}`, {
      responseType: 'blob'
    });
    return response.data;
  },
};

export const agentApi = {
  chat: (writingId: string, message: string): Promise<any> =>
    axiosInstance.post(`/api/agent/chat/${writingId}`, { message }),

  generate: (writingId: string, section: string): Promise<any> =>
    axiosInstance.post(`/api/agent/generate/${writingId}/${section}`),

  generateTheoretical: (writingId: string, sectionId: string): Promise<GenerateTheoreticalResponse> =>
    axiosInstance.post(`/api/agent/theoretical/${writingId}/${sectionId}/generate`),

  generateModel: (writingId: string, sectionId: string, data: GenerateModelRequest): Promise<GenerateModelResponse> =>
    axiosInstance.post(`/api/agent/model/${writingId}/${sectionId}/generate`, data),

  generateHypotheses: (writingId: string, sectionId: string, data: GenerateHypothesesRequest): Promise<GenerateHypothesesResponse> =>
    axiosInstance.post(`/api/agent/hypotheses/${writingId}/${sectionId}/generate`, data),

  generateFramework: (writingId: string, sectionId: string, data: GenerateFrameworkRequest): Promise<GenerateFrameworkResponse> =>
    axiosInstance.post(`/api/agent/framework/${writingId}/${sectionId}/generate`, data),

  sendMessage: (params: SendMessageRequest): Promise<SendMessageResponse> =>
    axiosInstance.post('/api/agent/message', params),

  getMessages: (params: SectionMessagesRequest): Promise<SectionMessagesResponse> =>
    axiosInstance.get(`/api/agent/messages/${params.writingId}/${params.sectionId}`),
};

export const previewAnalysis = async (params: { sectionId: string; content: string }): Promise<PreviewResponse> => {
  const response = await axiosInstance.post<PreviewResponse>(`/api/analysis/preview`, params);
  return response.data;
};

export const exportAnalysis = async (params: { sectionId: string; content: string; format: 'docx' | 'pdf' }): Promise<ExportResponse> => {
  const response = await axiosInstance.post<ExportResponse>(`/api/analysis/export`, params);
  return response.data;
};

export const methodApi = {
  analyzeData: (params: { writingId: string; data: any[]; dataType: string }) =>
    axiosInstance.post('/api/method/analyze', params),
  
  sendMessage: (params: SendMessageRequest): Promise<SendMessageResponse> =>
    axiosInstance.post('/api/method/message', params),
  
  getMessages: (params: SectionMessagesRequest): Promise<SectionMessagesResponse> =>
    axiosInstance.get(`/api/method/messages/${params.writingId}/${params.sectionId}`),
};

export const apiService = {
  writing: writingApi,
  agent: agentApi,
  method: methodApi,
};

// 实证分析结果类型定义
export interface EmpiricalAnalysisResult {
  regressionResults: Array<{
    variable: string;
    coefficient: number;
    standardError: number;
    tStat: number;
    pValue: number;
    significance: string;
  }>;
  heterogeneityResults: Array<{
    variable: string;
    coefficient: number;
    standardError: number;
    tStat: number;
    pValue: number;
    significance: string;
  }>;
  diagnosticTests: Array<{
    testName: string;
    result: string;
    suggestion: string;
    status: 'success' | 'warning' | 'error';
  }>;
  robustnessTests: Array<{
    testName: string;
    description: string;
    result: string;
    conclusion: string;
  }>;
  timeSeriesResults?: Array<{
    variable: string;
    coefficient: number;
    standardError: number;
    tStat: number;
    pValue: number;
    lag: number;
  }>;
  mediationResults?: Array<{
    path: string;
    coefficient: number;
    standardError: number;
    zStat: number;
    pValue: number;
    proportion: number;
  }>;
  moderationResults?: Array<{
    interaction: string;
    coefficient: number;
    standardError: number;
    tStat: number;
    pValue: number;
    simpleSlope: Array<{
      level: string;
      slope: number;
      standardError: number;
      tStat: number;
      pValue: number;
    }>;
  }>;
  endogeneityResults?: Array<{
    method: string;
    firstStage: Array<{
      variable: string;
      coefficient: number;
      standardError: number;
      tStat: number;
      pValue: number;
      significance: string;
    }>;
    secondStage: Array<{
      variable: string;
      coefficient: number;
      standardError: number;
      tStat: number;
      pValue: number;
      significance: string;
    }>;
    testResults: Array<{
      testName: string;
      statistic: number;
      pValue: number;
      conclusion: string;
    }>;
  }>;
  panelDataResults?: Array<{
    model: string;
    results: Array<{
      variable: string;
      coefficient: number;
      standardError: number;
      tStat: number;
      pValue: number;
      significance: string;
    }>;
    testResults: Array<{
      testName: string;
      statistic: number;
      pValue: number;
      conclusion: string;
    }>;
  }>;
  selectedMethods: string[];
}

// 实证分析相关的类型定义
export interface EmpiricalAnalysisContext {
  selectedMethods: string[];
  regressionResults: any[];
  heterogeneityResults: any[];
  diagnosticTests: any[];
  robustnessTests: any[];
}

export interface GenerateAnalysisResponse {
  content: string;
}

// 实证分析API服务
export const empiricalApi = {
  getResults: async (params: { writingId: string; sectionId: string }): Promise<{ data: EmpiricalAnalysisResult }> => {
    const response = await axiosInstance.get(`/api/writing/${params.writingId}/sections/${params.sectionId}/empirical-analysis/results`);
    return response.data;
  },
  
  updateAnalysis: async (params: { writingId: string; sectionId: string; section: string; content: string }): Promise<{ success: boolean }> => {
    const response = await axiosInstance.put(`/api/writing/${params.writingId}/sections/${params.sectionId}/empirical-analysis/${params.section}`, {
      content: params.content
    });
    return response.data;
  },
  
  runRobustnessTest: async (params: { writingId: string; sectionId: string; testName: string }): Promise<{ data: { success: boolean; message?: string } }> => {
    const response = await axiosInstance.post(`/api/writing/${params.writingId}/sections/${params.sectionId}/empirical-analysis/robustness`, {
      testName: params.testName
    });
    return response.data;
  },

  // 获取智能代理消息历史
  getAgentMessages: async ({
    sectionId,
    type
  }: {
    sectionId: string;
    type: string;
  }) => {
    return axiosInstance.get<{ messages: AgentMessage[] }>(
      `/api/empirical/${sectionId}/agent/messages`,
      { params: { type } }
    );
  },

  // 发送消息给智能代理
  sendAgentMessage: async ({
    sectionId,
    content,
    type,
    context
  }: {
    sectionId: string;
    content: string;
    type: string;
    context: EmpiricalAnalysisContext;
  }) => {
    return axiosInstance.post<AgentMessage>(
      `/api/empirical/${sectionId}/agent/message`,
      { content, type, context }
    );
  },

  // 生成分析文本
  generateAnalysis: async ({
    sectionId,
    section,
    context
  }: {
    sectionId: string;
    section: string;
    context: EmpiricalAnalysisContext;
  }) => {
    return axiosInstance.post<GenerateAnalysisResponse>(
      `/api/empirical/${sectionId}/generate/${section}`,
      { context }
    );
  },

  // 保存实证分析
  saveEmpiricalAnalysis: async ({
    sectionId,
    data
  }: {
    sectionId: string;
    data: any;
  }) => {
    return axiosInstance.post(
      `/api/empirical/${sectionId}/save`,
      data
    );
  },

  // 获取实证分析
  getEmpiricalAnalysis: async (sectionId: string) => {
    return axiosInstance.get(
      `/api/empirical/${sectionId}`
    );
  }
};