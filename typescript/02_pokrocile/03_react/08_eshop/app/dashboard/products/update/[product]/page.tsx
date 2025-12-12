import { validateAdminAndGetToken } from "@/app/dashboard/validate-admin";
import { api } from "@/convex/_generated/api";
import { type Id } from "@/convex/_generated/dataModel";
import { preloadedQueryResult, preloadQuery } from "convex/nextjs";
import { notFound } from "next/navigation";
import Form from "./form";

export default async function Page({
  params,
}: PageProps<"/dashboard/products/update/[product]">) {
  const token = await validateAdminAndGetToken();
  const { product: productId } = await params;
  const productPreload = await preloadQuery(
    api.products.getById,
    { id: productId as Id<"products"> },
    { token },
  );

  const product = preloadedQueryResult(productPreload);
  if (!product) return notFound();

  return (
    <div>
      <Form productPreload={productPreload} />
    </div>
  );
}
