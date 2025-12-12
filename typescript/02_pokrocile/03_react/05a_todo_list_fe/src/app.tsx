import styles from "./app.module.css";
import { useTodosRQ } from "./use-todos";

export default function App() {
  const { todos, addTodo, toggleTodoCompletion } = useTodosRQ();

  async function handleSubmit(data: FormData) {
    const title = data.get("title") as string;
    if (!title) return;
    addTodo({ title });
  }

  return (
    <div className={styles.wrapper}>
      <h1 className={styles.title}>Todo List</h1>

      <form action={handleSubmit} className={styles.form}>
        <input type="text" name="title" required placeholder="Todo Title..." />
        <button>Add</button>
      </form>

      <ul className={styles.list}>
        {todos.map(({ uuid, isComplete, title }) => (
          <li key={uuid}>
            <label className={styles.todo}>
              <input
                type="checkbox"
                checked={isComplete}
                onChange={() => toggleTodoCompletion({ uuid })}
              />
              <span>{title}</span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
