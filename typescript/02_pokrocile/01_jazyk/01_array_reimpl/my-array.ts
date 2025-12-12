import { MyArrayIterator } from "./my-array-iterator";

export class MyArray<T> {
  private _length = 0;
  private _data: Record<number, T> = {};

  get length() {
    return this._length;
  }

  at(index: number) {
    return this._data[index];
  }

  push(item: T) {
    this._data[this._length] = item;
    this._length++;
  }

  indexOf(item: T) {
    for (let i = 0; i < this._length; i++) {
      if (this._data[i] === item) return i;
    }

    return -1;
  }

  insertAt(index: number, item: T) {
    if (index < 0 || index > this._length) {
      throw new Error("Index out of bounds");
    }

    for (let i = this._length; i > index; i--) {
      this._data[i] = this._data[i - 1]!;
    }

    this._data[index] = item;
    this._length++;
  }

  removeAt(index: number) {
    if (index < 0 || index >= this._length) {
      throw new Error("Index out of bounds");
    }

    for (let i = index; i < this._length - 1; i++) {
      this._data[i] = this._data[i + 1]!;
    }

    delete this._data[this._length - 1];
    this._length--;
  }

  remove(item: T) {
    const index = this.indexOf(item);
    if (index !== -1) this.removeAt(index);
  }

  forEach(cb: (item: T, index: number) => void) {
    for (let i = 0; i < this._length; i++) {
      cb(this._data[i]!, i);
    }
  }

  map<U>(cb: (item: T, index: number) => U) {
    const result = new MyArray<U>();

    for (let i = 0; i < this._length; i++) {
      result.push(cb(this._data[i]!, i));
    }

    return result;
  }

  filter(cb: (item: T, index: number) => boolean) {
    const result = new MyArray<T>();

    for (let i = 0; i < this._length; i++) {
      const item = this._data[i]!;
      if (cb(item, i)) result.push(item);
    }

    return result;
  }

  reduce<U>(cb: (acc: U, item: T, index: number) => U, initialValue: U) {
    let acc = initialValue;

    for (let i = 0; i < this._length; i++) {
      acc = cb(acc, this._data[i]!, i);
    }

    return acc;
  }

  some(cb: (item: T, index: number) => boolean) {
    for (let i = 0; i < this._length; i++) {
      if (cb(this._data[i]!, i)) return true;
    }

    return false;
  }

  every(cb: (item: T, index: number) => boolean) {
    for (let i = 0; i < this._length; i++) {
      if (!cb(this._data[i]!, i)) return false;
    }

    return true;
  }

  find(cb: (item: T, index: number) => boolean) {
    for (let i = 0; i < this._length; i++) {
      if (cb(this._data[i]!, i)) return this._data[i]!;
    }

    return undefined;
  }

  reverse() {
    for (let i = 0; i < this._length / 2; i++) {
      const j = this._length - 1 - i;

      const leftItem = this._data[i]!;
      const rightItem = this._data[j]!;

      this._data[i] = rightItem;
      this._data[j] = leftItem;
    }
  }

  // sort(cb: (a: T, b: T) => number) {
  //   for (let i = 0; i < this._length; i++) {
  //     for (let j = i + 1; j < this._length; j++) {
  //       if (cb(this._data[i]!, this._data[j]!) > 0) {
  //         const temp = this._data[i]!;
  //         this._data[i] = this._data[j]!;
  //         this._data[j] = temp;
  //       }
  //     }
  //   }
  // }

  toString() {
    let result = "<";

    for (let i = 0; i < this._length; i++) {
      result += this._data[i]?.toString() ?? "";
      if (i < this._length - 1) result += ", ";
    }

    result += ">";
    return result;
  }

  [Symbol.iterator]() {
    return new MyArrayIterator(this);
  }

  static fromArray<T>(array: T[]) {
    const myArray = new MyArray<T>();
    for (const item of array) {
      myArray.push(item);
    }
    return myArray;
  }
}
