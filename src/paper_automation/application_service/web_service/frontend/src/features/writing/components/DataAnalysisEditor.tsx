import React, { useState, useEffect } from 'react';
import { Card, Upload, message, Select, InputNumber, Table, Checkbox, Row, Col, Statistic, Space, Radio, Alert, Input, Typography, Tooltip, Tag } from 'antd';
import { UploadOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { Box, Button, Stack } from '@mui/material';
import { axiosInstance } from '../../../services/api';
import { recommendMethodsByDataStructure } from '../utils/methodRecommendation';
import type { MethodRecommendation } from '../utils/methodRecommendation';

const { Title, Text } = Typography;

interface PreprocessConfig {
  missingValue: {
    method: 'mean' | 'median' | 'mode' | 'none';
    threshold: number;
  };
  outlier: {
    method: 'zscore' | 'iqr' | 'none';
    threshold: number;
  };
  standardization: {
    method: 'zscore' | 'minmax' | 'none';
  };
}

type VariableRole = 'dependent' | 'independent' | 'instrumental' | 'control' | 'moderator' | 'mediator' | 'grouping' | 'time' | 'id' | 'dummy';

interface VariableInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'dummy';
  role?: VariableRole;
  stats: {
    mean?: number;
    median?: number;
    std?: number;
    min?: number;
    max?: number;
    categories?: string[];
    frequencies?: number[];
    missing: number;
    skewness?: number;
    kurtosis?: number;
    isDummy?: boolean;
  };
}

interface ProcessedData {
  variables: VariableInfo[];
  rawData: any[][];
  preprocessConfig: PreprocessConfig;
}

export interface DataAnalysisData {
  preprocessConfig: PreprocessConfig;
  selectedVars: string[];
  processedData: ProcessedData | null;
  dataPreview?: string;
  dataSource?: string;
}

interface DataAnalysisEditorProps {
  onSave?: (data: DataAnalysisData) => void;
  onPrev?: () => void;
  onNext?: () => void;
  initialData?: DataAnalysisData;
  writingId: string;
  sectionId: string;
}

type DataType = 'cross' | 'panel' | 'time';

interface DataTypeInfo {
  type: DataType;
  confidence: number;
}

// 子组件定义
const PreprocessingConfig: React.FC<{
  config: PreprocessConfig;
  onConfigChange: (config: PreprocessConfig) => void;
}> = ({ config, onConfigChange }) => {
  const handleChange = (field: string, subField: string, value: any) => {
    const defaultThresholds = {
      missingValue: 0.5,
      outlier: 3,
    };

    onConfigChange({
      ...config,
      [field]: {
        ...config[field as keyof PreprocessConfig],
        [subField]: value,
        threshold: defaultThresholds[field as keyof typeof defaultThresholds] || 0
      }
    });
  };

  return (
    <Space size="large">
      <Space>
        <span style={{ color: '#000', fontWeight: 500 }}>缺失值处理</span>
        <Select
          value={config.missingValue.method}
          onChange={(value) => handleChange('missingValue', 'method', value)}
          style={{ width: 120 }}
          bordered={false}
        >
          <Select.Option value="mean">均值填充</Select.Option>
          <Select.Option value="median">中位数填充</Select.Option>
          <Select.Option value="mode">众数填充</Select.Option>
          <Select.Option value="none">不处理</Select.Option>
        </Select>
      </Space>

      <Space>
        <span style={{ color: '#000', fontWeight: 500 }}>异常值处理</span>
        <Select
          value={config.outlier.method}
          onChange={(value) => handleChange('outlier', 'method', value)}
          style={{ width: 120 }}
          bordered={false}
        >
          <Select.Option value="zscore">Z-score</Select.Option>
          <Select.Option value="iqr">IQR</Select.Option>
          <Select.Option value="none">不处理</Select.Option>
        </Select>
      </Space>

      <Space>
        <span style={{ color: '#000', fontWeight: 500 }}>标准化处理</span>
        <Select
          value={config.standardization.method}
          onChange={(value) => handleChange('standardization', 'method', value)}
          style={{ width: 120 }}
          bordered={false}
        >
          <Select.Option value="zscore">Z-score标准化</Select.Option>
          <Select.Option value="minmax">Min-Max标准化</Select.Option>
          <Select.Option value="none">不处理</Select.Option>
        </Select>
      </Space>
    </Space>
  );
};

const roleMapping: Record<VariableRole, string> = {
  dependent: '因变量',
  independent: '自变量',
  control: '控制变量',
  instrumental: '工具变量',
  moderator: '调节变量',
  mediator: '中介变量',
  grouping: '分组变量',
  time: '时间标识变量',
  id: '个体标识变量',
  dummy: '虚拟变量'
};

const getRoleName = (role: VariableRole | undefined) => {
  if (!role) return '-';
  return roleMapping[role];
};

const VariableSelection: React.FC<{
  variables: VariableInfo[];
  selectedVars: VariableInfo[];
  onVariableChange: (vars: VariableInfo[]) => void;
  dataType: 'cross' | 'panel' | 'time';
}> = ({ variables, selectedVars, onVariableChange, dataType }) => {
  const handleVariableChange = (varName: string, role: string) => {
    const variable = variables.find(v => v.name === varName);
    if (variable) {
      const newSelectedVars = [...selectedVars];
      const existingIndex = newSelectedVars.findIndex(v => v.name === varName);
      
      if (existingIndex >= 0) {
        // 更新已存在变量的角色
        newSelectedVars[existingIndex] = { ...variable, role: role as VariableInfo['role'] };
      } else {
        // 添加新变量
        newSelectedVars.push({ ...variable, role: role as VariableInfo['role'] });
      }
      
      onVariableChange(newSelectedVars);
    }
  };

  const handleRemoveVariable = (varName: string) => {
    onVariableChange(selectedVars.filter(v => v.name !== varName));
  };

  return (
    <Card title="变量选择">
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* 标识变量选择区域 */}
        {dataType !== 'cross' && (
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <div style={{ marginBottom: '8px' }}>
                <Text strong>时间标识变量</Text>
                <Tooltip title="用于标识时间维度的变量，如年份、季度等">
                  <InfoCircleOutlined style={{ marginLeft: '4px' }} />
                </Tooltip>
              </div>
            <Select
                style={{ width: '100%' }}
                placeholder="选择时间标识变量"
                value={selectedVars.find(v => v.role === 'time')?.name || undefined}
                onChange={(value) => value ? handleVariableChange(value, 'time') : handleRemoveVariable(selectedVars.find(v => v.role === 'time')?.name || '')}
                allowClear
              >
                {variables.map(v => (
                  <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
                ))}
            </Select>
            </Col>
            <Col span={12}>
              <div style={{ marginBottom: '8px' }}>
                <Text strong>个体标识变量</Text>
                <Tooltip title="用于标识个体的变量，如公司代码、省份代码等">
                  <InfoCircleOutlined style={{ marginLeft: '4px' }} />
                </Tooltip>
              </div>
            <Select
                style={{ width: '100%' }}
                placeholder="选择个体标识变量"
                value={selectedVars.find(v => v.role === 'id')?.name || undefined}
                onChange={(value) => value ? handleVariableChange(value, 'id') : handleRemoveVariable(selectedVars.find(v => v.role === 'id')?.name || '')}
                allowClear
              >
                {variables.map(v => (
                  <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
                ))}
            </Select>
            </Col>
          </Row>
        )}

        {/* 主要变量选择区域 */}
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>因变量</Text>
              <Tooltip title="选择您要研究的目标变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              style={{ width: '100%' }}
              placeholder="选择因变量"
              value={selectedVars.find(v => v.role === 'dependent')?.name || undefined}
              onChange={(value) => value ? handleVariableChange(value, 'dependent') : handleRemoveVariable(selectedVars.find(v => v.role === 'dependent')?.name || '')}
              allowClear
            >
              {variables.filter(v => v.type === 'numeric').map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>自变量</Text>
              <Tooltip title="选择您认为会影响因变量的解释变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择自变量"
              value={selectedVars.filter(v => v.role === 'independent').map(v => v.name)}
              onChange={(values) => {
                const currentIndependent = selectedVars.filter(v => v.role === 'independent');
                const toRemove = currentIndependent.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentIndependent.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'independent'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>控制变量</Text>
              <Tooltip title="选择需要控制的其他影响因素">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择控制变量"
              value={selectedVars.filter(v => v.role === 'control').map(v => v.name)}
              onChange={(values) => {
                const currentControl = selectedVars.filter(v => v.role === 'control');
                const toRemove = currentControl.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentControl.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'control'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
        </Row>

        <Row gutter={[16, 16]}>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>工具变量</Text>
              <Tooltip title="用于处理内生性问题的工具变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择工具变量"
              value={selectedVars.filter(v => v.role === 'instrumental').map(v => v.name)}
              onChange={(values) => {
                const currentInstrumental = selectedVars.filter(v => v.role === 'instrumental');
                const toRemove = currentInstrumental.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentInstrumental.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'instrumental'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>调节变量</Text>
              <Tooltip title="用于检验调节效应的变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择调节变量"
              value={selectedVars.filter(v => v.role === 'moderator').map(v => v.name)}
              onChange={(values) => {
                const currentModerator = selectedVars.filter(v => v.role === 'moderator');
                const toRemove = currentModerator.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentModerator.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'moderator'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>中介变量</Text>
              <Tooltip title="用于检验中介效应的变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择中介变量"
              value={selectedVars.filter(v => v.role === 'mediator').map(v => v.name)}
              onChange={(values) => {
                const currentMediator = selectedVars.filter(v => v.role === 'mediator');
                const toRemove = currentMediator.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentMediator.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'mediator'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
          <Col span={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>虚拟变量</Text>
              <Tooltip title="取值仅为0和1的二分类变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择虚拟变量"
              value={selectedVars.filter(v => v.role === 'dummy').map(v => v.name)}
              onChange={(values) => {
                const currentDummy = selectedVars.filter(v => v.role === 'dummy');
                const toRemove = currentDummy.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentDummy.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'dummy'));
              }}
              allowClear
            >
              {variables.filter(v => v.type === 'dummy' || (v.type === 'numeric' && v.stats.min === 0 && v.stats.max === 1)).map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
          <Col span={8} offset={8}>
            <div style={{ marginBottom: '8px' }}>
              <Text strong>分组变量</Text>
              <Tooltip title="用于进行异质性分析的分组变量，可以是分类变量或数值变量">
                <InfoCircleOutlined style={{ marginLeft: '4px' }} />
              </Tooltip>
            </div>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="选择分组变量"
              value={selectedVars.filter(v => v.role === 'grouping').map(v => v.name)}
              onChange={(values) => {
                const currentGrouping = selectedVars.filter(v => v.role === 'grouping');
                const toRemove = currentGrouping.filter(v => !values.includes(v.name));
                const toAdd = values.filter(value => !currentGrouping.find(v => v.name === value));
                
                toRemove.forEach(v => handleRemoveVariable(v.name));
                toAdd.forEach(value => handleVariableChange(value, 'grouping'));
              }}
              allowClear
            >
              {variables.map(v => (
                <Select.Option key={v.name} value={v.name}>{v.name}</Select.Option>
              ))}
            </Select>
          </Col>
        </Row>
      </Space>
    </Card>
  );
};

const DescriptiveStats: React.FC<{
  variables: VariableInfo[];
  rawDataLength: number;
}> = ({ variables, rawDataLength }) => {
  const columns = [
    {
      title: '变量类型',
      dataIndex: 'role',
      key: 'role',
      width: 120,
      align: 'center' as const,
      fixed: 'left' as const,
      render: (role: VariableRole) => roleMapping[role] || '-'
    },
    {
      title: '变量名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
      align: 'center' as const,
      fixed: 'left' as const,
    },
    {
      title: '变量描述',
      dataIndex: 'varType',
      key: 'varType',
      width: 120,
      align: 'center' as const,
    },
    {
      title: '样本量',
      dataIndex: 'sampleSize',
      key: 'sampleSize',
      width: 100,
      align: 'center' as const,
    },
    {
      title: '均值',
      dataIndex: 'mean',
      key: 'mean',
      width: 100,
      align: 'center' as const,
      render: (value: number | undefined) => value?.toFixed(4) ?? '-'
    },
    {
      title: '标准差',
      dataIndex: 'std',
      key: 'std',
      width: 100,
      align: 'center' as const,
      render: (value: number | undefined) => value?.toFixed(4) ?? '-'
    },
    {
      title: '最小值',
      dataIndex: 'min',
      key: 'min',
      width: 100,
      align: 'center' as const,
      render: (value: number | undefined) => value?.toFixed(4) ?? '-'
    },
    {
      title: '最大值',
      dataIndex: 'max',
      key: 'max',
      width: 100,
      align: 'center' as const,
      render: (value: number | undefined) => value?.toFixed(4) ?? '-'
    }
  ];

  const dataSource = variables.map(variable => ({
    key: variable.name,
    varType: variable.type === 'numeric' ? '数值型变量' : '分类型变量',
    name: variable.name,
    role: variable.role,
    sampleSize: rawDataLength,
    mean: variable.stats.mean,
    std: variable.stats.std,
    min: variable.stats.min,
    max: variable.stats.max
  }));

  return (
    <Card title="描述性统计">
      <div style={{ 
        width: '100%',
        overflow: 'auto'
      }}>
        <Table
          columns={columns}
          dataSource={dataSource}
          pagination={false}
          scroll={{ x: 'max-content', y: 400 }}
          size="middle"
          bordered
          sticky
        />
      </div>
    </Card>
  );
};

export const DataAnalysisEditor: React.FC<DataAnalysisEditorProps> = ({
  onSave,
  onPrev,
  onNext,
  initialData,
        writingId,
        sectionId,
}) => {
  const [processedData, setProcessedData] = useState<ProcessedData | null>(initialData?.processedData || null);
  const [selectedVars, setSelectedVars] = useState<string[]>(initialData?.selectedVars || []);
  const [preprocessConfig, setPreprocessConfig] = useState<PreprocessConfig>(
    initialData?.preprocessConfig || {
      missingValue: { method: 'mean', threshold: 0.5 },
      outlier: { method: 'zscore', threshold: 3 },
      standardization: { method: 'zscore' }
    }
  );
  const [uploading, setUploading] = useState(false);
  const [dataPreview, setDataPreview] = useState<string>(initialData?.dataPreview || '');
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const [dataType, setDataType] = useState<DataType>('cross');
  const [detectedDataType, setDetectedDataType] = useState<DataTypeInfo | null>(null);
  const [dataSource, setDataSource] = useState<string>(initialData?.dataSource || '');
  const [methodRecommendations, setMethodRecommendations] = useState<MethodRecommendation[]>([]);
  const [selectedVariables, setSelectedVariables] = useState<VariableInfo[]>([]);
  const [analysisType, setAnalysisType] = useState<'single' | 'multiple'>('single');
  const [selectedAnalysisVariables, setSelectedAnalysisVariables] = useState<string[]>([]);
  const [analysisMethod, setAnalysisMethod] = useState<string | null>(null);
  const [selectedMethod, setSelectedMethod] = useState<MethodRecommendation | null>(null);

  const handleFileUpload = async (file: File) => {
    if (!file) {
      message.error('请选择要上传的文件');
      return false;
    }

    // 检查文件类型
    const allowedTypes = [
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'text/csv'
    ];
    if (!allowedTypes.includes(file.type)) {
      message.error('只支持 .csv, .xlsx, .xls 格式的文件');
      return false;
    }

    try {
      setUploading(true);
      setCurrentFile(file);
      const formData = new FormData();
      formData.append('file', file);

      console.log('正在上传文件:', {
        fileName: file.name,
        fileType: file.type,
        fileSize: file.size,
        writingId,
        sectionId
      });

      const response = await axiosInstance.post(
        `/api/writing/${writingId}/sections/${sectionId}/data-analysis/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              message.loading({ content: `上传中 ${percent}%`, key: 'upload' });
            }
          },
          withCredentials: true
        }
      );

      if (response.data) {
        setProcessedData(response.data.processedData);
        setDataPreview(response.data.preview);
        // 设置检测到的数据类型
        if (response.data.detectedDataType) {
          setDetectedDataType(response.data.detectedDataType);
          setDataType(response.data.detectedDataType.type);
        }
        message.success({ content: '文件上传成功', key: 'upload' });

        // 更新方法推荐
        const recommendations = recommendMethodsByDataStructure({
          dataType: response.data.detectedDataType.type,
          hasInstrumental: false, // 这些属性可以从后端返回的数据中获取
          hasMediator: false,
          hasModerator: false,
          hasGroupVariable: response.data.processedData.variables.some((v: any) => v.type === 'categorical'),
          hasTimeVariable: response.data.processedData.variables.some((v: any) => v.type === 'time'),
          hasEntityVariable: response.data.processedData.variables.some((v: any) => v.type === 'id'),
          sampleSize: response.data.processedData.variables[0]?.observations || 0,
        });
        setMethodRecommendations(recommendations);

        return true;
      }
    } catch (error: any) {
      console.error('文件上传失败:', error);
      let errorMessage = '文件上传失败';
      if (error.response) {
        switch (error.response.status) {
          case 400:
            errorMessage = '文件格式错误或数据无效';
            break;
          case 413:
            errorMessage = '文件大小超出限制';
            break;
          case 415:
            errorMessage = '不支持的文件类型';
            break;
          default:
            errorMessage = error.response.data?.message || '文件上传失败，请重试';
        }
      }
      message.error({ content: errorMessage, key: 'upload' });
      setCurrentFile(null);
    } finally {
      setUploading(false);
    }
    return false;
  };

  const handleDataTypeChange = (e: any) => {
    setDataType(e.target.value);
  };

  // 添加实证分析触发函数
  const triggerEmpiricalAnalysis = async () => {
    try {
      if (!processedData || !selectedMethod || selectedVariables.length === 0) {
        message.error('请先完成数据分析配置');
        return;
      }

      // 准备变量数据
      const variables = selectedVariables.map(v => ({
        name: v.name,
        role: v.role,
        type: v.type
      }));

      // 发送实证分析请求
      await axiosInstance.post(`/api/writing/${writingId}/sections/${sectionId}/empirical-analysis/start`, {
        writingId,
        sectionId,
        dataType,
        selectedMethod,
        variables,
        preprocessConfig,
        dataSource: currentFile?.name
      });

      // 更新章节内容
      await axiosInstance.put(`/api/writings/${writingId}/sections/${sectionId}`, {
        content: JSON.stringify({
          dataType,
          selectedMethod,
          variables,
          preprocessConfig,
          dataSource: currentFile?.name
        }),
        completed: true
      });

      message.success('实证分析已开始');
      if (onNext) {
        onNext();
      }
    } catch (error) {
      console.error('实证分析错误:', error);
      message.error('实证分析失败，请重试');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1rem' }}>
      <Card title="1. 上传数据">
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Row gutter={24} align="middle">
            <Col span={12}>
              <Stack direction="row" spacing={2}>
                <Upload 
                  beforeUpload={handleFileUpload}
                  accept=".csv,.xlsx,.xls"
                  showUploadList={false}
                >
          <Button
            variant="contained"
                    color="primary"
                    startIcon={<UploadOutlined />}
                    disabled={uploading}
                  >
                    {uploading ? '上传中...' : '选择文件'}
          </Button>
                </Upload>
                {currentFile && <span>已选择: {currentFile.name}</span>}
              </Stack>
            </Col>
            <Col span={12}>
              <div>
                <div style={{ marginBottom: '8px' }}>数据类型</div>
                <Radio.Group onChange={handleDataTypeChange} value={dataType}>
                  <Radio value="cross">截面数据</Radio>
                  <Radio value="panel">面板数据</Radio>
                  <Radio value="time">时间序列数据</Radio>
                </Radio.Group>
                {detectedDataType && (
                  <Alert
                    style={{ marginTop: '8px' }}
                    message={`系统检测到这可能是${
                      detectedDataType.type === 'cross' ? '截面数据' :
                      detectedDataType.type === 'panel' ? '面板数据' : '时间序列数据'
                    }`}
                    type="info"
                    showIcon
                    icon={<InfoCircleOutlined />}
                  />
                )}
              </div>
            </Col>
          </Row>
          
          <div>
            <div style={{ marginBottom: '8px' }}>数据来源说明</div>
            <Input.TextArea
              placeholder="请输入数据来源说明，例如：2010-2020年30个省市的统计年鉴数据"
              value={dataSource}
              onChange={(e) => setDataSource(e.target.value)}
              autoSize={{ minRows: 2, maxRows: 4 }}
              style={{ width: '100%' }}
            />
            <div style={{ marginTop: '4px', color: '#888', fontSize: '12px' }}>
              这个说明将在数据分析和结论部分被引用
            </div>
          </div>
        </Space>
      </Card>

      {dataPreview && (
        <Card>
          <div style={{ 
            display: 'flex', 
            flexDirection: 'column',
            gap: '16px'
          }}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              borderBottom: '1px solid #f0f0f0',
              paddingBottom: '12px'
            }}>
              <span style={{ fontSize: '16px', fontWeight: 500 }}>2. 数据预览</span>
              <PreprocessingConfig
                config={preprocessConfig}
                onConfigChange={setPreprocessConfig}
              />
            </div>

            <div style={{ 
              overflowX: 'auto',
              overflowY: 'auto',
              maxHeight: '400px',
              fontFamily: 'monospace',
              fontSize: '14px',
              border: '1px solid #f0f0f0',
              borderRadius: '8px'
            }}>
              <table style={{ 
                width: '100%', 
                borderCollapse: 'collapse',
                whiteSpace: 'nowrap',
                tableLayout: 'fixed'
              }}>
                <thead style={{ position: 'sticky', top: 0, backgroundColor: '#fafafa', zIndex: 1 }}>
                  <tr>
                    {dataPreview.split('\n')[0].split(/\s+/).map((cell, cellIndex) => (
                      <th 
                        key={cellIndex}
                        style={{ 
                          padding: '12px 16px',
                          borderBottom: '1px solid #f0f0f0',
                          textAlign: 'center',
                          color: '#666',
                          fontWeight: 500
                        }}
                      >
                        {cell}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {dataPreview.split('\n').slice(1).map((line, index) => (
                    <tr key={index}>
                      {line.split(/\s+/).map((cell, cellIndex) => (
                        <td 
                          key={cellIndex}
                          style={{ 
                            padding: '8px 16px',
                            borderBottom: '1px solid #f0f0f0',
                            textAlign: 'center'
                          }}
                        >
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </Card>
      )}

      {processedData && (
        <Card title="3. 变量信息">
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {/* 变量选择部分 */}
            <VariableSelection
              variables={processedData.variables}
              selectedVars={selectedVariables}
              onVariableChange={setSelectedVariables}
              dataType={dataType}
            />

            {/* 描述性统计部分 */}
            {selectedVariables.length > 0 && (
              <DescriptiveStats 
                variables={selectedVariables}
                rawDataLength={processedData.rawData.length}
              />
            )}

            {/* 变量分析部分 */}
            {selectedVariables.length > 0 && (
              <Card title="变量分析">
                <Space direction="vertical" style={{ width: '100%' }} size="large">
                  {/* 分析类型选择 */}
                  <Row gutter={[16, 16]}>
                    <Col span={8}>
                      <div style={{ marginBottom: '8px' }}>
                        <Text strong>分析类型</Text>
                        <Tooltip title="选择要进行的分析类型">
                          <InfoCircleOutlined style={{ marginLeft: '4px' }} />
                        </Tooltip>
                      </div>
                <Select
                        style={{ width: '100%' }}
                        placeholder="选择分析类型"
                        onChange={(value) => setAnalysisType(value)}
                      >
                        <Select.Option value="single">单变量分析</Select.Option>
                        <Select.Option value="multiple">多变量分析</Select.Option>
                </Select>
                    </Col>
                  </Row>

                  {/* 变量选择（根据分析类型显示不同的选择框） */}
                  {analysisType && (
                    <Row gutter={[16, 16]}>
                      <Col span={24}>
                        <Card size="small" title="选择分析变量">
                          {analysisType === 'single' ? (
              <Select
                              style={{ width: '100%' }}
                              placeholder="选择要分析的变量"
                              onChange={(value) => setSelectedAnalysisVariables([value])}
                            >
                              {selectedVariables.map(variable => (
                                <Select.Option key={variable.name} value={variable.name}>
                                  {variable.name} ({getRoleName(variable.role)})
                                </Select.Option>
                  ))}
              </Select>
                          ) : (
              <Select
                              mode="multiple"
                              style={{ width: '100%' }}
                              placeholder="选择要分析的变量（可多选）"
                              onChange={(values) => setSelectedAnalysisVariables(values)}
                            >
                              {selectedVariables.map(variable => (
                                <Select.Option key={variable.name} value={variable.name}>
                                  {variable.name} ({getRoleName(variable.role)})
                                </Select.Option>
                  ))}
              </Select>
                          )}
                        </Card>
                      </Col>
                    </Row>
                  )}

                  {/* 分析方法选择 */}
                  {selectedAnalysisVariables.length > 0 && (
                    <Row gutter={[16, 16]}>
                      <Col span={24}>
                        <Card size="small" title="选择分析方法">
              <Select
                            style={{ width: '100%' }}
                            placeholder="选择分析方法"
                            onChange={(value) => setAnalysisMethod(value)}
                          >
                            {analysisType === 'single' ? (
                              <>
                                <Select.Option value="distribution">分布特征分析</Select.Option>
                                <Select.Option value="descriptive">描述性统计分析</Select.Option>
                                <Select.Option value="normality">正态性检验</Select.Option>
                              </>
                            ) : (
                              <>
                                <Select.Option value="correlation">相关性分析</Select.Option>
                                <Select.Option value="scatter">散点图分析</Select.Option>
                                <Select.Option value="covariance">协方差分析</Select.Option>
                              </>
                            )}
              </Select>
                        </Card>
                      </Col>
                    </Row>
                  )}

                  {/* 分析结果展示 */}
                  {analysisMethod && selectedAnalysisVariables.length > 0 && (
                    <Row gutter={[16, 16]}>
                      <Col span={24}>
                        <Card 
                          title={
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <Text strong>分析结果</Text>
                              <Tag color="blue">{analysisType === 'single' ? '单变量分析' : '多变量分析'}</Tag>
                              <Tag color="green">{
                                {
                                  'distribution': '分布特征分析',
                                  'descriptive': '描述性统计分析',
                                  'normality': '正态性检验',
                                  'correlation': '相关性分析',
                                  'scatter': '散点图分析',
                                  'covariance': '协方差分析'
                                }[analysisMethod]
                              }</Tag>
                            </div>
                          }
                        >
                          {/* 单变量分析结果 */}
                          {analysisType === 'single' && (
                            <>
                              {selectedAnalysisVariables.map((varName) => {
                                const variable = selectedVariables.find(v => v.name === varName);
                                if (!variable) return null;

                                return (
                                  <Card
                                    key={variable.name}
                                    type="inner"
                                    title={
                                      <Space>
                                        <Text strong style={{ fontSize: '16px' }}>{variable.name}</Text>
                                        <Tag color={
                                          variable.role === 'dependent' ? 'red' :
                                          variable.role === 'independent' ? 'blue' :
                                          variable.role === 'control' ? 'green' :
                                          variable.role === 'instrumental' ? 'purple' :
                                          variable.role === 'moderator' ? 'orange' :
                                          variable.role === 'mediator' ? 'cyan' :
                                          'default'
                                        }>{getRoleName(variable.role)}</Tag>
                                        <Tag color={variable.type === 'numeric' ? 'processing' : 'warning'}>
                                          {variable.type === 'numeric' ? '数值型' : '分类型'}
                                        </Tag>
                                      </Space>
                                    }
                                    style={{ marginBottom: '16px' }}
                                  >
                                    <div style={{ padding: '0 16px' }}>
                                      {/* 分布特征分析 */}
                                      {analysisMethod === 'distribution' && variable.type === 'numeric' && (
                                        <>
                                          <Row gutter={[32, 16]}>
                                            <Col span={6}>
                                              <Card className="stat-card" bordered={false}>
                                                <Statistic 
                                                  title={<Text strong>偏度</Text>}
                                                  value={variable.stats?.skewness}
                                                  precision={4}
                                                  valueStyle={{ color: '#13c2c2' }}
                                                />
                                              </Card>
                                            </Col>
                                            <Col span={6}>
                                              <Card className="stat-card" bordered={false}>
                                                <Statistic 
                                                  title={<Text strong>峰度</Text>}
                                                  value={variable.stats?.kurtosis}
                                                  precision={4}
                                                  valueStyle={{ color: '#13c2c2' }}
                                                />
                                              </Card>
                                            </Col>
                                            <Col span={6}>
                                              <Card className="stat-card" bordered={false}>
                                                <Statistic 
                                                  title={<Text strong>变异系数</Text>}
                                                  value={(() => {
                                                    const mean = variable.stats?.mean;
                                                    const std = variable.stats?.std;
                                                    return mean && std && mean !== 0 ? (std / mean) * 100 : undefined;
                                                  })()}
                                                  precision={2}
                                                  valueStyle={{ color: '#722ed1' }}
                                                  suffix="%"
                                                />
                                              </Card>
                                            </Col>
                                          </Row>
                                          <Alert
                                            style={{ marginTop: '16px' }}
                                            type="info"
                                            message={
                                              <div>
                                                <p>• 分布形态：{
                                                  variable.stats?.skewness
                                                    ? Math.abs(variable.stats.skewness) < 0.5
                                                      ? '近似对称'
                                                      : variable.stats.skewness > 0
                                                        ? '右偏'
                                                        : '左偏'
                                                    : '无法判断'
                                                }</p>
                                                <p>• 尖峰程度：{
                                                  variable.stats?.kurtosis
                                                    ? variable.stats.kurtosis > 3
                                                      ? '尖峰分布'
                                                      : variable.stats.kurtosis < 3
                                                        ? '平峰分布'
                                                        : '正态分布'
                                                    : '无法判断'
                                                }</p>
                                                <p>• 离散程度：{(() => {
                                                  const cv = variable.stats?.std && variable.stats?.mean && variable.stats.mean !== 0
                                                    ? variable.stats.std / variable.stats.mean
                                                    : null;
                                                  return cv
                                                    ? cv < 0.15
                                                      ? '离散程度低'
                                                      : cv < 0.3
                                                        ? '离散程度中等'
                                                        : '离散程度高'
                                                    : '无法判断';
                                                })()}</p>
                                              </div>
                                            }
                                          />
                                        </>
                                      )}

                                      {/* 描述性统计分析 */}
                                      {analysisMethod === 'descriptive' && (
                                        <>
                                          {variable.type === 'numeric' ? (
                                            <>
                                              <Row gutter={[32, 16]}>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>均值</Text>}
                                                      value={variable.stats?.mean}
                                                      precision={4}
                                                      valueStyle={{ color: '#1890ff' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>中位数</Text>}
                                                      value={variable.stats?.median}
                                                      precision={4}
                                                      valueStyle={{ color: '#52c41a' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>标准差</Text>}
                                                      value={variable.stats?.std}
                                                      precision={4}
                                                      valueStyle={{ color: '#722ed1' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>样本量</Text>}
                                                      value={processedData.rawData.length - (variable.stats?.missing || 0)}
                                                      valueStyle={{ color: '#fa8c16' }}
                                                    />
                                                  </Card>
                                                </Col>
                                              </Row>
                                              <Row gutter={[32, 16]} style={{ marginTop: '16px' }}>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>最小值</Text>}
                                                      value={variable.stats?.min}
                                                      precision={4}
                                                      valueStyle={{ color: '#eb2f96' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>最大值</Text>}
                                                      value={variable.stats?.max}
                                                      precision={4}
                                                      valueStyle={{ color: '#eb2f96' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>缺失值</Text>}
                                                      value={variable.stats?.missing}
                                                      valueStyle={{ color: '#f5222d' }}
                                                    />
                                                  </Card>
                                                </Col>
                                                <Col span={6}>
                                                  <Card className="stat-card" bordered={false}>
                                                    <Statistic 
                                                      title={<Text strong>缺失率</Text>}
                                                      value={(variable.stats?.missing / processedData.rawData.length) * 100}
                                                      precision={2}
                                                      valueStyle={{ color: '#f5222d' }}
                                                      suffix="%"
                                                    />
                                                  </Card>
                                                </Col>
                                              </Row>
                                            </>
                                          ) : (
                                            <Table
                                              dataSource={variable.stats.categories?.map((category, index) => ({
                                                key: index,
                                                category,
                                                frequency: variable.stats.frequencies?.[index] || 0,
                                                percentage: ((variable.stats.frequencies?.[index] || 0) / processedData.rawData.length * 100).toFixed(2)
                                              }))}
                                              columns={[
                                                {
                                                  title: '类别',
                                                  dataIndex: 'category',
                                                  key: 'category',
                                                },
                                                {
                                                  title: '频数',
                                                  dataIndex: 'frequency',
                                                  key: 'frequency',
                                                },
                                                {
                                                  title: '占比',
                                                  dataIndex: 'percentage',
                                                  key: 'percentage',
                                                  render: (text) => `${text}%`
                                                }
                                              ]}
                                              size="small"
                                              pagination={false}
                                            />
                                          )}
                                        </>
                                      )}

                                      {/* 正态性检验 */}
                                      {analysisMethod === 'normality' && variable.type === 'numeric' && (
                                        <>
                                          <Alert
                                            type="info"
                                            message={
                                              <div>
                                                <p>• 偏度检验：{
                                                  variable.stats?.skewness
                                                    ? Math.abs(variable.stats.skewness) < 0.5
                                                      ? '通过，数据分布近似对称'
                                                      : '未通过，数据分布' + (variable.stats.skewness > 0 ? '右偏' : '左偏')
                                                    : '无法判断'
                                                }</p>
                                                <p>• 峰度检验：{
                                                  variable.stats?.kurtosis
                                                    ? Math.abs(variable.stats.kurtosis - 3) < 0.5
                                                      ? '通过，数据呈正态分布'
                                                      : '未通过，数据呈' + (variable.stats.kurtosis > 3 ? '尖峰' : '平峰') + '分布'
                                                    : '无法判断'
                                                }</p>
                                                <p>• 综合判断：{
                                                  variable.stats?.skewness && variable.stats?.kurtosis
                                                    ? Math.abs(variable.stats.skewness) < 0.5 && Math.abs(variable.stats.kurtosis - 3) < 0.5
                                                      ? '数据基本符合正态分布'
                                                      : '数据不符合正态分布，建议进行数据转换'
                                                    : '无法判断'
                                                }</p>
                                              </div>
                                            }
                                          />
                                        </>
                                      )}
                                    </div>
                                  </Card>
                                );
                              })}
                            </>
                          )}

                          {/* 多变量分析结果 */}
                          {analysisType === 'multiple' && (
                            <Card type="inner">
                              {/* 相关性分析 */}
                              {analysisMethod === 'correlation' && (
                                <Table
                                  dataSource={selectedAnalysisVariables.map(varName => {
                                    const variable = selectedVariables.find(v => v.name === varName);
                                    const correlations = selectedAnalysisVariables.reduce((acc, otherVarName) => {
                                      const otherVar = selectedVariables.find(v => v.name === otherVarName);
                                      if (variable && otherVar) {
                                        // 这里应该是从后端获取相关系数，这里用随机值模拟
                                        acc[otherVarName] = varName === otherVarName ? 1 : Math.random();
                                      }
                                      return acc;
                                    }, {} as Record<string, number>);
                                    return {
                                      key: varName,
                                      variable: varName,
                                      ...correlations
                                    };
                                  })}
                                  columns={[
                                    {
                                      title: '变量',
                                      dataIndex: 'variable',
                                      key: 'variable',
                                      fixed: 'left',
                                    },
                                    ...selectedAnalysisVariables.map(varName => ({
                                      title: varName,
                                      dataIndex: varName,
                                      key: varName,
                                      render: (value: number) => value.toFixed(4)
                                    }))
                                  ]}
                                  scroll={{ x: 'max-content' }}
                                  pagination={false}
                                  bordered
                                />
                              )}

                              {/* 协方差分析 */}
                              {analysisMethod === 'covariance' && (
                                <Table
                                  dataSource={selectedAnalysisVariables.map(varName => {
                                    const variable = selectedVariables.find(v => v.name === varName);
                                    const covariances = selectedAnalysisVariables.reduce((acc, otherVarName) => {
                                      const otherVar = selectedVariables.find(v => v.name === otherVarName);
                                      if (variable && otherVar) {
                                        // 这里应该是从后端获取协方差，这里用随机值模拟
                                        acc[otherVarName] = varName === otherVarName ? variable.stats?.std || 0 : Math.random();
                                      }
                                      return acc;
                                    }, {} as Record<string, number>);
                                    return {
                                      key: varName,
                                      variable: varName,
                                      ...covariances
                                    };
                                  })}
                                  columns={[
                                    {
                                      title: '变量',
                                      dataIndex: 'variable',
                                      key: 'variable',
                                      fixed: 'left',
                                    },
                                    ...selectedAnalysisVariables.map(varName => ({
                                      title: varName,
                                      dataIndex: varName,
                                      key: varName,
                                      render: (value: number) => value.toFixed(4)
                                    }))
                                  ]}
                                  scroll={{ x: 'max-content' }}
                                  pagination={false}
                                  bordered
                                />
                              )}

                              {/* 散点图分析 */}
                              {analysisMethod === 'scatter' && (
                                <Alert
                                  type="warning"
                                  message="散点图功能正在开发中"
                                  description="该功能将在后续版本中提供，敬请期待。"
                                />
                              )}
                            </Card>
                          )}
                        </Card>
                      </Col>
                    </Row>
                  )}
                </Space>
              </Card>
            )}
          </Space>
        </Card>
      )}

      {methodRecommendations.length > 0 && !selectedMethod && (
        <Card title={
          <Space>
            <Text strong>4. 方法推荐</Text>
            <Tooltip title="系统根据您的数据特征为您推荐最适合的分析方法">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {methodRecommendations.map((method, index) => (
              <Card
                key={index}
                type="inner"
                title={
                  <Space>
                    <Text strong>{method.name}</Text>
                    <Tag color={method.confidence > 0.8 ? 'green' : 'blue'}>
                      推荐度：{Math.round(method.confidence * 100)}%
                    </Tag>
                  </Space>
                }
                extra={
                  <Button 
                    variant="contained"
                    color="primary"
                    onClick={() => {
                      setSelectedMethod(method);
                      setAnalysisMethod(method.name);
                      message.success(`已选择${method.name}作为分析方法`);
                    }}
                  >
                    选择此方法
                  </Button>
                }
              >
                <Row gutter={[24, 24]}>
                  <Col span={24}>
                    <Alert 
                      message={method.description} 
                      description={
                        <Typography.Paragraph style={{ margin: 0 }}>
                          该方法通过引入个体固定效应，可以控制不随时间变化的个体特征，从而有效地解决遗漏变量偏误问题。这种方法特别适用于研究个体内部的变化对因变量的影响，能够更准确地估计变量间的因果关系。
                        </Typography.Paragraph>
                      }
                      type="info" 
                      showIcon 
                    />
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="方法优势" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.advantages.map((adv, i) => (
                          <li key={i}>{adv}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="注意事项" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.considerations.map((con, i) => (
                          <li key={i}>{con}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="基本假设" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.assumptions.map((assumption, i) => (
                          <li key={i}>{assumption}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="建议检验" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.testMethods.map((test, i) => (
                          <li key={i}>{test}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                  
                  <Col span={24}>
                    <Card 
                      size="small" 
                      title="模型公式" 
                      bordered={false}
                      bodyStyle={{ 
                        backgroundColor: '#f5f5f5',
                        padding: '16px',
                        borderRadius: '4px',
                        fontFamily: 'KaTeX_Math, Times New Roman, serif',
                        fontSize: '16px',
                        textAlign: 'center'
                      }}
                    >
                      <Text code style={{ 
                        backgroundColor: 'transparent',
                        padding: '8px 16px',
                        border: 'none',
                        color: '#000000d9',
                        fontSize: '16px',
                        fontFamily: 'KaTeX_Math, Times New Roman, serif'
                      }}>
                        {method.formula}
                      </Text>
                      <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
                        其中，Y_it 表示因变量，α_i 表示个体固定效应，X_it 表示自变量向量，β 表示待估计的系数向量，ε_it 表示随机误差项。
                      </div>
                    </Card>
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="适用条件" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.suitableConditions.map((condition, i) => (
                          <li key={i}>{condition}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                  
                  <Col span={12}>
                    <Card size="small" title="适用场景" bordered={false}>
                      <ul style={{ paddingLeft: 20, margin: 0 }}>
                        {method.suitableScenarios.map((scenario, i) => (
                          <li key={i}>{scenario}</li>
                        ))}
                      </ul>
                    </Card>
                  </Col>
                </Row>
              </Card>
            ))}
          </Space>
        </Card>
      )}

      {selectedMethod && (
        <Card title={
          <Space>
            <Text strong>4. 已选择的分析方法</Text>
            <Tooltip title="您可以点击重新选择按钮更换分析方法">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }
        extra={
          <Button 
            variant="text"
            color="primary"
            onClick={() => {
              setSelectedMethod(null);
              message.info('已重新选择分析方法');
            }}
          >
            重新选择
          </Button>
        }
        >
          <Card
            type="inner"
            title={
              <Space>
                <Text strong>{selectedMethod.name}</Text>
                <Tag color={selectedMethod.confidence > 0.8 ? 'green' : 'blue'}>
                  推荐度：{Math.round(selectedMethod.confidence * 100)}%
                </Tag>
              </Space>
            }
          >
            <Row gutter={[24, 24]}>
              <Col span={24}>
                <Alert 
                  message={selectedMethod.description} 
                  description={
                    <Typography.Paragraph style={{ margin: 0 }}>
                      该方法通过引入个体固定效应，可以控制不随时间变化的个体特征，从而有效地解决遗漏变量偏误问题。这种方法特别适用于研究个体内部的变化对因变量的影响，能够更准确地估计变量间的因果关系。
                    </Typography.Paragraph>
                  }
                  type="info" 
                  showIcon 
                />
              </Col>
              
              <Col span={12}>
                <Card size="small" title="方法优势" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.advantages.map((adv, i) => (
                      <li key={i}>{adv}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
              
              <Col span={12}>
                <Card size="small" title="注意事项" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.considerations.map((con, i) => (
                      <li key={i}>{con}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
              
              <Col span={12}>
                <Card size="small" title="基本假设" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.assumptions.map((assumption, i) => (
                      <li key={i}>{assumption}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
              
              <Col span={12}>
                <Card size="small" title="建议检验" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.testMethods.map((test, i) => (
                      <li key={i}>{test}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
              
              <Col span={24}>
                <Card 
                  size="small" 
                  title="模型公式" 
                  bordered={false}
                  bodyStyle={{ 
                    backgroundColor: '#f5f5f5',
                    padding: '16px',
                    borderRadius: '4px',
                    fontFamily: 'KaTeX_Math, Times New Roman, serif',
                    fontSize: '16px',
                    textAlign: 'center'
                  }}
                >
                  <Text code style={{ 
                    backgroundColor: 'transparent',
                    padding: '8px 16px',
                    border: 'none',
                    color: '#000000d9',
                    fontSize: '16px',
                    fontFamily: 'KaTeX_Math, Times New Roman, serif'
                  }}>
                    {selectedMethod.formula}
                  </Text>
                  <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
                    其中，Y_it 表示因变量，α_i 表示个体固定效应，X_it 表示自变量向量，β 表示待估计的系数向量，ε_it 表示随机误差项。
                  </div>
                </Card>
              </Col>
              
              <Col span={12}>
                <Card size="small" title="适用条件" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.suitableConditions.map((condition, i) => (
                      <li key={i}>{condition}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
              
              <Col span={12}>
                <Card size="small" title="适用场景" bordered={false}>
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {selectedMethod.suitableScenarios.map((scenario, i) => (
                      <li key={i}>{scenario}</li>
                    ))}
                  </ul>
                </Card>
              </Col>
            </Row>
          </Card>
        </Card>
      )}

      {/* 底部按钮 */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', mt: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={onPrev}
        >
          上一步
        </Button>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => onSave && onSave({
              preprocessConfig,
              selectedVars: selectedVariables.map(v => v.name),
              processedData,
              dataPreview,
              dataSource
            })}
        >
          保存
        </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={triggerEmpiricalAnalysis}
            disabled={!selectedMethod || selectedVariables.length === 0}
          >
            开始实证分析
          </Button>
      </Box>
    </Box>
    </div>
  );
};

export default DataAnalysisEditor; 