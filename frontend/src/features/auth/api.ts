import { apiFetch } from "@/lib/api";

/**
 * Login user with email & password
 */
export function login(email: string, password: string) {
  return apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

/**
 * Register a new user
 */
export function register(data: {
  name: string;
  email: string;
  password: string;
}) {
  return apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Logout current user
 */
export function logout() {
  return apiFetch("/auth/logout", {
    method: "POST",
  });
}

/**
 * Get current logged-in user
 */
export function getMe() {
  return apiFetch("/auth/me");
}

/**
 * Request password reset
 */
export function forgotPassword(email: string) {
  return apiFetch("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}
