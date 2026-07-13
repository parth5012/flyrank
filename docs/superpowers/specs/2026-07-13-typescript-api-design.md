# Design Spec: Minimal TypeScript API Server

This document outlines the design for the smallest possible TypeScript backend server, featuring two JSON endpoints, testing setups, and publication instructions.

## 1. Requirements & Success Criteria
- **Language & Runtime**: TypeScript, Node.js.
- **Framework**: Express.js (single-file setup).
- **Location**: `Assignment 1` folder.
- **Endpoints**:
  - `GET /`: Returns a JSON welcome message and current timestamp.
  - `GET /api/info`: Returns JSON containing application health and system metadata (uptime, platform, Node version).
- **Verification**: Verified using `curl` and a web browser.
- **Git Repository**: All files will be committed and pushed to the public GitHub repository at `https://github.com/parth5012/flyrank.git`.

## 2. Project File Structure
All code and configurations reside inside `D:/work/projects/flyrank/Assignment 1`:
```
Assignment 1/
├── package.json      # Dependencies and execution scripts
├── tsconfig.json     # TypeScript configuration
└── server.ts         # Server entry point and endpoint handlers
```

## 3. Configuration & Dependency Specification

### package.json
- **Dependencies**: `express`
- **DevDependencies**: `typescript`, `@types/node`, `@types/express`, `tsx`
- **Scripts**:
  - `"dev"`: `"tsx server.ts"` (Runs the server locally in development mode)

### tsconfig.json
A basic TypeScript configuration:
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
  "include": ["server.ts"]
}
```

## 4. Endpoint Definitions

### Endpoint 1: Welcome API
- **Route**: `GET /`
- **Request Type**: None
- **Response Format**: `application/json`
- **Response Shape**:
  ```json
  {
    "message": "Welcome to the minimal TypeScript API!",
    "timestamp": "2026-07-13T17:26:23.000Z"
  }
  ```

### Endpoint 2: System Status Info
- **Route**: `GET /api/info`
- **Request Type**: None
- **Response Format**: `application/json`
- **Response Shape**:
  ```json
  {
    "status": "healthy",
    "uptime": 12.34,
    "platform": "win32",
    "nodeVersion": "v18.x.x"
  }
  ```

## 5. Verification Plan
Once the server is running on port `3000`:
1. **Browser Test**: Open `http://localhost:3000/` and `http://localhost:3000/api/info` in a web browser.
2. **Curl Test**: Run `curl http://localhost:3000/` and `curl http://localhost:3000/api/info` from the command line to verify the JSON responses.

## 6. GitHub Publication Plan
1. Run `git add` to stage the new files under `Assignment 1` and `docs/superpowers/specs/`.
2. Run `git commit -m "feat: implement minimal TypeScript Express API"` to create a commit.
3. Run `git push origin main` to publish to the public repository.
