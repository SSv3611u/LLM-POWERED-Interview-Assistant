import { useState } from 'react'

export default function SetupForm({ onStart, loading }) {
  const [targetRole, setTargetRole] = useState('')
  const [techStack, setTechStack] = useState('')
  const [resumeSummary, setResumeSummary] = useState('')
  const [numberOfQuestions, setNumberOfQuestions] = useState(5)
  const [extracting, setExtracting] = useState(false)

  async function handleResumeUpload(event) {
    const file = event.target.files?.[0]
    if (!file) return
    setExtracting(true)
    try {
      const { extractResume } = await import('../api/interviewApi.js')
      const { text } = await extractResume(file)
      setResumeSummary(text)
    } finally { setExtracting(false) }
  }

  function handleSubmit(e) {
    e.preventDefault()

    onStart({
      targetRole,
      techStack,
      resumeSummary,
      numberOfQuestions: Number(numberOfQuestions),
    })
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <div className="field">
        <label>Target Role</label>

        <input
          type="text"
          placeholder="e.g. AI Engineer, Java Developer, Full Stack Developer"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          required
        />
      </div>

      <div className="field">
        <label>Tech Stack / Skills</label>

        <input
          type="text"
          placeholder="e.g. Java, Spring Boot, React, MySQL, DSA"
          value={techStack}
          onChange={(e) => setTechStack(e.target.value)}
          required
        />

        <div className="hint">
          Enter your skills separated by commas.
        </div>
      </div>

      <div className="field">
        <label>Resume Summary (Optional)</label>

        <textarea
          placeholder="Paste your resume summary, projects, internships or achievements..."
          value={resumeSummary}
          onChange={(e) => setResumeSummary(e.target.value)}
        />
        <div className="upload-row"><label className="file-button">{extracting ? 'Reading resume...' : 'Upload PDF resume'}<input type="file" accept="application/pdf" onChange={handleResumeUpload} disabled={extracting} /></label></div>
      </div>

      <div className="field">
        <label>Number of Questions</label>

        <input
          type="number"
          min="3"
          max="15"
          value={numberOfQuestions}
          onChange={(e) => setNumberOfQuestions(e.target.value)}
        />
      </div>

      <div className="actions-row">
        <button
          className="primary"
          type="submit"
          disabled={loading}
        >
          {loading ? 'Generating Questions...' : 'Start Mock Interview'}
        </button>
      </div>
    </form>
  )
}
