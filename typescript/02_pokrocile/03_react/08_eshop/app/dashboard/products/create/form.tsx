"use client";

import { api } from "@/convex/_generated/api";
import { useMutation } from "convex/react";
import { useRouter } from "next/navigation";
import ProductForm from "../product-form";

export default function Form() {
  const router = useRouter();

  const create = useMutation(api.products.create);

  return (
    <ProductForm
      onSubmit={(data) =>
        create({ product: data }).then(() => router.push("/dashboard/products"))
      }
    />
  );
}
