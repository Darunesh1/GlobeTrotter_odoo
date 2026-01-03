/**
 * Base URL of the backend API.
 *
 * This value comes from `.env.local`:
 * NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
 *
 * The `NEXT_PUBLIC_` prefix is required so Next.js
 * exposes this variable to the browser.
 */
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

/**
 * A shared helper function for making API calls to the backend.
 *
 * - Centralizes fetch logic
 * - Ensures consistent headers
 * - Handles errors in one place
 * - Makes frontend ↔ backend integration clean
 *
 * T is a generic type representing the expected response shape.
 */
export async function apiFetch<T>(
  path: string,               // API endpoint path (e.g. "/auth/login")
  options?: RequestInit       // Optional fetch configuration (method, body, headers)
): Promise<T> {
  /**
   * Make the HTTP request using the Fetch API
   */
  const res = await fetch(`${API_BASE}${path}`, {
    /**
     * Include cookies in requests.
     * Required if backend uses:
     * - HTTP-only cookies
     * - refresh tokens
     * - session-based auth
     */
    credentials: "include",

    /**
     * Default headers for JSON APIs.
     * Additional headers passed in `options` will override these.
     */
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },

    /**
     * Spread the rest of the fetch options
     * (method, body, etc.)
     */
    ...options,
  });

  /**
   * If the response is NOT successful (status not in 200–299),
   * throw an error so the caller can handle it (UI error message).
   */
  if (!res.ok) {
    /**
     * Try to read the error message returned by backend.
     * This helps show meaningful messages to users.
     */
    const errorText = await res.text();

    throw new Error(
      errorText || "Request failed. Please try again."
    );
  }

  /**
   * If the request succeeded, parse and return JSON response.
   *
   * The response is typed as `T`, so TypeScript
   * knows what shape to expect.
   */
  return res.json();
}
