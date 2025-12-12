import { Hono } from "hono";
import { cors } from "hono/cors";
import { readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { v4 as generateUuid } from "uuid";

const todosFile = join(__dirname, "todos.json");

type Todo = {
  uuid: string;
  title: string;
  isComplete: boolean;
};

async function listTodos() {
  const data = await readFile(todosFile, { encoding: "utf8" });
  return JSON.parse(data) as Todo[];
}

async function saveTodos(todos: Todo[]) {
  await writeFile(todosFile, JSON.stringify(todos));
}

async function addTodo(title: string) {
  const todo: Todo = {
    uuid: generateUuid(),
    title: title,
    isComplete: false,
  };

  const todos = await listTodos();
  todos.push(todo);
  await saveTodos(todos);
  return todo;
}

async function toggleTodoCompletion(uuid: string) {
  let todo: Todo | null = null;

  const todos = await listTodos();
  for (const currentTodo of todos) {
    if (currentTodo.uuid !== uuid) continue;
    currentTodo.isComplete = !currentTodo.isComplete;
    todo = currentTodo;
  }

  await saveTodos(todos);
  return todo;
}

const app = new Hono();
app.use(cors());

app.get("/todos", async (c) => {
  const todos = await listTodos();
  return c.json(todos);
});

app.post("/todos", async (c) => {
  const req = (await c.req.json()) as { title: string };
  const todo = await addTodo(req.title);
  return c.json({ success: true, todo });
});

app.post("/todos/toggle/:uuid", async (c) => {
  const uuid = c.req.param("uuid");
  const todo = await toggleTodoCompletion(uuid);
  return c.json({ success: true, todo });
});

export default app;
