export interface MethodRecommendation {
  name: string;
  description: string;
  advantages: string[];
  considerations: string[];
  assumptions: string[];
  testMethods: string[];
  formula: string;
  suitableConditions: string[];
  suitableScenarios: string[];
  confidence: number;
}

interface DataInfo {
  dataType: 'panel' | 'cross_section' | 'time_series';
  hasInstrumental: boolean;
  hasMediator: boolean;
  hasModerator: boolean;
  hasGroupVariable: boolean;
  hasTimeVariable: boolean;
  hasEntityVariable: boolean;
  sampleSize: number;
}

export const recommendMethodsByDataStructure = (dataInfo: DataInfo): MethodRecommendation[] => {
  const recommendations: MethodRecommendation[] = [];

  // 面板数据推荐
  if (dataInfo.dataType === 'panel') {
    // 固定效应模型
    recommendations.push({
      name: '固定效应模型',
      description: '控制不随时间变化的个体特征，适用于研究个体内部的变化',
      advantages: [
        '控制不可观测的个体固定效应',
        '减少遗漏变量偏误',
        '适用于大样本面板数据'
      ],
      considerations: [
        '无法估计不随时间变化的变量系数',
        '需要足够的时间维度变异'
      ],
      assumptions: [
        '严格外生性',
        '误差项同方差性',
        '误差项无序列相关'
      ],
      testMethods: [
        'Hausman检验',
        'F检验',
        '异方差检验'
      ],
      formula: 'Y_it = α_i + X_it′β + ε_it',
      suitableConditions: [
        '个体效应与解释变量相关',
        '样本量充足',
        '时间跨度适中'
      ],
      suitableScenarios: [
        '公司金融研究',
        '产业经济分析',
        '区域经济研究'
      ],
      confidence: 0.9
    });

    // 随机效应模型
    recommendations.push({
      name: '随机效应模型',
      description: '假设个体效应为随机变量，适用于研究个体间的差异',
      advantages: [
        '可以估计不随时间变化的变量系数',
        '效率更高（如果假设成立）'
      ],
      considerations: [
        '需要个体效应与解释变量不相关的假设',
        '可能存在内生性问题'
      ],
      assumptions: [
        '个体效应与解释变量不相关',
        '误差项同方差性',
        '误差项无序列相关'
      ],
      testMethods: [
        'Hausman检验',
        'Breusch-Pagan LM检验'
      ],
      formula: 'Y_it = α + X_it′β + (u_i + ε_it)',
      suitableConditions: [
        '个体效应与解释变量不相关',
        '样本是总体的随机抽样'
      ],
      suitableScenarios: [
        '宏观经济研究',
        '人口统计分析',
        '社会调查研究'
      ],
      confidence: 0.85
    });
  }

  // 截面数据推荐
  if (dataInfo.dataType === 'cross_section') {
    // OLS
    recommendations.push({
      name: '普通最小二乘法（OLS）',
      description: '最基础的回归方法，适用于基本的线性关系分析',
      advantages: [
        '计算简单',
        '结果易于解释',
        '在古典假设下是最佳线性无偏估计量'
      ],
      considerations: [
        '可能存在内生性问题',
        '需要满足严格的古典假设'
      ],
      assumptions: [
        '线性关系',
        '误差项独立同分布',
        '解释变量与误差项不相关'
      ],
      testMethods: [
        '异方差检验',
        '序列相关检验',
        '正态性检验'
      ],
      formula: 'Y = Xβ + ε',
      suitableConditions: [
        '无严重内生性问题',
        '误差项满足古典假设'
      ],
      suitableScenarios: [
        '简单的因果关系分析',
        '预测模型构建',
        '相关性研究'
      ],
      confidence: 0.8
    });

    // 2SLS
    if (dataInfo.hasInstrumental) {
      recommendations.push({
        name: '两阶段最小二乘法（2SLS）',
        description: '处理内生性问题的常用方法，通过工具变量进行估计',
        advantages: [
          '可以处理内生性问题',
          '得到一致估计量'
        ],
        considerations: [
          '需要有效的工具变量',
          '弱工具变量问题'
        ],
        assumptions: [
          '工具变量的相关性',
          '工具变量的外生性',
          '排他性假设'
        ],
        testMethods: [
          '过度识别检验',
          '弱工具变量检验',
          'Hausman内生性检验'
        ],
        formula: '第一阶段：X = Zπ + v\n第二阶段：Y = X̂β + ε',
        suitableConditions: [
          '存在内生性问题',
          '有合适的工具变量'
        ],
        suitableScenarios: [
          '政策效果评估',
          '供需关系研究',
          '因果推断分析'
        ],
        confidence: 0.85
      });
    }
  }

  // 时间序列推荐
  if (dataInfo.dataType === 'time_series') {
    recommendations.push({
      name: '时间序列分析',
      description: '适用于研究变量随时间变化的模式和关系',
      advantages: [
        '可以捕捉时间趋势',
        '处理序列相关',
        '进行预测'
      ],
      considerations: [
        '需要足够长的时间序列',
        '可能存在单位根问题'
      ],
      assumptions: [
        '平稳性（或可转化为平稳）',
        '无序列相关',
        '误差项同方差性'
      ],
      testMethods: [
        '单位根检验',
        '协整检验',
        'Granger因果检验'
      ],
      formula: '取决于具体模型（AR、MA、ARIMA等）',
      suitableConditions: [
        '时间序列数据',
        '关注时间动态变化'
      ],
      suitableScenarios: [
        '经济周期研究',
        '金融市场分析',
        '预测研究'
      ],
      confidence: 0.85
    });
  }

  return recommendations;
}; 