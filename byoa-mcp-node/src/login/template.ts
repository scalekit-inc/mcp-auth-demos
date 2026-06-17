export function loginPage(params: {
  loginRequestId: string;
  state: string;
  error?: string;
}): string {
  const { loginRequestId, state, error } = params;
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sign in</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }
    .card {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      padding: 2rem;
      width: 100%;
      max-width: 380px;
    }
    h1 { font-size: 1.25rem; margin-bottom: 1.5rem; color: #111; }
    label { display: block; font-size: 0.875rem; color: #555; margin-bottom: 0.25rem; }
    input[type="email"], input[type="password"] {
      width: 100%;
      padding: 0.5rem 0.75rem;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      font-size: 1rem;
      margin-bottom: 1rem;
    }
    input:focus { outline: 2px solid #6366f1; border-color: transparent; }
    button {
      width: 100%;
      padding: 0.6rem;
      background: #6366f1;
      color: #fff;
      border: none;
      border-radius: 6px;
      font-size: 1rem;
      cursor: pointer;
    }
    button:hover { background: #4f46e5; }
    .error {
      background: #fef2f2;
      border: 1px solid #fca5a5;
      color: #b91c1c;
      border-radius: 6px;
      padding: 0.5rem 0.75rem;
      font-size: 0.875rem;
      margin-bottom: 1rem;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Sign in to continue</h1>
    ${error ? `<div class="error">${error}</div>` : ''}
    <form method="POST" action="/login/submit">
      <input type="hidden" name="login_request_id" value="${loginRequestId}" />
      <input type="hidden" name="state" value="${state}" />
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required autocomplete="email" />
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required autocomplete="current-password" />
      <button type="submit">Sign in</button>
    </form>
  </div>
</body>
</html>`;
}
