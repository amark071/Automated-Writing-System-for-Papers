import React from 'react';
import {
  Card,
  Typography,
  Table,
  Space,
  Alert,
  Tag,
  Row,
  Col,
  Tooltip,
  Empty,
  Divider,
} from 'antd';
import { Button, Box } from '@mui/material';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

interface RegressionResult {
  variable: string;
  coefficient: number;
  standardError: number;
  tStat: number;
  pValue: number;
  significance: string;
}

interface MediationResult extends RegressionResult {
  effectType: 'direct' | 'indirect' | 'total';
}

interface ModerationResult extends RegressionResult {
  interactionTerm: string;
}

interface DiagnosticTest {
  testName: string;
  result: string;
  suggestion: string;
  status: 'success' | 'warning' | 'error';
}

interface RobustnessTest {
  testName: string;
  description: string;
  result: string;
  conclusion: string;
}

interface EmpiricalResultsProps {
  sectionId: string;
  regressionResults: RegressionResult[];
  heterogeneityResults: RegressionResult[];
  mediationResults?: MediationResult[];
  moderationResults?: ModerationResult[];
  diagnosticTests: DiagnosticTest[];
  robustnessTests: RobustnessTest[];
  selectedMethods: string[];
  onRunRobustnessTest?: (type: string) => void;
  onSave?: () => void;
  onPrev?: () => void;
  onNext?: () => void;
}

export const EmpiricalResults: React.FC<EmpiricalResultsProps> = ({
  regressionResults,
  heterogeneityResults,
  mediationResults = [],
  moderationResults = [],
  diagnosticTests,
  robustnessTests,
  selectedMethods,
  onRunRobustnessTest,
  onSave,
  onPrev,
  onNext,
}) => {
  const renderRegressionResults = () => {
    const getSignificanceLevel = (significance: string) => {
      switch (significance) {
        case '***':
          return '1%';
        case '**':
          return '5%';
        case '*':
          return '10%';
        default:
          return '不显著';
      }
    };

    const r2Value = regressionResults.find(r => r.variable === 'R²')?.coefficient.toFixed(4);

    return (
      <div style={{ marginBottom: '4rem' }}>
        <Title level={4}>1. 基准回归结果</Title>
        <Typography.Text style={{ fontSize: '16px', display: 'block', marginTop: '1rem', marginBottom: '2rem' }}>
          表1报告了基准回归的结果。从回归结果可以看出，{regressionResults.map(result => {
            if (result.variable === '样本量' || result.variable === 'R²') return '';
            const significanceLevel = getSignificanceLevel(result.significance);
            const direction = result.coefficient > 0 ? '正向' : '负向';
            return `${result.variable}对因变量具有${direction}影响(${result.coefficient.toFixed(4)})，在${significanceLevel}水平上显著；`;
          }).join('')}模型的R²为${r2Value}，表明模型具有一定的解释力。
        </Typography.Text>
        <div style={{ overflowX: 'auto', marginTop: '2rem' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
            <thead>
              <tr>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left', width: '200px' }}>变量</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>模型(1)</th>
              </tr>
            </thead>
            <tbody>
              {regressionResults.map((result, index) => (
                <tr key={index}>
                  <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>
                    {result.variable}
                  </td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>
                    <div>{result.coefficient?.toFixed(4) ?? '-'}{result.significance}</div>
                    <div style={{ color: '#666', fontSize: '0.9em' }}>
                      ({result.standardError?.toFixed(4) ?? '-'})
                    </div>
                  </td>
                </tr>
              ))}
              <tr>
                <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>样本量</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>5120</td>
              </tr>
              <tr>
                <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>R²</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>0.0213</td>
              </tr>
            </tbody>
          </table>
        </div>
        <Paragraph type="secondary" style={{ marginTop: '1rem', fontSize: '0.9em' }}>
          注：括号内为标准误；*、**、*** 分别表示在10%、5%和1%的水平上显著。
        </Paragraph>
      </div>
    );
  };

  const renderMechanismAnalysis = () => {
    // 如果没有机制分析结果，返回空的提示
    if (!mediationResults?.length && !moderationResults?.length) {
      return (
        <div style={{ marginBottom: '4rem' }}>
          <Title level={4}>2. 机制分析</Title>
          <Empty
            description={
              <span>暂无机制分析结果</span>
            }
          />
        </div>
      );
    }

    return (
      <div style={{ marginBottom: '4rem' }}>
        <Title level={4}>2. 机制分析</Title>
        <Typography.Text style={{ fontSize: '16px', display: 'block', marginTop: '1rem', marginBottom: '2rem' }}>
          {mediationResults?.length > 0 && `中介效应分析结果表明，${mediationResults.map(result => {
            const significance = result.significance ? '显著' : '不显著';
            return `${result.variable}的中介效应为${result.coefficient.toFixed(4)}，在${result.significance}水平上统计${significance}；`;
          }).join('')}`}
          {moderationResults?.length > 0 && `调节效应分析结果表明，${moderationResults.map(result => {
            const significance = result.significance ? '显著' : '不显著';
            return `${result.variable}的调节效应为${result.coefficient.toFixed(4)}，在${result.significance}水平上统计${significance}；`;
          }).join('')}`}
        </Typography.Text>
        <div style={{ overflowX: 'auto', marginTop: '2rem' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
            <thead>
              <tr>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left', width: '200px' }}>变量</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>中介效应</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>调节效应</th>
              </tr>
            </thead>
            <tbody>
              {/* 这里添加机制分析的结果 */}
            </tbody>
          </table>
        </div>
        <Paragraph type="secondary" style={{ marginTop: '1rem', fontSize: '0.9em' }}>
          注：括号内为标准误；*、**、*** 分别表示在10%、5%和1%的水平上显著。
        </Paragraph>
      </div>
    );
  };

  const renderHeterogeneityResults = () => {
    // 如果没有异质性分析结果，返回空的提示
    if (!heterogeneityResults?.length) {
      return (
        <div style={{ marginBottom: '4rem' }}>
          <Title level={4}>3. 异质性分析</Title>
          <Empty
            description={
              <span>暂无异质性分析结果</span>
            }
          />
        </div>
      );
    }

    return (
      <div style={{ marginBottom: '4rem' }}>
        <Title level={4}>3. 异质性分析</Title>
        <Typography.Text style={{ fontSize: '16px', display: 'block', marginTop: '1rem', marginBottom: '2rem' }}>
          表3报告了分地区的异质性分析结果。从回归结果可以看出，{heterogeneityResults.filter(result => result.variable.includes('东部')).map(result => {
            const baseVar = result.variable.split('_')[0];
            const eastResult = heterogeneityResults.find(r => r.variable === `${baseVar}_东部`);
            const centralResult = heterogeneityResults.find(r => r.variable === `${baseVar}_中部`);
            const westResult = heterogeneityResults.find(r => r.variable === `${baseVar}_西部`);
            
            return `${baseVar}在东部地区的影响为${eastResult?.coefficient.toFixed(4)}，在中部地区的影响为${centralResult?.coefficient.toFixed(4)}，在西部地区的影响为${westResult?.coefficient.toFixed(4)}，表明存在明显的区域异质性；`;
          }).join('')}
        </Typography.Text>
        <div style={{ overflowX: 'auto', marginTop: '2rem' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
            <thead>
              <tr>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left', width: '200px' }}>变量</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>东部地区</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>中部地区</th>
                <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>西部地区</th>
              </tr>
            </thead>
            <tbody>
              {heterogeneityResults.filter(result => result.variable.includes('东部')).map((result, index) => {
                const baseVar = result.variable.split('_')[0];
                const eastResult = heterogeneityResults.find(r => r.variable === `${baseVar}_东部`);
                const centralResult = heterogeneityResults.find(r => r.variable === `${baseVar}_中部`);
                const westResult = heterogeneityResults.find(r => r.variable === `${baseVar}_西部`);
                
                return (
                  <tr key={index}>
                    <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>
                      {baseVar}
                    </td>
                    <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>
                      {eastResult && (
                        <>
                          <div>{eastResult.coefficient?.toFixed(4) ?? '-'}{eastResult.significance}</div>
                          <div style={{ color: '#666', fontSize: '0.9em' }}>
                            ({eastResult.standardError?.toFixed(4) ?? '-'})
                          </div>
                        </>
                      )}
                    </td>
                    <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>
                      {centralResult && (
                        <>
                          <div>{centralResult.coefficient?.toFixed(4) ?? '-'}{centralResult.significance}</div>
                          <div style={{ color: '#666', fontSize: '0.9em' }}>
                            ({centralResult.standardError?.toFixed(4) ?? '-'})
                          </div>
                        </>
                      )}
                    </td>
                    <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>
                      {westResult && (
                        <>
                          <div>{westResult.coefficient?.toFixed(4) ?? '-'}{westResult.significance}</div>
                          <div style={{ color: '#666', fontSize: '0.9em' }}>
                            ({westResult.standardError?.toFixed(4) ?? '-'})
                          </div>
                        </>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <Paragraph type="secondary" style={{ marginTop: '1rem', fontSize: '0.9em' }}>
          注：括号内为标准误；*、**、*** 分别表示在10%、5%和1%的水平上显著。
        </Paragraph>
      </div>
    );
  };

  const renderDiagnosticTests = () => (
    <div style={{ marginBottom: '4rem' }}>
      <Title level={4}>4. 稳健性检验</Title>
      <Title level={5} style={{ marginTop: '2rem' }}>4.1 基本诊断检验</Title>
      <Typography.Text style={{ fontSize: '16px', display: 'block', marginTop: '1rem' }}>
        为了确保研究结果的可靠性，本文进行了一系列诊断检验。
      </Typography.Text>
      <div style={{ overflowX: 'auto', marginTop: '2rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
          <thead>
            <tr>
              <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left', width: '200px' }}>检验项目</th>
              <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>统计量</th>
              <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>p值</th>
              <th style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>结论</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>White异方差检验</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>3526.1321</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>0.0000</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>存在异方差性</td>
            </tr>
            <tr>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>Jarque-Bera正态性检验</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>2329740.9338</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>0.0000</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>残差不服从正态分布</td>
            </tr>
            <tr>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>Ramsey RESET检验</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>1586.0929</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>0.0000</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>模型设定存在问题</td>
            </tr>
            <tr>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>VIF检验 (EC)</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>1.0597</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>-</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>多重共线性在可接受范围</td>
            </tr>
            <tr>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>VIF检验 (TC)</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>1.0597</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>-</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #f0f0f0' }}>多重共线性在可接受范围</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div style={{ marginTop: '2rem' }}>
        <Text strong>改进建议：</Text>
        <ol style={{ marginTop: '1rem', paddingLeft: '1.5rem' }}>
          <li>模型存在异方差问题，建议采用稳健标准误或GLS估计。</li>
          <li>残差不服从正态分布，可能需要考虑变量的非线性转换。</li>
          <li>模型设定存在问题，建议进行以下进一步检验：</li>
        </ol>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
          <Button variant="outlined">内生性检验</Button>
          <Button variant="outlined">工具变量估计</Button>
          <Button variant="outlined">面板固定效应</Button>
        </div>
      </div>
    </div>
  );

  const renderRobustnessTests = () => (
    <div style={{ marginBottom: '4rem' }}>
      <Title level={5}>4.2 稳健性检验方案</Title>
      <Typography.Text style={{ fontSize: '16px', display: 'block', marginTop: '1rem' }}>
        基于上述诊断结果，建议采用以下方案进行稳健性检验：
      </Typography.Text>
      <ol style={{ marginTop: '1rem', paddingLeft: '1.5rem' }}>
        <li>使用稳健标准误重新估计模型</li>
        <li>考虑加入年份固定效应和地区固定效应</li>
        <li>使用工具变量方法处理潜在的内生性问题</li>
        <li>考虑变量的非线性关系</li>
      </ol>
      <div style={{ marginTop: '2rem' }}>
          <Button
            variant="contained"
          color="primary"
          onClick={() => onRunRobustnessTest && onRunRobustnessTest('robust')}
          >
            执行稳健性检验
          </Button>
      </div>
    </div>
  );

  return (
    <div style={{ padding: '24px' }}>
      {renderRegressionResults()}
      <Divider style={{ margin: '3rem 0' }} />
      {renderMechanismAnalysis()}
      <Divider style={{ margin: '3rem 0' }} />
      {renderHeterogeneityResults()}
      <Divider style={{ margin: '3rem 0' }} />
      {renderDiagnosticTests()}
      <Divider style={{ margin: '3rem 0' }} />
      {renderRobustnessTests()}
      
      {/* 底部导航按钮 */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', mt: 4 }}>
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
            onClick={onSave}
          >
            保存
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={onNext}
          >
            下一步
          </Button>
        </Box>
      </Box>
    </div>
  );
};

export default EmpiricalResults; 