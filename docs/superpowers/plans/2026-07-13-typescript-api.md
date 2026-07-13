# Minimal TypeScript API Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the smallest possible Express + TypeScript backend with two JSON endpoints, test it with curl/browser, and publish it to a public GitHub repository.

**Architecture:** A single-file Express server that defines a Welcome endpoint (`GET /`) and a System Status endpoint (`GET /api/info`). Testing is handled using Node.js's native test runner (`node:test`) and native `fetch` over an ephemeral port, keeping dependencies extremely lightweight.

**Tech Stack:** Node.js (v18+), Express.js, TypeScript, tsx (for execution), native node:test (for testing).

---

### Task 1: Project Initialization and Configuration

**Files:**
- Create: `Assignment 1/package.json`
- Create: `Assignment 1/tsconfig.json`

- [ ] **Step 1: Create package.json**

Write the following contents to `D:/work/projects/flyrank/Assignment 1/package.json`:
```json
{
  "name": "minimal-typescript-api",
  "version": "1.0.0",
  "description": "Minimal TypeScript API Server",
  "main": "server.ts",
  "scripts": {
    "dev": "tsx server.ts",
    "test": "node --import tsx --test server.test.ts"
  },
  "dependencies": {
    "express": "^4.19.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^20.11.24",
    "typescript": "^5.3.3",
    "tsx": "^4.7.1"
  }
}
```

- [ ] **Step 2: Create tsconfig.json**

Write the following contents to `D:/work/projects/flyrank/Assignment 1/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist"
  },
  "include": ["server.ts", "server.test.ts"]
}
```

- [ ] **Step 3: Install dependencies**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
npm install
```
Expected: Successfully installs all packages with no major errors.

- [ ] **Step 4: Commit configuration**

Run these commands inside `D:/work/projects/flyrank`:
```powershell
git add "Assignment 1/package.json" "Assignment 1/tsconfig.json"
git commit -m "chore: initialize project and configure typescript"
```

---

### Task 2: Implement Welcome Endpoint (GET /)

**Files:**
- Create: `Assignment 1/server.test.ts`
- Create: `Assignment 1/server.ts`

- [ ] **Step 1: Write a failing integration test**

Write the following contents to `D:/work/projects/flyrank/Assignment 1/server.test.ts`:
```typescript
import { test } from 'node:test';
import assert from 'node:assert';
import http from 'http';
import { app } from './server';

test('GET / returns welcome JSON', async (t) => {
  const server = http.createServer(app);
  
  // Start server on an ephemeral port
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const address = server.address() as any;
  const port = address.port;
  const url = `http://localhost:${port}/`;

  try {
    const res = await fetch(url);
    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.headers.get('content-type')?.includes('application/json'), true);
    
    const body = await res.json() as any;
    assert.strictEqual(body.message, 'Welcome to the minimal TypeScript API!');
    assert.ok(body.timestamp);
  } finally {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});
```

- [ ] **Step 2: Run test to verify it fails**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
node --import tsx --test server.test.ts
```
Expected: FAIL because `server.ts` does not exist or does not export `app`.

- [ ] **Step 3: Create server.ts and write minimal implementation**

Write the following contents to `D:/work/projects/flyrank/Assignment 1/server.ts`:
```typescript
import express, { Express, Request, Response } from 'express';

const app: Express = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'Welcome to the minimal TypeScript API!',
    timestamp: new Date().toISOString(),
  });
});

// Run server only when executed directly, not when imported for tests
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
  });
}

export { app };
```

- [ ] **Step 4: Run test to verify it passes**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
node --import tsx --test server.test.ts
```
Expected: PASS

- [ ] **Step 5: Commit changes**

Run these commands inside `D:/work/projects/flyrank`:
```powershell
git add "Assignment 1/server.ts" "Assignment 1/server.test.ts"
git commit -m "feat: implement GET / endpoint with integration tests"
```

---

### Task 3: Implement Info Endpoint (GET /api/info)

**Files:**
- Modify: `Assignment 1/server.test.ts`
- Modify: `Assignment 1/server.ts`

- [ ] **Step 1: Write a failing test for GET /api/info**

Modify `D:/work/projects/flyrank/Assignment 1/server.test.ts` by appending this test block:
```typescript
test('GET /api/info returns system status info JSON', async (t) => {
  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const address = server.address() as any;
  const port = address.port;
  const url = `http://localhost:${port}/api/info`;

  try {
    const res = await fetch(url);
    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.headers.get('content-type')?.includes('application/json'), true);
    
    const body = await res.json() as any;
    assert.strictEqual(body.status, 'healthy');
    assert.ok(typeof body.uptime === 'number');
    assert.strictEqual(body.platform, process.platform);
    assert.strictEqual(body.nodeVersion, process.version);
  } finally {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});
```

- [ ] **Step 2: Run test to verify it fails**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
node --import tsx --test server.test.ts
```
Expected: FAIL because `/api/info` is not implemented and returns a 404.

- [ ] **Step 3: Implement the GET /api/info endpoint**

Modify `D:/work/projects/flyrank/Assignment 1/server.ts` to include the route handler:
```typescript
import express, { Express, Request, Response } from 'express';

const app: Express = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'Welcome to the minimal TypeScript API!',
    timestamp: new Date().toISOString(),
  });
});

app.get('/api/info', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    platform: process.platform,
    nodeVersion: process.version,
  });
});

// Run server only when executed directly, not when imported for tests
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
  });
}

export { app };
```

- [ ] **Step 4: Run tests to verify all tests pass**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
node --import tsx --test server.test.ts
```
Expected: PASS (both tests run and pass successfully)

- [ ] **Step 5: Commit changes**

Run these commands inside `D:/work/projects/flyrank`:
```powershell
git add "Assignment 1/server.ts" "Assignment 1/server.test.ts"
git commit -m "feat: implement GET /api/info endpoint and tests"
```

---

### Task 4: Local Verification and GitHub Publication

- [ ] **Step 1: Verify using npm run test**

Run this command inside `D:/work/projects/flyrank/Assignment 1`:
```powershell
npm run test
```
Expected: Successfully executes tests and outputs passing results.

- [ ] **Step 2: Start server locally and test via curl / browser**

1. Run the dev server in the background or terminal:
   ```powershell
   npm run dev
   ```
   Expected: Prints "Server is running at http://localhost:3000".

2. In another terminal or command prompt, execute curl:
   ```powershell
   curl http://localhost:3000/
   curl http://localhost:3000/api/info
   ```
   Expected: Returns the correct JSON formats.

- [ ] **Step 3: Publish to Github**

Run this command inside `D:/work/projects/flyrank`:
```powershell
git push origin main
```
Expected: Pushes the local commits to the remote public repository successfully.
