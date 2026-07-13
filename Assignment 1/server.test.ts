import { test } from 'node:test';
import assert from 'node:assert';
import http from 'http';
import { AddressInfo } from 'net';
import { app } from './server';

interface WelcomeResponse {
  message: string;
  timestamp: string;
}

interface InfoResponse {
  status: string;
  uptime: number;
  platform: string;
  nodeVersion: string;
}

test('GET / returns welcome JSON', async (t) => {
  const server = http.createServer(app);
  
  // Start server on an ephemeral port
  await new Promise<void>((resolve, reject) => {
    server.listen(0, () => resolve());
    server.on('error', reject);
  });
  const address = server.address() as AddressInfo;
  const port = address.port;
  const url = `http://localhost:${port}/`;

  try {
    const res = await fetch(url);
    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.headers.get('content-type')?.includes('application/json'), true);
    
    const body = await res.json() as WelcomeResponse;
    assert.strictEqual(body.message, 'Welcome to the minimal TypeScript API!');
    assert.ok(body.timestamp);
  } finally {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});

test('GET /api/info returns system status info JSON', async (t) => {
  const server = http.createServer(app);
  await new Promise<void>((resolve, reject) => {
    server.listen(0, () => resolve());
    server.on('error', reject);
  });
  const address = server.address() as AddressInfo;
  const port = address.port;
  const url = `http://localhost:${port}/api/info`;

  try {
    const res = await fetch(url);
    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.headers.get('content-type')?.includes('application/json'), true);
    
    const body = await res.json() as InfoResponse;
    assert.strictEqual(body.status, 'healthy');
    assert.ok(typeof body.uptime === 'number');
    assert.strictEqual(body.platform, process.platform);
    assert.strictEqual(body.nodeVersion, process.version);
  } finally {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});
