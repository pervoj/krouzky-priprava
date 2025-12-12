import { partial } from "convex-helpers/validators";
import { v } from "convex/values";
import { type Id } from "./_generated/dataModel";
import { query, type QueryCtx } from "./_generated/server";
import { adminMutation } from "./auth";

async function getFileUrlsForIds(ctx: QueryCtx, ids: Id<"_storage">[]) {
  const urls = await Promise.all(ids.map((id) => ctx.storage.getUrl(id)));
  return urls.filter((url) => url !== null);
}

export const list = query({
  handler: async (ctx) => {
    const products = await ctx.db.query("products").collect();
    return await Promise.all(
      products.map(async (product) => {
        return {
          ...product,
          images: product.images
            ? await getFileUrlsForIds(ctx, product.images)
            : [],
        };
      }),
    );
  },
});

export const getById = query({
  args: {
    id: v.id("products"),
  },
  handler: async (ctx, args) => {
    const product = await ctx.db.get(args.id);
    if (!product) return null;

    return {
      ...product,
      images: product.images
        ? await getFileUrlsForIds(ctx, product.images)
        : [],
    };
  },
});

export const create = adminMutation({
  args: {
    product: v.object({
      title: v.string(),
      description: v.string(),
      price: v.number(),
    }),
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("products", {
      title: args.product.title,
      description: args.product.description,
      price: { value: args.product.price, currency: "CZK" },
    });
  },
});

export const update = adminMutation({
  args: {
    id: v.id("products"),
    product: partial(
      v.object({
        title: v.string(),
        description: v.string(),
        price: v.number(),
      }),
    ),
  },
  handler: async (ctx, args) => {
    return await ctx.db.patch(args.id, {
      title: args.product.title,
      description: args.product.description,
      price: args.product.price
        ? { value: args.product.price, currency: "CZK" }
        : undefined,
    });
  },
});
