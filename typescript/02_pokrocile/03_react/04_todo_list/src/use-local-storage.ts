import { useEffect, useState } from "react";

// https://react.dev/learn/you-might-not-need-an-effect

export function useLocalStorage<T>(key: string, defaultValue: T | (() => T)) {
  const [value, setValue] = useState<T>(() => {
    const jsonValue = window.localStorage.getItem(key);
    if (jsonValue != null) return JSON.parse(jsonValue);

    if (defaultValue instanceof Function) {
      return defaultValue();
    } else {
      return defaultValue;
    }
  });

  useEffect(() => {
    if (value === undefined) return window.localStorage.removeItem(key);
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
