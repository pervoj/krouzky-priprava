import { auth } from "@clerk/nextjs/server";

export async function getConvexAuthToken(
  authRes?: Pick<Awaited<ReturnType<typeof auth>>, "getToken">,
) {
  const { getToken } = authRes ?? (await auth());
  return await getToken({ template: "convex" });
}
