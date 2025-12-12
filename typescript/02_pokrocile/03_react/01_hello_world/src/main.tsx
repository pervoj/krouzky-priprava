/* eslint-disable react-refresh/only-export-components */

import { createElement } from "react";
import { createRoot } from "react-dom/client";

const rootElement = document.getElementById("root")!;
const reactRoot = createRoot(rootElement);

// ručně

reactRoot.render([
  createElement("h1", null, "Hello, World!"),
  createElement("p", null, "This is my first React app!"),
  createElement(
    "div",
    {
      title: "Hi!",
      style: {
        width: 128,
        height: 128,
        padding: 12,
        backgroundColor: "red",
      },
    },
    createElement("button", null, "Button!")
  ),
]);

// pomocí JSX

reactRoot.render(
  <>
    <h1>Hello, World!</h1>
    <p>This is my first React app with JSX!</p>
    <div
      title="Hi!"
      style={{
        width: 128,
        height: 128,
        padding: 12,
        backgroundColor: "red",
      }}
    >
      <button>Button!</button>
    </div>
  </>
);

// rozdělení do komponent

function Title() {
  return <h1>Hello, Components!</h1>;
}

type BoxProps = {
  title?: string;
  color?: string;
};

function Box({ title, color }: BoxProps) {
  return (
    <div
      title={title}
      style={{
        width: 128,
        height: 128,
        padding: 12,
        backgroundColor: color,
      }}
    >
      <button>Button!</button>
    </div>
  );
}

reactRoot.render(
  <>
    <Title />
    <p>This is my first React app with JSX!</p>
    <Box title="Hi, Props!" color="blue" />
  </>
);
