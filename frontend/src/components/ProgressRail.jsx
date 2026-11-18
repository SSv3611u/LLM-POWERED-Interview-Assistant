export default function ProgressRail({ questions, currentIndex, answeredIds }) {
  return (
    <div className="progress-rail">
      {questions.map((q, i) => {
        const isDone = answeredIds.has(q.id)
        const isActive = i === currentIndex
        const cls = isDone ? 'progress-dot done' : isActive ? 'progress-dot active' : 'progress-dot'
        return <div key={q.id} className={cls}>{i + 1}</div>
      })}
    </div>
  )
}
