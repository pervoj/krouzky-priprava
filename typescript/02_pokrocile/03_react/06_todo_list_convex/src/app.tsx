import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import styles from "./app.module.css";

export default function App() {
  const todos = useQuery(api.todos.list) ?? [];

  const addTodo = useMutation(api.todos.add);
  const toggleTodoCompletion = useMutation(api.todos.toggleCompletion);

  async function handleSubmit(data: FormData) {
    const title = data.get("title") as string;
    await addTodo({ title });
  }

  return (
    <div className={styles.wrapper}>
      <h1 className={styles.title}>Todo List</h1>

      <form action={handleSubmit} className={styles.form}>
        <input type="text" name="title" required placeholder="Todo Title..." />
        <button>Add</button>
      </form>

      <ul className={styles.list}>
        {todos.map(({ _id, isComplete, title }) => (
          <li key={_id}>
            <label className={styles.todo}>
              <input
                type="checkbox"
                checked={isComplete}
                onChange={() => void toggleTodoCompletion({ id: _id })}
              />
              <span>{title}</span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
