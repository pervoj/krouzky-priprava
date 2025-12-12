import { MyArray } from "./my-array";

const arr = MyArray.fromArray(["Hello", "World", "Ahoj", "Cau", "Hi", "Bye"]);

arr.reverse();

console.log(Array.from(arr));
