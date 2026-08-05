import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [problems, setProblems] = useState([])

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
        <h1>CodeArena ⚔️</h1>
        <nav>
          <button className="nav-btn">Problems</button>
          <button className="nav-btn login-btn">Sign In</button>
        </nav>
      </header>

      <main className="main-content">
        <h2 className="section-title">Problem Library</h2>
        <div className="problem-grid">
          {problems.map((problem) => (
            <div key={problem.id} className="problem-card">
              <div className="problem-header">
                <h3>{problem.id}. {problem.title}</h3>
                <span className="difficulty easy">Easy</span>
              </div>
              <p className="problem-desc">{problem.description}</p>
              <button className="solve-btn">Solve Challenge</button>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}

export default App