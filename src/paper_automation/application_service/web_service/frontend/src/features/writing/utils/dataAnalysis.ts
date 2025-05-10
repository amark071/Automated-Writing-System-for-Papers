import * as XLSX from 'xlsx';

export interface DataStats {
  count: number;
  mean: number;
  std: number;
  min: number;
  max: number;
  missing: number;
}

export interface VariableInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'date' | 'dummy';
  stats: DataStats;
}

export interface ProcessedData {
  rawData: any[];
  variables: VariableInfo[];
  dataType: 'panel' | 'cross_section' | 'time_series' | null;
  confidence: number;
}

// 文件解析函数
export const parseFile = async (file: File): Promise<ProcessedData> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        let data: any[] = [];
        
        if (file.name.endsWith('.csv')) {
          const text = e.target?.result as string;
          data = parseCSV(text);
        } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
          const buffer = e.target?.result as ArrayBuffer;
          data = parseExcel(buffer);
        }

        const processedData = preprocessData(data);
        const dataType = detectDataType(processedData);
        const variables = analyzeVariables(processedData);

        resolve({
          rawData: processedData,
          variables,
          ...dataType
        });
      } catch (error: any) {
        reject(new Error('文件解析失败：' + error.message));
      }
    };

    reader.onerror = () => {
      reject(new Error('文件读取失败'));
    };

    if (file.name.endsWith('.csv')) {
      reader.readAsText(file);
    } else {
      reader.readAsArrayBuffer(file);
    }
  });
};

// CSV解析
const parseCSV = (text: string): any[] => {
  const lines = text.split('\\n');
  const headers = lines[0].split(',').map(h => h.trim());
  
  return lines.slice(1)
    .filter(line => line.trim())
    .map(line => {
      const values = line.split(',');
      return headers.reduce((obj, header, index) => {
        obj[header] = values[index]?.trim() ?? '';
        return obj;
      }, {} as any);
    });
};

// Excel解析
const parseExcel = (buffer: ArrayBuffer): any[] => {
  const workbook = XLSX.read(buffer, { type: 'array' });
  const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
  return XLSX.utils.sheet_to_json(firstSheet);
};

// 数据预处理
export const preprocessData = (data: any[]): any[] => {
  if (!data.length) return [];

  return data.map(row => {
    const processed = { ...row };
    Object.keys(processed).forEach(key => {
      const value = processed[key];
      // 处理缺失值
      if (value === '' || value === undefined || value === null) {
        processed[key] = null;
      }
      // 尝试转换数值
      else if (!isNaN(value)) {
        processed[key] = Number(value);
      }
      // 尝试转换日期
      else if (!isNaN(Date.parse(value))) {
        processed[key] = new Date(value);
      }
    });
    return processed;
  });
};

// 检测数据类型
export const detectDataType = (data: any[]): { dataType: 'panel' | 'cross_section' | 'time_series' | null, confidence: number } => {
  if (!data.length) return { dataType: null, confidence: 0 };

  const hasTimeVariable = Object.keys(data[0]).some(key => 
    key.toLowerCase().includes('year') || 
    key.toLowerCase().includes('date') ||
    key.toLowerCase().includes('time')
  );

  const hasEntityVariable = Object.keys(data[0]).some(key =>
    key.toLowerCase().includes('id') ||
    key.toLowerCase().includes('entity') ||
    key.toLowerCase().includes('firm') ||
    key.toLowerCase().includes('company') ||
    key.toLowerCase().includes('province') ||
    key.toLowerCase().includes('city')
  );

  if (hasTimeVariable && hasEntityVariable) {
    return { dataType: 'panel', confidence: 0.9 };
  } else if (hasTimeVariable) {
    return { dataType: 'time_series', confidence: 0.8 };
  } else {
    return { dataType: 'cross_section', confidence: 0.7 };
  }
};

// 分析变量
export const analyzeVariables = (data: any[]): VariableInfo[] => {
  if (!data.length) return [];

  const variables: VariableInfo[] = [];
  const columns = Object.keys(data[0]);

  columns.forEach(column => {
    const values = data.map(row => row[column]).filter(v => v !== null);
    const numericValues = values.filter(v => !isNaN(v)).map(Number);
    
    let type: 'numeric' | 'categorical' | 'date' | 'dummy' = 'categorical';
    
    // 检查是否为虚拟变量（只包含0和1的数值变量）
    if (numericValues.length === values.length && 
        numericValues.every(v => v === 0 || v === 1)) {
      type = 'dummy';
    }
    // 检查是否为普通数值变量
    else if (numericValues.length / values.length > 0.8) {
      type = 'numeric';
    }
    // 检查是否为日期
    else if (values.every(v => !isNaN(Date.parse(v)))) {
      type = 'date';
    }

    const stats: DataStats = {
      count: values.length,
      mean: (type === 'numeric' || type === 'dummy') ? calculateMean(numericValues) : 0,
      std: (type === 'numeric' || type === 'dummy') ? calculateStd(numericValues) : 0,
      min: (type === 'numeric' || type === 'dummy') ? Math.min(...numericValues) : 0,
      max: (type === 'numeric' || type === 'dummy') ? Math.max(...numericValues) : 0,
      missing: data.length - values.length
    };

    variables.push({
      name: column,
      type,
      stats
    });
  });

  return variables;
};

// 计算均值
const calculateMean = (values: number[]): number => {
  if (!values.length) return 0;
  return values.reduce((sum, val) => sum + val, 0) / values.length;
};

// 计算标准差
const calculateStd = (values: number[]): number => {
  if (!values.length) return 0;
  const mean = calculateMean(values);
  const squareDiffs = values.map(value => Math.pow(value - mean, 2));
  return Math.sqrt(calculateMean(squareDiffs));
};

// 生成相关性矩阵
export const generateCorrelationMatrix = (data: any[], variables: string[]): number[][] => {
  const matrix: number[][] = [];
  
  for (let i = 0; i < variables.length; i++) {
    matrix[i] = [];
    for (let j = 0; j < variables.length; j++) {
      const var1 = variables[i];
      const var2 = variables[j];
      
      if (i === j) {
        matrix[i][j] = 1;
      } else {
        const values1 = data.map(row => row[var1]).filter(v => v !== null && !isNaN(v));
        const values2 = data.map(row => row[var2]).filter(v => v !== null && !isNaN(v));
        matrix[i][j] = calculateCorrelation(values1, values2);
      }
    }
  }
  
  return matrix;
};

// 计算相关系数
const calculateCorrelation = (values1: number[], values2: number[]): number => {
  if (values1.length !== values2.length || !values1.length) return 0;
  
  const mean1 = calculateMean(values1);
  const mean2 = calculateMean(values2);
  
  let numerator = 0;
  let denominator1 = 0;
  let denominator2 = 0;
  
  for (let i = 0; i < values1.length; i++) {
    const diff1 = values1[i] - mean1;
    const diff2 = values2[i] - mean2;
    numerator += diff1 * diff2;
    denominator1 += diff1 * diff1;
    denominator2 += diff2 * diff2;
  }
  
  if (denominator1 === 0 || denominator2 === 0) return 0;
  return numerator / Math.sqrt(denominator1 * denominator2);
};

// 数据预处理配置接口
export interface PreprocessConfig {
  missingValue: {
    method: 'mean' | 'median' | 'mode' | 'remove' | 'none';
    threshold?: number; // 缺失值比例阈值，超过则删除该变量
  };
  outlier: {
    method: 'zscore' | 'iqr' | 'none';
    threshold: number; // Z分数阈值或IQR倍数
  };
  standardization: {
    method: 'zscore' | 'minmax' | 'none';
  };
}

// 数据预处理函数
export const preprocessDataAdvanced = (
  data: any[],
  variables: VariableInfo[],
  config: PreprocessConfig
): { data: any[], summary: PreprocessSummary } => {
  let processedData = [...data];
  const summary: PreprocessSummary = {
    missingValues: {},
    outliers: {},
    standardization: {}
  };

  // 处理缺失值
  if (config.missingValue.method !== 'none') {
    const result = handleMissingValues(processedData, variables, config.missingValue);
    processedData = result.data;
    summary.missingValues = result.summary;
  }

  // 处理异常值
  if (config.outlier.method !== 'none') {
    const result = handleOutliers(processedData, variables, config.outlier);
    processedData = result.data;
    summary.outliers = result.summary;
  }

  // 数据标准化
  if (config.standardization.method !== 'none') {
    const result = standardizeData(processedData, variables, config.standardization);
    processedData = result.data;
    summary.standardization = result.summary;
  }

  return { data: processedData, summary };
};

// 处理缺失值
const handleMissingValues = (
  data: any[],
  variables: VariableInfo[],
  config: PreprocessConfig['missingValue']
) => {
  let processedData = [...data];
  const summary: { [key: string]: { method: string; count: number } } = {};

  variables.forEach(variable => {
    if (variable.type !== 'numeric') return;

    const missingCount = processedData.filter(row => row[variable.name] === null).length;
    const missingRatio = missingCount / processedData.length;

    if (missingRatio > (config.threshold || 0.5)) {
      summary[variable.name] = { method: 'skip', count: missingCount };
      return;
    }

    let method = config.method;
    let count = 0;

    switch (method) {
      case 'mean': {
        const mean = calculateMean(processedData.filter(row => row[variable.name] !== null).map(row => row[variable.name]));
        processedData = processedData.map(row => {
          if (row[variable.name] === null) {
            count++;
            return { ...row, [variable.name]: mean };
          }
          return row;
        });
        break;
      }
      case 'median': {
        const median = calculateMedian(processedData.filter(row => row[variable.name] !== null).map(row => row[variable.name]));
        processedData = processedData.map(row => {
          if (row[variable.name] === null) {
            count++;
            return { ...row, [variable.name]: median };
          }
          return row;
        });
        break;
      }
      case 'remove': {
        const newData = processedData.filter(row => row[variable.name] !== null);
        count = processedData.length - newData.length;
        processedData = newData;
        break;
      }
      default:
        method = 'none';
    }

    if (method !== 'none') {
      summary[variable.name] = { method, count };
    }
  });

  return { data: processedData, summary };
};

// 处理异常值
const handleOutliers = (
  data: any[],
  variables: VariableInfo[],
  config: PreprocessConfig['outlier']
) => {
  const summary: { [key: string]: { method: string, count: number } } = {};
  const processedData = [...data];

  variables.forEach(variable => {
    if (variable.type === 'numeric') {
      const values = data.map(row => row[variable.name]).filter(v => v !== null);
      let outlierIndices: number[] = [];

      if (config.method === 'zscore') {
        outlierIndices = detectOutliersZScore(values, config.threshold);
      } else if (config.method === 'iqr') {
        outlierIndices = detectOutliersIQR(values, config.threshold);
      }

      // 将异常值替换为边界值
      outlierIndices.forEach(index => {
        const value = values[index];
        const mean = calculateMean(values);
        const std = calculateStd(values);
        processedData[index][variable.name] = value > mean ? 
          mean + config.threshold * std : 
          mean - config.threshold * std;
      });

      summary[variable.name] = {
        method: config.method,
        count: outlierIndices.length
      };
    }
  });

  return { data: processedData, summary };
};

// 数据标准化
const standardizeData = (
  data: any[],
  variables: VariableInfo[],
  config: PreprocessConfig['standardization']
) => {
  const summary: { [key: string]: { method: string, params: any } } = {};
  const processedData = [...data];

  variables.forEach(variable => {
    if (variable.type === 'numeric') {
      const values = data.map(row => row[variable.name]).filter(v => v !== null);

      if (config.method === 'zscore') {
        const mean = calculateMean(values);
        const std = calculateStd(values);
        processedData.forEach(row => {
          if (row[variable.name] !== null) {
            row[variable.name] = (row[variable.name] - mean) / std;
          }
        });
        summary[variable.name] = {
          method: 'zscore',
          params: { mean, std }
        };
      } else if (config.method === 'minmax') {
        const min = Math.min(...values);
        const max = Math.max(...values);
        processedData.forEach(row => {
          if (row[variable.name] !== null) {
            row[variable.name] = (row[variable.name] - min) / (max - min);
          }
        });
        summary[variable.name] = {
          method: 'minmax',
          params: { min, max }
        };
      }
    }
  });

  return { data: processedData, summary };
};

// 计算中位数
const calculateMedian = (values: number[]): number => {
  if (!values.length) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0
    ? (sorted[middle - 1] + sorted[middle]) / 2
    : sorted[middle];
};

// 检测异常值（Z分数法）
const detectOutliersZScore = (values: number[], threshold: number): number[] => {
  const mean = calculateMean(values);
  const std = calculateStd(values);
  return values
    .map((value, index) => ({ value, index }))
    .filter(({ value }) => Math.abs((value - mean) / std) > threshold)
    .map(({ index }) => index);
};

// 检测异常值（IQR法）
const detectOutliersIQR = (values: number[], threshold: number): number[] => {
  const sorted = [...values].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)];
  const q3 = sorted[Math.floor(sorted.length * 0.75)];
  const iqr = q3 - q1;
  const lowerBound = q1 - threshold * iqr;
  const upperBound = q3 + threshold * iqr;
  
  return values
    .map((value, index) => ({ value, index }))
    .filter(({ value }) => value < lowerBound || value > upperBound)
    .map(({ index }) => index);
};

export interface PreprocessSummary {
  missingValues: {
    [key: string]: {
      method: string;
      count: number;
    };
  };
  outliers: {
    [key: string]: {
      method: string;
      count: number;
    };
  };
  standardization: {
    [key: string]: {
      method: string;
      params: any;
    };
  };
} 