import { useState } from "react";

export default function App() {
  const [counter, setCounter] = useState(0);

  function increment() {
    setCounter((prev) => prev - 1);
  }

  function decrement() {
    setCounter((prev) => prev + 1);
  }

  return (
    <>
      <h1>Počítadlo</h1>

      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <button onClick={increment}>-</button>
        <span>{counter}</span>
        <button onClick={decrement}>+</button>
      </div>

      <p>Číslo je {counter % 2 === 0 ? "sudé" : "liché"}</p>
      {counter < 0 && <p>Číslo je záporné</p>}
    </>
  );
}
