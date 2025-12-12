import { literals } from "convex-helpers/validators";
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  roleMembers: defineTable({
    user: v.string(),
    role: literals("admin"),
  }).index("by_user", ["user"]),
  products: defineTable({
    title: v.string(),
    description: v.string(),
    price: v.object({
      value: v.number(),
      currency: v.string(),
    }),
    images: v.optional(v.array(v.id("_storage"))),
  }),
});
