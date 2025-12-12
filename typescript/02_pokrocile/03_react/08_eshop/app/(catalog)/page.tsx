import { api } from "@/convex/_generated/api";
import { preloadQuery } from "convex/nextjs";
import ProductsGrid from "./products-grid";

export default async function Page() {
  const productsPreload = await preloadQuery(api.products.list);

  return <ProductsGrid productsPreload={productsPreload} />;
}
