import { Button } from "@/components/ui/button";
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/nextjs";

export default function Header() {
  return (
    <header className="flex items-center justify-end p-4">
      <AuthNav />
    </header>
  );
}

function AuthNav() {
  return (
    <div className="flex items-center gap-2">
      <SignedOut>
        <Button asChild variant="outline" size="sm">
          <SignInButton />
        </Button>

        <Button asChild variant="default" size="sm">
          <SignUpButton />
        </Button>
      </SignedOut>

      <SignedIn>
        <UserButton />
      </SignedIn>
    </div>
  );
}
