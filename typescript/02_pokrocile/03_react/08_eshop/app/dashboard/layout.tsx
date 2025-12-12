import { ReactNode } from "react";
import { validateAdminAndGetToken } from "./validate-admin";

export default async function Layout({ children }: { children: ReactNode }) {
  await validateAdminAndGetToken();

  return <>{children}</>;
}
