import { useState } from "react";

export default function AuthForm({ onSubmit, loading }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  function submit(event) { event.preventDefault(); onSubmit(mode, { name, email, password }); }
  return <form className="card auth-card" onSubmit={submit}>
    <div className="eyebrow">Your interview workspace</div>
    <h2>{mode === "login" ? "Welcome back" : "Create your account"}</h2>
    {mode === "register" && <div className="field"><label>Name</label><input value={name} onChange={e => setName(e.target.value)} required minLength="2" /></div>}
    <div className="field"><label>Email</label><input type="email" value={email} onChange={e => setEmail(e.target.value)} required /></div>
    <div className="field"><label>Password</label><input type="password" value={password} onChange={e => setPassword(e.target.value)} required minLength="8" /></div>
    <div className="actions-row"><button className="primary" disabled={loading}>{loading ? "Please wait..." : mode === "login" ? "Sign in" : "Create account"}</button></div>
    <button type="button" className="link-button" onClick={() => setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "New here? Create an account" : "Already have an account? Sign in"}</button>
  </form>
}
