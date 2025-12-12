import {
  customCtxAndArgs,
  customMutation,
  customQuery,
} from "convex-helpers/server/customFunctions";
import { Doc } from "./_generated/dataModel";
import { mutation, query, type QueryCtx } from "./_generated/server";

const allowedRoles: Doc<"roleMembers">["role"][] = ["admin"];

export async function getCurrentAdminUserId(ctx: QueryCtx) {
  const user = await ctx.auth.getUserIdentity();
  if (!user) return null;

  const userId = user.tokenIdentifier;
  const roleMember = await ctx.db
    .query("roleMembers")
    .withIndex("by_user", (q) => q.eq("user", userId))
    .first();

  if (!roleMember) return null;
  if (!allowedRoles.includes(roleMember.role)) return null;

  return userId;
}

const funcBuilder = customCtxAndArgs({
  args: {},
  input: async (ctx: QueryCtx) => {
    const userId = await getCurrentAdminUserId(ctx);
    if (!userId) throw new Error("Unauthorized");
    return { ctx: { userId }, args: {} };
  },
});

export const adminQuery = customQuery(query, funcBuilder);
export const adminMutation = customMutation(mutation, funcBuilder);
