"use client";

import { Badge } from "@/components/ui/badge";
import { type api } from "@/convex/_generated/api";
import { usePreloadedQuery, type Preloaded } from "convex/react";
import currency from "currency.js";

export default function Content({
  productPreload,
}: {
  productPreload: Preloaded<typeof api.products.getById>;
}) {
  const product = usePreloadedQuery(productPreload);
  if (!product) return null;

  return (
    <div className="p-6 grid gap-4 max-w-7xl w-full mx-auto">
      <h1 className="text-2xl font-bold">{product.title}</h1>
      <p>{product.description}</p>
      <Badge className="text-lg">
        {currency(product.price.value).format({
          decimal: ",",
          separator: " ",
          precision: 2,
          pattern: "# !",
          symbol: "Kč",
        })}
      </Badge>
    </div>
  );
}
