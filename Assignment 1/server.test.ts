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
