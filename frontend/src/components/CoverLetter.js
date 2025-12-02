import React, { useState } from 'react';
import './CoverLetter.css';

function CoverLetter({ coverLetter, onClose }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(coverLetter.full_text || '');
  const [copied, setCopied] = useState(false);

  // Handle copy to clipboard
  const handleCopy = () => {
    const today = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    const formattedLetter = `${today}

Dear Hiring Manager,

${isEditing ? editedText : coverLetter.full_text}

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.

Sincerely,
[Your Name]`;

    navigator.clipboard.writeText(formattedLetter);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Handle download as text file
  const handleDownload = () => {
    const today = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    const formattedLetter = `${today}

Dear Hiring Manager,

${isEditing ? editedText : coverLetter.full_text}

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.

Sincerely,
[Your Name]`;

    const blob = new Blob([formattedLetter], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cover_letter.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Toggle edit mode
  const handleEditToggle = () => {
    if (isEditing) {
      setEditedText(editedText);
    }
    setIsEditing(!isEditing);
  };

  return (
    <div className="cover-letter-modal">
      <div className="cover-letter-container">
        <div className="cover-letter-header">
          <h2>🎯 Your Personalized Cover Letter</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="cover-letter-content">
          <div className="letter-date">
            {new Date().toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </div>

          <div className="letter-greeting">
            Dear Hiring Manager,
          </div>

          {isEditing ? (
            <textarea
              className="letter-editor"
              value={editedText}
              onChange={(e) => setEditedText(e.target.value)}
              rows={15}
            />
          ) : (
            <div className="letter-body">
              {coverLetter.opening && (
                <div className="letter-paragraph">
                  {coverLetter.opening}
                </div>
              )}

              {coverLetter.skills && (
                <div className="letter-paragraph">
                  {coverLetter.skills}
                </div>
              )}

              {coverLetter.experience && (
                <div className="letter-paragraph">
                  {coverLetter.experience}
                </div>
              )}

              {coverLetter.education && (
                <div className="letter-paragraph">
                  {coverLetter.education}
                </div>
              )}

              {coverLetter.closing && (
                <div className="letter-paragraph">
                  {coverLetter.closing}
                </div>
              )}
            </div>
          )}

          <div className="letter-closing">
            <p>Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.</p>
            <p className="signature">Sincerely,<br />[Your Name]</p>
          </div>
        </div>

        <div className="cover-letter-actions">
          <button 
            className="action-button edit-button"
            onClick={handleEditToggle}
          >
            {isEditing ? '✓ Save Edit' : '✏️ Edit'}
          </button>
          <button 
            className="action-button copy-button"
            onClick={handleCopy}
          >
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button 
            className="action-button download-button"
            onClick={handleDownload}
          >
            💾 Download
          </button>
        </div>

        <div className="cover-letter-tip">
          <strong>💡 Pro Tip:</strong> Customize the letter with specific details about the company and position. Replace [Your Name] with your actual name before sending.
        </div>
      </div>
    </div>
  );
}

export default CoverLetter;
