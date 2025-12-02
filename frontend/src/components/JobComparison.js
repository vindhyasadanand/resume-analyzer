import React, { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import './JobComparison.css';

const API_BASE_URL = 'https://s0ogqkfqaf.execute-api.us-east-1.amazonaws.com';

function JobComparison({ resumeFile }) {
  const [jobDescriptions, setJobDescriptions] = useState(['', '', '']);
  const [jobTitles, setJobTitles] = useState(['Job 1', 'Job 2', 'Job 3']);
  const [loading, setLoading] = useState(false);
  const [comparisonResults, setComparisonResults] = useState(null);
  const [error, setError] = useState('');

  const handleJobDescriptionChange = (index, value) => {
    const newDescriptions = [...jobDescriptions];
    newDescriptions[index] = value;
    setJobDescriptions(newDescriptions);
  };

  const handleJobTitleChange = (index, value) => {
    const newTitles = [...jobTitles];
    newTitles[index] = value;
    setJobTitles(newTitles);
  };

  const addJobField = () => {
    setJobDescriptions([...jobDescriptions, '']);
    setJobTitles([...jobTitles, `Job ${jobDescriptions.length + 1}`]);
  };

  const removeJobField = (index) => {
    if (jobDescriptions.length > 1) {
      const newDescriptions = jobDescriptions.filter((_, i) => i !== index);
      const newTitles = jobTitles.filter((_, i) => i !== index);
      setJobDescriptions(newDescriptions);
      setJobTitles(newTitles);
    }
  };

  const handleCompare = async () => {
    if (!resumeFile) {
      setError('Please upload a resume first');
      return;
    }

    const validJobs = jobDescriptions.filter(desc => desc.trim().length > 0);
    if (validJobs.length < 2) {
      setError('Please enter at least 2 job descriptions to compare');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Step 1: Upload resume to S3 (if not already uploaded)
      const uploadResponse = await axios.post(`${API_BASE_URL}/upload`, {
        filename: resumeFile.name,
        fileType: resumeFile.type || 'application/pdf'
      });

      const { upload_url, key } = uploadResponse.data;

      await axios.put(upload_url, resumeFile, {
        headers: {
          'Content-Type': resumeFile.type
        }
      });

      // Step 2: Prepare jobs data with titles
      const jobs = jobDescriptions
        .map((desc, index) => ({
          title: jobTitles[index],
          description: desc
        }))
        .filter(job => job.description.trim().length > 0);

      // Step 3: Call batch-compare endpoint
      const response = await axios.post(`${API_BASE_URL}/batch-compare`, {
        resume_key: key,
        jobs: jobs
      });

      setComparisonResults(response.data.results);
    } catch (err) {
      console.error('Comparison error:', err);
      setError(err.response?.data?.error || 'Failed to compare jobs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getColorByScore = (score) => {
    if (score >= 75) return '#4CAF50';  // Dark Green - Excellent
    if (score >= 55) return '#8BC34A';  // Light Green - Good
    if (score >= 40) return '#FF9800';  // Orange - Fair
    return '#f44336';                    // Red - Poor
  };

  return (
    <div className="job-comparison-container">
      <h2>🎯 Multiple Job Comparison</h2>
      <p className="description">Compare your resume against multiple job descriptions to find the best match</p>

      <div className="job-inputs">
        {jobDescriptions.map((desc, index) => (
          <div key={index} className="job-input-group">
            <div className="job-header">
              <input
                type="text"
                placeholder={`Job Title ${index + 1}`}
                value={jobTitles[index]}
                onChange={(e) => handleJobTitleChange(index, e.target.value)}
                className="job-title-input"
              />
              {jobDescriptions.length > 1 && (
                <button
                  onClick={() => removeJobField(index)}
                  className="remove-job-btn"
                  title="Remove this job"
                >
                  ✕
                </button>
              )}
            </div>
            <textarea
              placeholder={`Enter job description ${index + 1}...`}
              value={desc}
              onChange={(e) => handleJobDescriptionChange(index, e.target.value)}
              rows="6"
              className="job-description-input"
            />
          </div>
        ))}
      </div>

      <div className="comparison-actions">
        <button onClick={addJobField} className="add-job-btn">
          ➕ Add Another Job
        </button>
        <button
          onClick={handleCompare}
          disabled={loading || !resumeFile}
          className="compare-btn"
        >
          {loading ? 'Comparing...' : 'Compare All Jobs'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {comparisonResults && (
        <div className="comparison-results">
          <h3>📊 Comparison Results</h3>
          
          {/* Bar Chart */}
          <div className="comparison-chart">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={comparisonResults}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="title" />
                <YAxis domain={[0, 100]} />
                <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                  {comparisonResults.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getColorByScore(entry.score)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Ranking Table */}
          <div className="ranking-table">
            <h4>🏆 Job Rankings</h4>
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Job Title</th>
                  <th>Match Score</th>
                  <th>Skills Match</th>
                  <th>Recommendation</th>
                </tr>
              </thead>
              <tbody>
                {comparisonResults
                  .sort((a, b) => b.score - a.score)
                  .map((job, index) => (
                    <tr key={index} className={index === 0 ? 'best-match' : ''}>
                      <td className="rank">
                        {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                      </td>
                      <td className="job-title">{job.title}</td>
                      <td className="score">
                        <span
                          className="score-badge"
                          style={{ backgroundColor: getColorByScore(job.score) }}
                        >
                          {job.score.toFixed(1)}%
                        </span>
                      </td>
                      <td className="skills">
                        {job.matched_skills}
                      </td>
                      <td className="recommendation">
                        {job.score >= 75
                          ? '🎯 Excellent match! Apply with confidence'
                          : job.score >= 55
                          ? '✅ Good match. Consider applying'
                          : job.score >= 40
                          ? '⚠️ Fair match. Skill development recommended'
                          : '❌ Significant skill gaps. Needs preparation'}
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>

          {/* Top Match Details */}
          {comparisonResults.length > 0 && (
            <div className="top-match-details">
              <h4>🎯 Best Match: {comparisonResults.sort((a, b) => b.score - a.score)[0].title}</h4>
              <div className="top-match-details">
                <div className="insight-card">
                  <span className="insight-icon">✅</span>
                  <div>
                    <strong>Strengths</strong>
                    <p>
                      {(() => {
                        const topJob = comparisonResults.sort((a, b) => b.score - a.score)[0];
                        const strengths = topJob.strengths;
                        if (Array.isArray(strengths) && strengths.length > 0) {
                          return strengths.join('. ') + '.';
                        }
                        return strengths || 'Strong alignment with job requirements';
                      })()}
                    </p>
                  </div>
                </div>
                <div className="insight-card">
                  <span className="insight-icon">💡</span>
                  <div>
                    <strong>Improvement Tips</strong>
                    <p>
                      {(() => {
                        const topJob = comparisonResults.sort((a, b) => b.score - a.score)[0];
                        const improvements = topJob.improvements;
                        if (Array.isArray(improvements) && improvements.length > 0) {
                          return improvements.join('. ') + '.';
                        }
                        return improvements || 'Consider highlighting more relevant experience';
                      })()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default JobComparison;
