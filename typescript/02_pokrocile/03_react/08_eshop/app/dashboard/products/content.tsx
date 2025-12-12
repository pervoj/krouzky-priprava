"use client";

import { api } from "@/convex/_generated/api";
import { Preloaded, usePreloadedQuery } from "convex/react";
import Link from "next/link";

export default function Content({
  productsPreload,
}: {
  productsPreload: Preloaded<typeof api.products.list>;
}) {
  const products = usePreloadedQuery(productsPreload);

  return (
    <div className="grid gap-4">
      {products.map((product) => (
        <Link
          key={product._id}
          href={`/dashboard/products/update/${product._id}`}
        >
          {product.title}
        </Link>
      ))}
    </div>
  );
}
