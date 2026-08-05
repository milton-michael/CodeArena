import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import './App.css'

function App() {
  const [problems, setProblems] = useState([])
  const [activeProblem, setActiveProblem] = useState(null)
  const [code, setCode] = useState('# Write your Python code here\n')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/problems')
      .then((response) => response.json())
      .then((data) => {
        if (data.problems) {
          setProblems(data.problems)
        }
      })
      .catch((error) => console.error('Error fetching data:', error))
  }, [])

  return (
    <div className="app-container">
      <header className="navbar">
        <h1 onClick={() => setActiveProblem(null)} style={{cursor: 'pointer'}}>CodeArena ⚔️</h1>
        <nav>
          <button className="nav-btn" onClick={() => setActiveProblem(null)}>Problems</button>
          <button className="nav-btn login-btn">Sign In</button>
        </nav>
      </header>

      <main className="main-content">
        {!activeProblem ? (
          // Dashboard View
          <>
            <h2 className="section-title">Problem Library</h2>
            <div className="problem-grid">
              {problems.map((problem) => (
                <div key={problem.id} className="problem-card">
                  <div className="problem-header">
                    <h3>{problem.id}. {problem.title}</h3>
                    <span className="difficulty easy">Easy</span>
                  </div>
                  <p className="problem-desc">{problem.description}</p>
                  <button className="solve-btn" onClick={() => setActiveProblem(problem)}>
                    Solve Challenge
                  </button>
                </div>
              ))}
            </div>
          </>
        ) : (
          // Active Workspace View
          <div className="workspace">
            <div className="problem-panel">
              <h2>{activeProblem.title}</h2>
              <span className="difficulty easy" style={{display: 'inline-block', marginTop: '10px'}}>Easy</span>
              <p className="problem-desc" style={{marginTop: '20px'}}>{activeProblem.description}</p>
            </div>
            
            <div className="editor-panel">
              <div className="editor-header">
                <span>main.py</span>
                <button className="run-btn">Run Code</button>
              </div>
              <Editor
                height="100%"
                defaultLanguage="python"
                theme="vs-dark"
                value={code}
                onChange={(value) => setCode(value)}
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                }}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App