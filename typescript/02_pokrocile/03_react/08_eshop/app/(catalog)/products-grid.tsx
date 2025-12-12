"use client";

import { type api } from "@/convex/_generated/api";
import { usePreloadedQuery, type Preloaded } from "convex/react";
import ProductCard from "./product-card";

export default function ProductsGrid({
  productsPreload,
}: {
  productsPreload: Preloaded<typeof api.products.list>;
}) {
  const products = usePreloadedQuery(productsPreload);

  return (
    <div className="p-6 grid gap-4 max-w-7xl w-full mx-auto md:grid-cols-2 xl:grid-cols-3">
      {products.map((p) => (
        <ProductCard key={p._id} product={p} />
      ))}
    </div>
  );
}
