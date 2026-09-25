import { spawnSync, spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const isWin = process.platform === 'win32';
const npm = isWin ? 'npm.cmd' : 'npm';

function install(folder) {
  const dir = join(root, folder);
  if (!existsSync(join(dir, 'node_modules'))) {
    console.log(`\nInstalling ${folder} dependencies...`);
    const r = spawnSync(npm, ['install', '--no-audit', '--no-fund'], { cwd: dir, stdio: 'inherit' });
    if (r.status !== 0) {
      console.error(`\n${folder} dependency installation failed.`);
      process.exit(r.status ?? 1);
    }
  }
}

install('server');
install('client');

console.log('\nKISSAN SATHI is starting...');
console.log('Frontend: http://localhost:5173');
console.log('API:      http://localhost:4000/health');

if (isWin) {
  const serverDir = join(root, 'server');
  const clientDir = join(root, 'client');
  const serverCmd = `cd /d "${serverDir}" && npm run dev`;
  const clientCmd = `cd /d "${clientDir}" && npm run dev -- --host 127.0.0.1`;
  const server = spawn('cmd.exe', ['/d', '/k', serverCmd], { detached: true, stdio: 'ignore' });
  const client = spawn('cmd.exe', ['/d', '/k', clientCmd], { detached: true, stdio: 'ignore' });
  server.unref();
  client.unref();
  console.log('\nTwo command windows have been opened. Keep both open.');
  console.log('Open http://localhost:5173 after a few seconds.');
} else {
  const server = spawn(npm, ['run', 'dev'], { cwd: join(root, 'server'), stdio: 'inherit' });
  const client = spawn(npm, ['run', 'dev', '--', '--host', '127.0.0.1'], { cwd: join(root, 'client'), stdio: 'inherit' });
  let stopping = false;
  const stop = (code = 0) => { if (stopping) return; stopping = true; server.kill('SIGTERM'); client.kill('SIGTERM'); setTimeout(() => process.exit(code), 250); };
  process.on('SIGINT', () => stop(0));
  process.on('SIGTERM', () => stop(0));
  server.on('exit', code => { if (!stopping && code !== 0) stop(code ?? 1); });
  client.on('exit', code => { if (!stopping && code !== 0) stop(code ?? 1); });
}
