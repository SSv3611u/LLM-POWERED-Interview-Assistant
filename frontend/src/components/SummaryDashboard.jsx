export default function SummaryDashboard({ summary, questions, onRestart, onReview }) {
  const questionById = Object.fromEntries(questions.map(q => [q.id, q]))

  return (
    <div className="card">
      <div className="summary-row">
        <span>Average score</span>
      </div>
      <div className="summary-avg">{summary.averageScore.toFixed(1)}<span style={{ fontSize: 20 }}>/10</span></div>
      <div className="hint" style={{ marginBottom: 24 }}>
        {summary.questionsAnswered} of {summary.totalQuestions} questions answered — {summary.targetRole}
      </div>

      {summary.feedbackList.map(f => (
        <div key={f.questionId} className="feedback-panel">
          <div className="category-tag">{questionById[f.questionId]?.category}</div>
          <div className="question-text" style={{ fontSize: 15 }}>
            {questionById[f.questionId]?.questionText}
          </div>
          <div className="score-badge">{f.score} / 10</div>
          <div className="rubric-grid">{Object.entries(f.rubric || {}).map(([name, score]) => <div key={name}><span>{name}</span><strong>{score}/10</strong></div>)}</div>
          <div className="feedback-text">{f.feedback}</div>
          <div className="ideal-points">{f.idealAnswerPoints}</div>
          {onReview && <button className="link-button" onClick={() => onReview(f.questionId)}>Add human review</button>}
        </div>
      ))}

      <div className="feedback-panel"><h3>Skill-gap analysis</h3>{summary.skillGaps.map(gap => <div className="gap-row" key={gap.skill}><div><strong>{gap.skill}</strong><span>{gap.recommendation}</span></div><b className={`priority ${gap.priority.toLowerCase()}`}>{gap.averageScore}/10 · {gap.priority}</b></div>)}</div>
      <div className="feedback-panel"><h3>Practice plan</h3><ol>{summary.practicePlan.map(item => <li key={item}>{item}</li>)}</ol></div>

      <div className="actions-row">
        <button className="ghost" onClick={onRestart}>Start a new session</button>
      </div>
    </div>
  )
}
