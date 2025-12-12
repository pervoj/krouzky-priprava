import { query } from "./_generated/server";
import { getCurrentAdminUserId } from "./auth";

export const canOpenDashboard = query({
  handler: async (ctx) => {
    const userId = await getCurrentAdminUserId(ctx);
    return !!userId;
  },
});
