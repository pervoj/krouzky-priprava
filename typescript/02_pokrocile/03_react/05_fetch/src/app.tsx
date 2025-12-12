/* eslint-disable @typescript-eslint/no-unused-vars */

import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import { useEffect, useState } from "react";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TodoList />
    </QueryClientProvider>
  );
}

function TodoList() {
  const todos = useTodosRQ();
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}

type Todo = {
  id: number;
  userId: number;
  title: string;
  completed: boolean;
};

function useTodosRQ() {
  const { data: todos } = useQuery<Todo[]>({
    queryKey: ["todos"],
    initialData: [],
    queryFn: async () => {
      const res = await fetch("https://jsonplaceholder.typicode.com/todos");
      const data = await res.json();
      return data;
    },
  });

  return todos;
}

function useTodosFetch() {
  const [todos, setTodos] = useState<Todo[]>([]);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/todos")
      .then((res) => res.json())
      .then((data) => setTodos(data));
  }, []);

  return todos;
}
