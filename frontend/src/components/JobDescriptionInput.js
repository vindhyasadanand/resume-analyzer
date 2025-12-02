import React from 'react';
import './JobDescriptionInput.css';

function JobDescriptionInput({ value, onChange }) {
  return (
    <div className="job-description-container">
      <label htmlFor="job-description" className="input-label">
        📋 Job Description
      </label>
      <p className="input-hint">
        Paste the job description to compare with the uploaded resume
      </p>
      <textarea
        id="job-description"
        className="job-description-textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the complete job description here, including required skills, qualifications, and responsibilities..."
        rows={12}
      />
      <div className="char-count">
        {value.length} characters
      </div>
    </div>
  );
}

export default JobDescriptionInput;
