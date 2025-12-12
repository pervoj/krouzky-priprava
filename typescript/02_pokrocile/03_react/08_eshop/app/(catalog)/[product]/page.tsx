import { api } from "@/convex/_generated/api";
import { type Id } from "@/convex/_generated/dataModel";
import { preloadedQueryResult, preloadQuery } from "convex/nextjs";
import { notFound } from "next/navigation";
import Content from "./content";

export default async function Page({ params }: PageProps<"/[product]">) {
  const { product: productId } = await params;

  const productPreload = await preloadQuery(api.products.getById, {
    id: productId as Id<"products">,
  });

  const productValue = preloadedQueryResult(productPreload);
  if (!productValue) return notFound();

  return <Content productPreload={productPreload} />;
}
