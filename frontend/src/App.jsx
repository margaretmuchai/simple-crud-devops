import { useState, useEffect } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [editingId, setEditingId] = useState(null)

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    const res = await fetch('/api/tasks')
    const data = await res.json()
    setTasks(data)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const method = editingId ? 'PUT' : 'POST'
    const url = editingId ? `/api/tasks/${editingId}` : '/api/tasks'
    
    await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description })
    })
    
    setTitle('')
    setDescription('')
    setEditingId(null)
    fetchTasks()
  }

  const handleEdit = (task) => {
    setTitle(task.title)
    setDescription(task.description || '')
    setEditingId(task.id)
  }

  const handleDelete = async (id) => {
    await fetch(`/api/tasks/${id}`, { method: 'DELETE' })
    fetchTasks()
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Task Manager</h1>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ display: 'block', width: '100%', padding: '8px', marginBottom: '10px' }}
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ display: 'block', width: '100%', padding: '8px', marginBottom: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>
          {editingId ? 'Update' : 'Add'} Task
        </button>
        {editingId && (
          <button type="button" onClick={() => { setEditingId(null); setTitle(''); setDescription('') }} style={{ marginLeft: '10px' }}>
            Cancel
          </button>
        )}
      </form>

      <div>
        {tasks.map(task => (
          <div key={task.id} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <button onClick={() => handleEdit(task)} style={{ marginRight: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(task.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App