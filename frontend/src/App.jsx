import { useState, useEffect } from 'react'

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
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>CodeArena Dashboard</h1>
      <div style={{ marginTop: '20px' }}>
        {problems.map((problem) => (
          <div 
            key={problem.id} 
            style={{ 
              border: '1px solid #ccc', 
              padding: '15px', 
              marginBottom: '10px', 
              borderRadius: '8px' 
            }}
          >
            <h2>{problem.title}</h2>
            <p>{problem.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App