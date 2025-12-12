"use client";

import { api } from "@/convex/_generated/api";
import { Preloaded, useMutation, usePreloadedQuery } from "convex/react";
import { useRouter } from "next/navigation";
import ProductForm from "../../product-form";

export default function Form({
  productPreload,
}: {
  productPreload: Preloaded<typeof api.products.getById>;
}) {
  const router = useRouter();
  const product = usePreloadedQuery(productPreload)!;
  const update = useMutation(api.products.update);

  return (
    <ProductForm
      defaultValues={{
        title: product.title,
        description: product.description,
        price: product.price.value,
      }}
      onSubmit={(data) =>
        update({ id: product._id, product: data }).then(() =>
          router.push("/dashboard/products"),
        )
      }
    />
  );
}
