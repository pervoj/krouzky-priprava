import { Button } from "@/components/ui/button";
import { api } from "@/convex/_generated/api";
import { preloadQuery } from "convex/nextjs";
import Link from "next/link";
import { validateAdminAndGetToken } from "../validate-admin";
import Content from "./content";

export default async function Page() {
  const token = await validateAdminAndGetToken();
  const productsPreload = await preloadQuery(api.products.list, {}, { token });

  return (
    <div className="grid gap-8 p-6 max-w-7xl w-full mx-auto">
      <div className="flex items-center justify-end">
        <Button asChild variant="outline" size="sm">
          <Link href="/dashboard/products/create">Create Product</Link>
        </Button>
      </div>

      <Content productsPreload={productsPreload} />
    </div>
  );
}
