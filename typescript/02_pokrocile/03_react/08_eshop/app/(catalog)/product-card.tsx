import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardAction,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { type api } from "@/convex/_generated/api";
import currency from "currency.js";
import Link from "next/link";

type Product = (typeof api.products.list._returnType)[number];

export default function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/${product._id}`} className="grid">
      <Card>
        <CardHeader>
          <CardTitle>{product.title}</CardTitle>
          <CardDescription>{product.description}</CardDescription>
          <CardAction>
            <Badge>
              {currency(product.price.value).format({
                decimal: ",",
                separator: " ",
                precision: 2,
                pattern: "# !",
                symbol: "Kč",
              })}
            </Badge>
          </CardAction>
        </CardHeader>
      </Card>
    </Link>
  );
}
