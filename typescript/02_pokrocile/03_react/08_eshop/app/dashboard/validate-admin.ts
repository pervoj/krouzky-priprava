import { api } from "@/convex/_generated/api";
import { getConvexAuthToken } from "@/lib/auth";
import { fetchQuery } from "convex/nextjs";
import { forbidden, unauthorized } from "next/navigation";

export async function validateAdminAndGetToken() {
  const token = await getConvexAuthToken();
  if (!token) return unauthorized();

  const canOpen = await fetchQuery(
    api.dashboard.canOpenDashboard,
    {},
    { token },
  );
  if (!canOpen) return forbidden();

  return token;
}
