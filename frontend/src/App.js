import React, { useState } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import JobDescriptionInput from './components/JobDescriptionInput';
import Results from './components/Results';
import JobComparison from './components/JobComparison';
import './App.css';

// Replace with your API Gateway endpoint after deployment
const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT || 'YOUR_API_GATEWAY_ENDPOINT';

function App() {
  const [step, setStep] = useState(1);
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeKey, setResumeKey] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [atsData, setAtsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileSelect = (file) => {
    setResumeFile(file);
    setError('');
  };

  const uploadResume = async () => {
    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Step 1: Get presigned URL
      const uploadResponse = await axios.post(`${API_ENDPOINT}/upload`, {
        filename: resumeFile.name,
        fileType: resumeFile.type || 'application/pdf'
      });

      const { upload_url, key } = uploadResponse.data;

      // Step 2: Upload file to S3
      await axios.put(upload_url, resumeFile, {
        headers: {
          'Content-Type': resumeFile.type
        }
      });

      setResumeKey(key);
      setStep(2);
    } catch (err) {
      console.error('Upload error:', err);
      console.error('Error details:', err.response?.data);
      console.error('Error status:', err.response?.status);
      setError(`Failed to upload resume: ${err.response?.status || err.message}. Check console for details.`);
    } finally {
      setLoading(false);
    }
  };

  const analyzeResume = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_ENDPOINT}/analyze`, {
        resume_key: resumeKey,
        job_description: jobDescription
      });

      setResults(response.data.results);
      setAtsData(response.data.ats_score || null);
      setStep(3);
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const startOver = () => {
    setStep(1);
    setResumeFile(null);
    setResumeKey('');
    setJobDescription('');
    setResults(null);
    setAtsData(null);
    setError('');
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🎯 Resume Analyzer</h1>
          <p>Analyze resume compatibility with job descriptions using AWS Serverless</p>
        </header>

        {/* Progress Steps */}
        <div className="progress-steps">
          <div className={`step ${step >= 1 ? 'active' : ''}`}>
            <div className="step-number">1</div>
            <div className="step-label">Upload Resume</div>
          </div>
          <div className={`step ${step >= 2 ? 'active' : ''}`}>
            <div className="step-number">2</div>
            <div className="step-label">Job Description</div>
          </div>
          <div className={`step ${step >= 3 ? 'active' : ''}`}>
            <div className="step-number">3</div>
            <div className="step-label">Results</div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
          </div>
        )}

        {/* Step 1: Upload Resume */}
        {step === 1 && (
          <div className="step-content">
            <FileUpload 
              onFileSelect={handleFileSelect}
              selectedFile={resumeFile}
            />
            <button
              className="btn btn-primary"
              onClick={uploadResume}
              disabled={!resumeFile || loading}
            >
              {loading ? 'Uploading...' : 'Upload & Continue'}
            </button>
          </div>
        )}

        {/* Step 2: Job Description */}
        {step === 2 && (
          <div className="step-content">
            <JobDescriptionInput
              value={jobDescription}
              onChange={setJobDescription}
            />
            <div className="button-group">
              <button
                className="btn btn-secondary"
                onClick={() => setStep(1)}
                disabled={loading}
              >
                Back
              </button>
              <button
                className="btn btn-primary"
                onClick={analyzeResume}
                disabled={!jobDescription.trim() || loading}
              >
                {loading ? 'Analyzing...' : 'Analyze Resume'}
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Results */}
        {step === 3 && results && (
          <div className="step-content">
            <Results 
              results={results} 
              atsData={atsData} 
              resumeKey={resumeKey}
              jobDescription={jobDescription}
            />
            
            {/* Job Comparison Section */}
            <JobComparison resumeFile={resumeFile} />
            
            <button
              className="btn btn-primary"
              onClick={startOver}
            >
              Analyze Another Resume
            </button>
          </div>
        )}

        {/* Footer */}
        <footer className="footer">
          <p>Built with AWS Lambda, S3, DynamoDB & API Gateway</p>
          <p className="team">Team 20: Keyur Modi, Naveen John, Vindhya Hegde</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
