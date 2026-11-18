import { useState, useEffect } from 'react'

export default function QuestionCard({
  question,
  onSubmit,
  submitting,
  feedback,
  onNext,
  isLast,
}) {
  const [answerText, setAnswerText] = useState('')

  // Clear the textarea whenever the question changes
  useEffect(() => {
    setAnswerText('')
  }, [question.id])

  function handleSubmit(e) {
    e.preventDefault()

    if (!answerText.trim()) return

    onSubmit(answerText)
  }

  return (
    <div className="card">
      <div className="category-tag">{question.category}</div>

      <div className="question-text">
        {question.questionText}
      </div>

      {!feedback && (
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Your Answer</label>

            <textarea
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Type your answer here..."
              required
            />
          </div>

          <div className="actions-row">
            <button
              className="primary"
              type="submit"
              disabled={submitting}
            >
              {submitting
                ? 'Evaluating...'
                : 'Submit Answer'}
            </button>
          </div>
        </form>
      )}

      {feedback && (
        <div className="feedback-panel">
          <div className="score-badge">
            {feedback.score} / 10
          </div>

          <div className="rubric-grid">
            {Object.entries(feedback.rubric || {}).map(([name, score]) => <div key={name}><span>{name}</span><strong>{score}/10</strong></div>)}
          </div>

          <div className="feedback-text">
            {feedback.feedback}
          </div>

          <div className="ideal-points">
            <strong>Ideal answer points</strong><br />{feedback.idealAnswerPoints}
          </div>
          {feedback.missingConcepts?.length > 0 && <div className="missing"><strong>Focus next:</strong> {feedback.missingConcepts.join(', ')}</div>}

          <div className="actions-row">
            <button
              className="primary"
              onClick={onNext}
            >
              {isLast
                ? 'See Summary'
                : 'Next Question'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
