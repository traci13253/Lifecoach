const { useState, useEffect } = React;

function GoalForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/goals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description })
    });
    const newGoal = await res.json();
    onAdd(newGoal);
    setTitle('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Goal title" />
      <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" />
      <button type="submit">Add Goal</button>
    </form>
  );
}

function TaskList({ goal, onChange }) {
  const [tasks, setTasks] = useState([]);
  const [desc, setDesc] = useState('');

  useEffect(() => {
    if (goal) {
      fetch(`/tasks?goal_id=${goal.id}`).then(res => res.json()).then(setTasks);
    }
  }, [goal]);

  const addTask = async (e) => {
    e.preventDefault();
    const res = await fetch('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: desc, goal_id: goal.id })
    });
    const newTask = await res.json();
    const updated = [...tasks, newTask];
    setTasks(updated);
    setDesc('');
    onChange();
  };

  const toggleComplete = async (task) => {
    const res = await fetch(`/tasks/${task.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !task.completed })
    });
    const updated = await res.json();
    setTasks(tasks.map(t => t.id === updated.id ? updated : t));
    onChange();
  };

  return (
    <div>
      <h3>Tasks for {goal.title}</h3>
      <ul>
        {tasks.map(t => (
          <li key={t.id}>
            <input type="checkbox" checked={t.completed} onChange={() => toggleComplete(t)} />
            {t.description}
          </li>
        ))}
      </ul>
      <form onSubmit={addTask}>
        <input value={desc} onChange={e => setDesc(e.target.value)} placeholder="New task" />
        <button type="submit">Add Task</button>
      </form>
    </div>
  );
}

function AchievementSummary({ refresh }) {
  const [summary, setSummary] = useState({ total: 0, completed: 0 });

  useEffect(() => {
    fetch('/tasks').then(res => res.json()).then(tasks => {
      const total = tasks.length;
      const completed = tasks.filter(t => t.completed).length;
      setSummary({ total, completed });
    });
  }, [refresh]);

  return (
    <div>
      <h2>Achievements</h2>
      <p>{summary.completed} of {summary.total} tasks completed</p>
    </div>
  );
}

function GoalApp() {
  const [goals, setGoals] = useState([]);
  const [selected, setSelected] = useState(null);
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    fetch('/goals').then(res => res.json()).then(setGoals);
  }, []);

  const addGoal = (goal) => {
    setGoals([...goals, goal]);
  };

  const refreshSummary = () => setRefresh(r => r + 1);

  return (
    <div>
      <h1>Lifecoach Goals</h1>
      <GoalForm onAdd={addGoal} />
      <ul>
        {goals.map(g => (
          <li key={g.id} onClick={() => setSelected(g)}>{g.title}</li>
        ))}
      </ul>
      {selected && <TaskList goal={selected} onChange={refreshSummary} />}
      <AchievementSummary refresh={refresh} />
    </div>
  );
}

ReactDOM.render(<GoalApp />, document.getElementById('root'));
