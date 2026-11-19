import { useState } from "react";

export default function ProfilePanel({ profile, onSave, onBack, saving }) {
  const [name, setName] = useState(profile.name);
  const [editing, setEditing] = useState(false);
  function submit(event) { event.preventDefault(); onSave(name); setEditing(false); }
  return <section className="card profile-panel">
    <div className="summary-row"><div><div className="eyebrow">Account profile</div><h2>{profile.name}</h2></div><button className="ghost" onClick={onBack}>Back to workspace</button></div>
    <div className="profile-stats"><div><b>{profile.interviewsCompleted}</b><span>completed interviews</span></div><div><b>{profile.averageScore.toFixed(1)}</b><span>average score</span></div></div>
    {editing ? <form onSubmit={submit}><div className="field"><label>Display name</label><input value={name} onChange={event => setName(event.target.value)} minLength="2" required /></div><div className="actions-row"><button type="button" className="ghost" onClick={() => setEditing(false)}>Cancel</button><button className="primary" disabled={saving}>Save profile</button></div></form> : <div className="profile-details"><div><span>Email</span><strong>{profile.email}</strong></div><div><span>Member since</span><strong>{profile.memberSince}</strong></div><button className="link-button" onClick={() => setEditing(true)}>Edit display name</button></div>}
  </section>
}
