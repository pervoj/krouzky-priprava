import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const list = query({
  handler: async (ctx) => {
    return await ctx.db.query("todos").collect();
  },
});

export const add = mutation({
  args: {
    title: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("todos", {
      title: args.title,
      isComplete: false,
    });
  },
});

export const toggleCompletion = mutation({
  args: {
    id: v.id("todos"),
  },
  handler: async (ctx, args) => {
    const todo = await ctx.db.get(args.id);
    if (!todo) return;
    return await ctx.db.patch(args.id, { isComplete: !todo.isComplete });
  },
});
