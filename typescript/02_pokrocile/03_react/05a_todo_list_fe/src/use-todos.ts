import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

console.log(import.meta.env.VITE_BACKEND_URL);

const backendUrl = new URL(import.meta.env.VITE_BACKEND_URL);

type Todo = {
  uuid: string;
  title: string;
  isComplete: boolean;
};

async function listTodos() {
  const res = await fetch(new URL("/todos", backendUrl));
  const data = (await res.json()) as Todo[];
  return data;
}

async function addTodo(todo: { title: string }) {
  const res = await fetch(new URL("/todos", backendUrl), {
    method: "POST",
    body: JSON.stringify(todo),
  });
  const data = (await res.json()) as { success: boolean; todo: Todo };
  if (!data.success) throw new Error("Failed to create todo");
  return data.todo;
}

async function toggleTodoCompletion(todo: { uuid: string }) {
  const res = await fetch(new URL(`/todos/toggle/${todo.uuid}`, backendUrl), {
    method: "POST",
  });
  const data = (await res.json()) as { success: boolean; todo: Todo };
  if (!data.success) throw new Error("Failed to toggle todo completion");
  return data.todo;
}

export function useTodosRQ() {
  const { data: todos } = useQuery<Todo[]>({
    queryKey: ["todos"],
    initialData: [],
    queryFn: async () => {
      return await listTodos();
    },
  });

  const addMutation = useMutation({
    mutationFn: async (todo: { title: string }, ctx) => {
      await addTodo(todo);
      void ctx.client.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  const toggleCompletionMutation = useMutation({
    mutationFn: async (todo: { uuid: string }, ctx) => {
      await toggleTodoCompletion(todo);
      void ctx.client.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  return {
    todos,
    addTodo: addMutation.mutate,
    toggleTodoCompletion: toggleCompletionMutation.mutate,
  };
}

export function useTodosFetch() {
  const [todos, setTodos] = useState<Todo[]>([]);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/todos")
      .then((res) => res.json())
      .then((data) => setTodos(data));
  }, []);

  return todos;
}
