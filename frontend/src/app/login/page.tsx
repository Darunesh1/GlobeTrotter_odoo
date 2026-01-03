"use client";

import { useState } from "react";
import { useAuth } from "@/context/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Link from "next/link";
import { Plane } from "lucide-react";

export default function LoginPage() {
  const { login, isLoading } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await login(email, password);
    } catch (err: unknown) {
      const extractErrorDetail = (error: unknown): string | undefined => {
        if (typeof error === "string") return error;
        if (typeof error === "object" && error !== null && "response" in error) {
          const maybeErr = error as Record<string, unknown>;
          const response = maybeErr.response as Record<string, unknown> | undefined;
          if (response && "data" in response) {
            const data = response.data as Record<string, unknown> | undefined;
            if (data && "detail" in data) {
              const detail = data.detail;
              if (typeof detail === "string") return detail;
            }
          }
        }
        return undefined;
      };

      setError(
        extractErrorDetail(err) ??
          "Invalid email or password. Please try again."
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/10 via-background to-secondary/20 px-4">
      <Card className="w-full max-w-md shadow-xl border-muted/40 backdrop-blur">
        <CardHeader className="space-y-3 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground">
            <Plane className="h-6 w-6" />
          </div>
          <CardTitle className="text-3xl font-bold">
            Welcome back
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Continue planning your next adventure
          </p>
        </CardHeader>

        <CardContent className="space-y-5">
          {error && (
            <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1">
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Password</label>
              <Input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full h-11 text-base"
              disabled={isLoading}
            >
              {isLoading ? "Signing in…" : "Sign In"}
            </Button>
          </form>

          <p className="text-sm text-center text-muted-foreground">
            Don’t have an account?{" "}
            <Link
              href="/register"
              className="font-medium text-primary underline-offset-4 hover:underline"
            >
              Create one
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
