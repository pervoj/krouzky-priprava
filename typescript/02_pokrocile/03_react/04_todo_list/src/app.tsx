import styles from "./app.module.css";
import { useLocalStorage } from "./use-local-storage";

type TodoItem = {
  uuid: string;
  isComplete: boolean;
  title: string;
};

export default function App() {
  const [todos, setTodos] = useLocalStorage<TodoItem[]>("tasks", []);

  async function addTodo(data: FormData) {
    const title = data.get("title") as string;
    if (!title) return;

    setTodos((prev) => [
      {
        uuid: crypto.randomUUID(),
        isComplete: false,
        title,
      },
      ...prev,
    ]);
  }

  function toggleTodoCompletion(uuid: string) {
    setTodos((prev) =>
      prev.map((todo) => {
        if (todo.uuid !== uuid) return todo;
        return { ...todo, isComplete: !todo.isComplete };
      })
    );
  }

  return (
    <div className={styles.wrapper}>
      <h1 className={styles.title}>Todo List</h1>

      <form action={addTodo} className={styles.form}>
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
                onChange={() => toggleTodoCompletion(uuid)}
              />
              <span>{title}</span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
