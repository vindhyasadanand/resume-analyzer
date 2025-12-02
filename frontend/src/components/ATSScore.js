import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import './ATSScore.css';

function ATSScore({ atsData }) {
  if (!atsData) return null;

  const scoreData = [
    { name: 'Pass', value: atsData.score },
    { name: 'Issues', value: 100 - atsData.score }
  ];

  const COLORS = ['#4CAF50', '#FF6B6B'];

  const getScoreLabel = (score) => {
    if (score >= 80) return { label: 'ATS Friendly', color: '#4CAF50' };
    if (score >= 60) return { label: 'Needs Minor Fixes', color: '#FF9800' };
    return { label: 'Needs Major Fixes', color: '#f44336' };
  };

  const scoreInfo = getScoreLabel(atsData.score);

  return (
    <div className="ats-container">
      <h3 className="ats-title">🤖 ATS Compatibility Score</h3>
      
      <div className="ats-content">
        <div className="ats-chart">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={scoreData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                dataKey="value"
                startAngle={90}
                endAngle={-270}
              >
                {scoreData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="ats-score-overlay">
            <div className="ats-score-value" style={{ color: scoreInfo.color }}>
              {atsData.score}%
            </div>
            <div className="ats-score-label" style={{ color: scoreInfo.color }}>
              {scoreInfo.label}
            </div>
          </div>
        </div>

        <div className="ats-details">
          {atsData.issues && atsData.issues.length > 0 && (
            <div className="ats-issues">
              <h4>⚠️ Issues Found:</h4>
              <ul>
                {atsData.issues.map((issue, index) => (
                  <li key={index} className="ats-issue-item">
                    <span className="issue-icon">❌</span>
                    {issue}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {atsData.recommendations && atsData.recommendations.length > 0 && (
            <div className="ats-recommendations">
              <h4>💡 Recommendations:</h4>
              <ul>
                {atsData.recommendations.map((rec, index) => (
                  <li key={index} className="ats-rec-item">
                    <span className="rec-icon">✅</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ATSScore;
