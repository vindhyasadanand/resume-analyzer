import React, { useState } from 'react';
import './LearningPath.css';

const COURSE_DATABASE = {
  // Programming Languages
  'python': [
    { title: 'Python for Everybody Specialization', platform: 'Coursera', url: 'https://www.coursera.org/specializations/python', level: 'Beginner' },
    { title: 'Complete Python Bootcamp', platform: 'Udemy', url: 'https://www.udemy.com/course/complete-python-bootcamp/', level: 'All Levels' }
  ],
  'javascript': [
    { title: 'JavaScript Algorithms and Data Structures', platform: 'freeCodeCamp', url: 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', level: 'All Levels' },
    { title: 'Modern JavaScript From The Beginning', platform: 'Udemy', url: 'https://www.udemy.com/course/modern-javascript-from-the-beginning/', level: 'All Levels' }
  ],
  'java': [
    { title: 'Java Programming and Software Engineering', platform: 'Coursera', url: 'https://www.coursera.org/specializations/java-programming', level: 'Beginner' },
    { title: 'Java Programming Masterclass', platform: 'Udemy', url: 'https://www.udemy.com/course/java-the-complete-java-developer-course/', level: 'All Levels' }
  ],
  'react': [
    { title: 'React - The Complete Guide', platform: 'Udemy', url: 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/', level: 'All Levels' },
    { title: 'Full-Stack Web Development with React', platform: 'Coursera', url: 'https://www.coursera.org/specializations/full-stack-react', level: 'Intermediate' }
  ],
  'node': [
    { title: 'The Complete Node.js Developer Course', platform: 'Udemy', url: 'https://www.udemy.com/course/the-complete-nodejs-developer-course-2/', level: 'All Levels' },
    { title: 'Server-side Development with NodeJS', platform: 'Coursera', url: 'https://www.coursera.org/learn/server-side-nodejs', level: 'Intermediate' }
  ],
  'android': [
    { title: 'The Complete Android Developer Course', platform: 'Udemy', url: 'https://www.udemy.com/course/complete-android-n-developer-course/', level: 'All Levels' },
    { title: 'Android App Development Specialization', platform: 'Coursera', url: 'https://www.coursera.org/specializations/android-app-development', level: 'Beginner' },
    { title: 'Advanced Android with Kotlin', platform: 'Google Developers', url: 'https://developer.android.com/courses', level: 'Advanced' }
  ],
  'kotlin': [
    { title: 'Kotlin for Java Developers', platform: 'Coursera', url: 'https://www.coursera.org/learn/kotlin-for-java-developers', level: 'Intermediate' },
    { title: 'Kotlin Programming: The Comprehensive Course', platform: 'Udemy', url: 'https://www.udemy.com/course/kotlin-course/', level: 'All Levels' }
  ],
  'sdk': [
    { title: 'Android SDK Platform Tools', platform: 'Android Developers', url: 'https://developer.android.com/studio/releases/platform-tools', level: 'All Levels' },
    { title: 'Mobile App Development', platform: 'Coursera', url: 'https://www.coursera.org/specializations/mobile-app-development', level: 'Intermediate' }
  ],
  'api': [
    { title: 'REST API Design, Development & Management', platform: 'Udemy', url: 'https://www.udemy.com/course/rest-api/', level: 'All Levels' },
    { title: 'APIs and Web Services', platform: 'Coursera', url: 'https://www.coursera.org/learn/web-services-api', level: 'Intermediate' }
  ],
  
  // Cloud & DevOps
  'aws': [
    { title: 'AWS Certified Solutions Architect', platform: 'Coursera', url: 'https://www.coursera.org/learn/aws-cloud-technical-essentials', level: 'Beginner' },
    { title: 'Ultimate AWS Certified Solutions Architect Associate', platform: 'Udemy', url: 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/', level: 'All Levels' }
  ],
  'docker': [
    { title: 'Docker and Kubernetes: The Complete Guide', platform: 'Udemy', url: 'https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/', level: 'All Levels' },
    { title: 'Introduction to Containers w/ Docker, Kubernetes', platform: 'Coursera', url: 'https://www.coursera.org/learn/ibm-containers-docker-kubernetes-openshift', level: 'Beginner' }
  ],
  'kubernetes': [
    { title: 'Kubernetes for the Absolute Beginners', platform: 'Udemy', url: 'https://www.udemy.com/course/learn-kubernetes/', level: 'Beginner' },
    { title: 'Getting Started with Google Kubernetes Engine', platform: 'Coursera', url: 'https://www.coursera.org/learn/google-kubernetes-engine', level: 'Intermediate' }
  ],
  
  // Data Science & ML
  'machine learning': [
    { title: 'Machine Learning Specialization', platform: 'Coursera', url: 'https://www.coursera.org/specializations/machine-learning-introduction', level: 'Beginner' },
    { title: 'Machine Learning A-Z', platform: 'Udemy', url: 'https://www.udemy.com/course/machinelearning/', level: 'All Levels' }
  ],
  'tensorflow': [
    { title: 'DeepLearning.AI TensorFlow Developer', platform: 'Coursera', url: 'https://www.coursera.org/professional-certificates/tensorflow-in-practice', level: 'Intermediate' },
    { title: 'TensorFlow 2.0 Complete Course', platform: 'Udemy', url: 'https://www.udemy.com/course/tensorflow-2/', level: 'All Levels' }
  ],
  'data analysis': [
    { title: 'Google Data Analytics Professional Certificate', platform: 'Coursera', url: 'https://www.coursera.org/professional-certificates/google-data-analytics', level: 'Beginner' },
    { title: 'The Data Science Course: Complete Data Science', platform: 'Udemy', url: 'https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/', level: 'All Levels' }
  ],
  
  // Databases
  'sql': [
    { title: 'SQL for Data Science', platform: 'Coursera', url: 'https://www.coursera.org/learn/sql-for-data-science', level: 'Beginner' },
    { title: 'The Complete SQL Bootcamp', platform: 'Udemy', url: 'https://www.udemy.com/course/the-complete-sql-bootcamp/', level: 'All Levels' }
  ],
  'mongodb': [
    { title: 'MongoDB - The Complete Developer Guide', platform: 'Udemy', url: 'https://www.udemy.com/course/mongodb-the-complete-developers-guide/', level: 'All Levels' },
    { title: 'MongoDB Basics', platform: 'MongoDB University', url: 'https://university.mongodb.com/', level: 'Beginner' }
  ],
  
  // Soft Skills
  'agile': [
    { title: 'Agile with Atlassian Jira', platform: 'Coursera', url: 'https://www.coursera.org/learn/agile-atlassian-jira', level: 'Beginner' },
    { title: 'Agile Crash Course: Agile Project Management', platform: 'Udemy', url: 'https://www.udemy.com/course/agile-crash-course/', level: 'All Levels' }
  ],
  'git': [
    { title: 'Version Control with Git', platform: 'Coursera', url: 'https://www.coursera.org/learn/version-control-with-git', level: 'Beginner' },
    { title: 'Git Complete: The definitive guide', platform: 'Udemy', url: 'https://www.udemy.com/course/git-complete/', level: 'All Levels' }
  ],
  'communication': [
    { title: 'Improving Communication Skills', platform: 'Coursera', url: 'https://www.coursera.org/learn/wharton-communication-skills', level: 'All Levels' },
    { title: 'Communication Skills Machine', platform: 'Udemy', url: 'https://www.udemy.com/course/communication-skills-training/', level: 'All Levels' }
  ]
};

function LearningPath({ missingSkills = [] }) {
  const [expandedSkill, setExpandedSkill] = useState(null);

  // Filter out generic/non-technical words - COMPREHENSIVE LIST
  const NON_TECHNICAL_WORDS = [
    // Generic action words
    'experience', 'years', 'building', 'relevant', 'technical', 'field',
    'equivalent', 'practical', 'degree', 'completed', 'prior', 'joining',
    'process', 'obtaining', 'bachelor', 'computer', 'engineering',
    'track', 'record', 'setting', 'direction', 'team', 'driving',
    'consensus', 'successful', 'cross', 'functional', 'partnerships',
    'maintainable', 'testable', 'code', 'bases', 'including', 'design',
    'unit', 'testing', 'techniques', 'least', 'one', 'large', 'scale',
    'product', 'production', 'supporting', 'millions', 'active', 'users',
    'shipped', 'complex', 'applications', 'targeting', 'using', 'native',
    'languages', 'frameworks', 'multithreading', 'mobile', 'memory',
    'management', 'preferred', 'qualifications', 'requirements',
    'work', 'your', 'build', 'checkout', 'payments', 'platform',
    'discord', 'fullstack', 'full', 'stack', 'developer', 'software',
    'must', 'should', 'currently', 'has', 'will', 'able', 'ability',
    'strong', 'good', 'excellent', 'demonstrated', 'proven', 'solid',
    // Buzzwords and soft skills
    'scalability', 'scalable', 'flexibility', 'flexible', 'reliability', 'reliable',
    'availability', 'available', 'maintainability', 'productivity', 'productive',
    'efficiency', 'efficient', 'performance', 'optimization', 'optimized',
    'integration', 'collaboration', 'collaborative', 'innovation', 'innovative',
    'creativity', 'creative', 'leadership', 'management', 'strategy', 'strategic',
    'planning', 'execution', 'delivery', 'success', 'successful', 'growth',
    'impact', 'impactful', 'value', 'excellence', 'excellent', 'commitment',
    'dedication', 'dedicated', 'passion', 'passionate', 'background', 'knowledge',
    'expertise', 'proficiency', 'proficient', 'capability', 'competency',
    'competent', 'skill', 'skills', 'qualification', 'requirement', 'advanced',
    'expert', 'experienced', 'senior', 'junior', 'lead', 'principal',
    // Generic tech words (not specific enough)
    'application', 'applications', 'system', 'systems', 'service', 'services',
    'tool', 'tools', 'solution', 'solutions', 'feature', 'features',
    'component', 'components', 'module', 'modules', 'library', 'libraries',
    'project', 'projects', 'user', 'users', 'client', 'clients',
    'server', 'servers', 'data', 'database', 'databases', 'framework',
    'architecture', 'infrastructure', 'environment', 'development',
    'implementation', 'deployment', 'maintenance', 'support',
    // Common phrases
    'problem', 'solving', 'critical', 'thinking', 'attention', 'detail',
    'communication', 'written', 'verbal', 'interpersonal', 'organizational',
    'time', 'prioritization', 'multitasking', 'adaptability', 'learning',
    'self', 'motivated', 'initiative', 'ownership', 'accountability',
    'responsibility', 'others', 'matters', 'clinical', 'various', 'multiple',
    'several', 'different', 'general', 'specific', 'particular'
  ];

  const filterTechnicalSkills = (skills) => {
    return skills.filter(skill => {
      const skillLower = skill.toLowerCase().trim();
      
      // Skip if too short (likely not a real skill)
      if (skillLower.length < 2) return false;
      
      // Skip generic words
      if (NON_TECHNICAL_WORDS.includes(skillLower)) return false;
      
      // Skip if it's just a number
      if (/^\d+$/.test(skillLower)) return false;
      
      // Skip common phrases with these words
      if (skillLower.includes('experience') || 
          skillLower.includes('years of') ||
          skillLower.includes('ability to') ||
          skillLower.includes('strong') ||
          skillLower.includes('working') ||
          skillLower.includes('knowledge of') ||
          skillLower.includes('understanding of') ||
          skillLower.includes('familiarity with')) return false;
      
      // Skip words ending in common soft skill suffixes
      if (skillLower.endsWith('ness') || 
          skillLower.endsWith('ship') || 
          skillLower.endsWith('ment') ||
          skillLower.endsWith('tion') ||
          skillLower.endsWith('sion') ||
          skillLower.endsWith('ance') ||
          skillLower.endsWith('ence') ||
          skillLower.endsWith('ity') ||
          skillLower.endsWith('ful') ||
          skillLower.endsWith('ive') ||
          skillLower.endsWith('able') ||
          skillLower.endsWith('ible')) {
        // Allow specific tech terms that end with these
        const techExceptions = ['authentication', 'authorization', 'implementation',
                               'configuration', 'automation', 'development', 'deployment',
                               'testing', 'programming', 'debugging', 'responsive'];
        if (!techExceptions.some(ex => skillLower.includes(ex))) {
          return false;
        }
      }
      
      // Skip if it contains multiple common words (likely a phrase, not a skill)
      const commonWords = ['to', 'of', 'in', 'for', 'with', 'and', 'or', 'the', 'a', 'an', 'at', 'on'];
      const words = skillLower.split(/\s+/);
      if (words.length > 2 && words.some(w => commonWords.includes(w))) return false;
      
      // Only accept if it looks like a technical term
      // Must contain: numbers, dots, hyphens, +, #, OR be a known tech pattern
      const techPatterns = [
        /\d/,  // Contains numbers (python3, angular2)
        /\./,  // Contains dots (node.js, vue.js)
        /-/,   // Contains hyphens (react-native)
        /[+#]/,  // Contains + or # (C++, C#)
        /^[A-Z]{2,5}$/,  // All caps acronym (AWS, SQL, API)
        /(script|base|flow|ware|sys|sql|web|net|cloud|api|dev|ops|bot|app|proto|graph)/i,  // Tech word parts
        /(python|java|ruby|rust|swift|kotlin|scala|perl|php|bash|react|angular|vue|node|django|flask|spring|docker|kubernetes|mongo|redis|postgres)/i  // Known tech
      ];
      
      const hasTechPattern = techPatterns.some(pattern => pattern.test(skillLower));
      
      return hasTechPattern;
    });
  };

  const findCourses = (skill) => {
    const skillLower = skill.toLowerCase();
    
    // Direct match
    if (COURSE_DATABASE[skillLower]) {
      return COURSE_DATABASE[skillLower];
    }
    
    // Partial match
    for (const [key, courses] of Object.entries(COURSE_DATABASE)) {
      if (skillLower.includes(key) || key.includes(skillLower)) {
        return courses;
      }
    }
    
    // Default generic courses
    return [
      { title: `Learn ${skill} - Comprehensive Guide`, platform: 'Search Online', url: `https://www.google.com/search?q=learn+${encodeURIComponent(skill)}+course`, level: 'All Levels' }
    ];
  };

  const toggleSkill = (skill) => {
    setExpandedSkill(expandedSkill === skill ? null : skill);
  };

  const getPriorityLevel = (index) => {
    if (index < 3) return 'high';
    if (index < 6) return 'medium';
    return 'low';
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'high': return '🔴 High Priority';
      case 'medium': return '🟡 Medium Priority';
      case 'low': return '🟢 Low Priority';
      default: return '';
    }
  };

  // Filter to only technical skills
  const technicalSkills = filterTechnicalSkills(missingSkills);

  if (!technicalSkills || technicalSkills.length === 0) {
    return (
      <div className="learning-path-container">
        <h2>🎓 Skills Development Path</h2>
        <div className="no-gaps">
          <p>🎉 Great news! Your resume has strong coverage for this position.</p>
          <p>Consider exploring these areas to stand out even more:</p>
          <ul>
            <li>Advanced certifications in your field</li>
            <li>Leadership and management skills</li>
            <li>Emerging technologies in your domain</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-path-container">
      <h2>🎓 Personalized Skills Development Path</h2>
      <p className="learning-description">
        Based on the job requirements, here are recommended courses to bridge your technical skill gaps:
      </p>

      <div className="skill-priority-legend">
        <span className="legend-item">🔴 High Priority - Learn first</span>
        <span className="legend-item">🟡 Medium Priority - Important skills</span>
        <span className="legend-item">🟢 Low Priority - Nice to have</span>
      </div>

      <div className="learning-path-list">
        {technicalSkills.slice(0, 10).map((skill, index) => {
          const priority = getPriorityLevel(index);
          const courses = findCourses(skill);
          const isExpanded = expandedSkill === skill;

          return (
            <div key={index} className={`skill-card ${priority}`}>
              <div className="skill-header" onClick={() => toggleSkill(skill)}>
                <div className="skill-info">
                  <h3>{skill}</h3>
                  <span className="priority-badge">{getPriorityLabel(priority)}</span>
                </div>
                <button className="expand-btn">
                  {isExpanded ? '▲' : '▼'}
                </button>
              </div>

              {isExpanded && (
                <div className="courses-list">
                  <h4>📚 Recommended Courses:</h4>
                  {courses.map((course, idx) => (
                    <div key={idx} className="course-card">
                      <div className="course-info">
                        <h5>{course.title}</h5>
                        <div className="course-meta">
                          <span className="platform-badge">{course.platform}</span>
                          <span className="level-badge">{course.level}</span>
                        </div>
                      </div>
                      <a
                        href={course.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="course-link"
                      >
                        View Course →
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="learning-tips">
        <h3>💡 Learning Tips</h3>
        <ul>
          <li><strong>Start with high-priority skills</strong> - These are most critical for the role</li>
          <li><strong>Set realistic goals</strong> - Focus on 1-2 skills at a time</li>
          <li><strong>Build projects</strong> - Apply what you learn in real-world scenarios</li>
          <li><strong>Update your resume</strong> - Add new skills as you complete courses</li>
          <li><strong>Get certified</strong> - Many courses offer certificates to showcase your learning</li>
        </ul>
      </div>
    </div>
  );
}

export default LearningPath;
