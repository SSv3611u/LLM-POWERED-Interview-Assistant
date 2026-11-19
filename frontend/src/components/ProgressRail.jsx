export default function ProgressRail({ questions, currentIndex, answeredIds, onNavigate }) {
  return (
    <div className="progress-rail">
      {questions.map((q, i) => {
        const isDone = answeredIds.has(q.id)
        const isActive = i === currentIndex
        const cls = isDone ? 'progress-dot done' : isActive ? 'progress-dot active' : 'progress-dot'
        const isAvailable = i <= currentIndex || isDone
        return <button type="button" key={q.id} className={`${cls} ${isAvailable ? 'navigable' : ''}`} onClick={() => isAvailable && onNavigate(i)} disabled={!isAvailable} aria-label={`Question ${i + 1}`}>{i + 1}</button>
      })}
    </div>
  )
}
