"use client";

import { useMutation, useQuery } from "convex/react";
import { api } from "~/convex/_generated/api";

export default function Products() {
  const products = useQuery(api.products.list) ?? [];

  const createProduct = useMutation(api.products.create);

  async function handleSubmit(data: FormData) {
    const name = data.get("name")?.toString() ?? "";

    await createProduct({ name });
  }

  return (
    <div className="grid gap-4">
      <form className="flex items-stretch gap-2" action={handleSubmit}>
        <input
          name="name"
          type="text"
          placeholder="Název produktu"
          required
          className="grow border rounded-xl px-2 py-1"
        />
        <button className="border rounded-xl px-2 py-1">Vytvořit</button>
      </form>

      <ul className="grid gap-2">
        {products.map((product) => (
          <li key={product._id} className="p-4 border rounded-xl">
            {product.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
