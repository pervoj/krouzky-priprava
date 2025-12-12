import { MyArray } from "./my-array";

export class MyArrayIterator<T> {
  private _index = 0;
  private _array: MyArray<T>;

  constructor(array: MyArray<T>) {
    this._array = array;
  }

  next() {
    const done = this._index >= this._array.length;
    if (done) return { done, value: undefined };

    const value = this._array.at(this._index);
    this._index++;

    return { done: false, value };
  }
}
