# WorkAny API 接口文档

## 概述

WorkAny API 是一个基于 Hono 框架构建的 TypeScript API 服务器，提供 AI Agent 执行、沙箱环境、文件操作等功能。

**基础 URL**: `http://localhost:<port>`

**版本**: v0.1.16

---

## 目录

- [Agent 接口](#agent-接口)
- [Sandbox 接口](#sandbox-接口)
- [Health 接口](#health-接口)
- [MCP 接口](#mcp-接口)
- [Providers 接口](#providers-接口)
- [Files 接口](#files-接口)
- [Preview 接口](#preview-接口)

---

## Agent 接口

AI Agent 执行和任务管理相关接口。

### 1. 创建计划（规划阶段）

**POST** `/agent/plan`

创建执行计划，不执行任务。

#### 请求体

```typescript
{
  prompt: string;           // 必需：任务描述
  modelConfig?: {           // 可选：AI 模型配置
    apiKey?: string;
    baseUrl?: string;
    model?: string;
  };
}
```

#### 响应

**Content-Type**: `text/event-stream` (SSE 流式响应)

#### SSE 事件类型

- `plan_start`: 规划开始
- `plan_step`: 规划步骤
- `plan_complete`: 规划完成
- `error`: 错误信息

#### 示例

```bash
curl -X POST http://localhost:3000/agent/plan \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "创建一个用户登录页面",
    "modelConfig": {
      "model": "claude-sonnet-4-5-20250929"
    }
  }'
```

---

### 2. 执行计划

**POST** `/agent/execute`

执行已批准的计划。

#### 请求体

```typescript
{
  planId: string;           // 必需：计划 ID
  prompt?: string;          // 可选：原始提示词
  workDir?: string;         // 可选：工作目录
  taskId?: string;          // 可选：任务 ID
  modelConfig?: {           // 可选：AI 模型配置
    apiKey?: string;
    baseUrl?: string;
    model?: string;
  };
  sandboxConfig?: {         // 可选：沙箱配置
    enabled: boolean;
    provider?: 'codex' | 'native' | 'docker';
  };
  skillsConfig?: {          // 可选：技能配置
    enabled: boolean;
    userDirEnabled: boolean;
    appDirEnabled: boolean;
    skillsPath?: string;
  };
  mcpConfig?: {             // 可选：MCP 配置
    enabled: boolean;
    userDirEnabled: boolean;
    appDirEnabled: boolean;
    mcpConfigPath?: string;
  };
}
```

#### 响应

**Content-Type**: `text/event-stream` (SSE 流式响应)

#### 示例

```bash
curl -X POST http://localhost:3000/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "planId": "plan_12345",
    "prompt": "创建一个用户登录页面",
    "workDir": "/Users/user/projects"
  }'
```

---

### 3. 直接执行（一体化）

**POST** `/agent/`

直接执行任务（规划 + 执行一体化）。

#### 请求体

```typescript
{
  prompt: string;           // 必需：任务描述
  sessionId?: string;       // 可选：会话 ID
  conversation?: Array<{    // 可选：对话历史
    role: 'user' | 'assistant';
    content: string;
  }>;
  workDir?: string;         // 可选：工作目录
  taskId?: string;          // 可选：任务 ID
  modelConfig?: {           // 可选：AI 模型配置
    apiKey?: string;
    baseUrl?: string;
    model?: string;
  };
  sandboxConfig?: {         // 可选：沙箱配置
    enabled: boolean;
    provider?: 'codex' | 'native' | 'docker';
  };
  images?: Array<{          // 可选：图片数据
    data: string;           // base64 编码的图片数据
    mimeType: string;       // 图片 MIME 类型
  }>;
  skillsConfig?: {          // 可选：技能配置
    enabled: boolean;
    userDirEnabled: boolean;
    appDirEnabled: boolean;
    skillsPath?: string;
  };
  mcpConfig?: {             // 可选：MCP 配置
    enabled: boolean;
    userDirEnabled: boolean;
    appDirEnabled: boolean;
    mcpConfigPath?: string;
  };
}
```

#### 响应

**Content-Type**: `text/event-stream` (SSE 流式响应)

#### 示例

```bash
curl -X POST http://localhost:3000/agent/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "创建一个用户登录页面",
    "workDir": "/Users/user/projects"
  }'
```

---

### 4. 停止任务

**POST** `/agent/stop/:sessionId`

停止正在运行的任务。

#### 参数

- `sessionId` (路径参数): 会话 ID

#### 响应

```json
{
  "status": "stopped"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/agent/stop/session_12345
```

---

### 5. 获取会话状态

**GET** `/agent/session/:sessionId`

获取会话的当前状态。

#### 参数

- `sessionId` (路径参数): 会话 ID

#### 响应

```json
{
  "id": "session_12345",
  "createdAt": "2025-01-15T10:30:00.000Z",
  "phase": "execute",
  "isAborted": false
}
```

#### 示例

```bash
curl http://localhost:3000/agent/session/session_12345
```

---

### 6. 获取计划详情

**GET** `/agent/plan/:planId`

获取已保存的计划详情。

#### 参数

- `planId` (路径参数): 计划 ID

#### 响应

```json
{
  "id": "plan_12345",
  "prompt": "创建一个用户登录页面",
  "steps": [...],
  "createdAt": "2025-01-15T10:30:00.000Z"
}
```

#### 示例

```bash
curl http://localhost:3000/agent/plan/plan_12345
```

---

## Sandbox 接口

沙箱执行环境相关接口。

### 1. 检查沙箱可用性

**GET** `/sandbox/available`

检查沙箱是否可用，返回使用的提供商信息。

#### 响应

```json
{
  "available": true,
  "provider": "codex",
  "providerName": "Codex Sandbox",
  "isolation": "vm",
  "mode": "vm",
  "message": "Codex sandbox is available",
  "usedFallback": false,
  "fallbackReason": null
}
```

#### 示例

```bash
curl http://localhost:3000/sandbox/available
```

---

### 2. 获取可用镜像

**GET** `/sandbox/images`

获取可用的沙箱镜像列表。

#### 响应

```json
{
  "images": {
    "node": "node:20",
    "python": "python:3.12",
    "alpine": "alpine:latest"
  },
  "default": "node:20"
}
```

#### 示例

```bash
curl http://localhost:3000/sandbox/images
```

---

### 3. 执行命令

**POST** `/sandbox/exec`

在沙箱中执行命令。

#### 请求体

```typescript
{
  command: string;          // 必需：要执行的命令
  args?: string[];          // 可选：命令参数
  image?: string;           // 可选：镜像名称（默认: node:20）
  cwd?: string;             // 可选：工作目录（默认: /workspace）
  env?: Record<string, string>;  // 可选：环境变量
  provider?: 'codex' | 'native' | 'docker';  // 可选：沙箱提供商
  timeout?: number;         // 可选：超时时间（毫秒）
}
```

#### 响应

```json
{
  "success": true,
  "provider": "codex",
  "providerName": "Codex Sandbox",
  "providerInfo": {
    "type": "codex",
    "name": "Codex Sandbox",
    "isolation": "vm",
    "isolationLabel": "VM 硬件隔离"
  },
  "exitCode": 0,
  "stdout": "output...",
  "stderr": "",
  "duration": 1234
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/sandbox/exec \
  -H "Content-Type: application/json" \
  -d '{
    "command": "node",
    "args": ["-v"],
    "image": "node:20"
  }'
```

---

### 4. 运行脚本文件

**POST** `/sandbox/run/file`

在沙箱中运行脚本文件，自动检测运行时。

#### 请求体

```typescript
{
  filePath: string;         // 必需：脚本文件路径
  args?: string[];          // 可选：脚本参数
  workDir: string;          // 必需：工作目录
  env?: Record<string, string>;  // 可选：环境变量
  packages?: string[];      // 可选：需要安装的包
  provider?: 'codex' | 'native' | 'docker';  // 可选：沙箱提供商
  timeout?: number;         // 可选：超时时间（毫秒，默认: 120000）
}
```

#### 响应

```json
{
  "success": true,
  "runtime": "node",
  "provider": "codex",
  "providerName": "Codex Sandbox",
  "providerInfo": {
    "type": "codex",
    "name": "Codex Sandbox",
    "isolation": "vm",
    "isolationLabel": "VM 硬件隔离"
  },
  "exitCode": 0,
  "stdout": "output...",
  "stderr": "",
  "duration": 5000
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/sandbox/run/file \
  -H "Content-Type: application/json" \
  -d '{
    "filePath": "/workspace/script.js",
    "workDir": "/workspace"
  }'
```

---

### 5. 运行 Node.js 脚本内容

**POST** `/sandbox/run/node`

在沙箱中运行 Node.js 脚本内容。

#### 请求体

```typescript
{
  script: string;           // 必需：脚本内容
  packages?: string[];      // 可选：需要安装的包
  cwd?: string;             // 可选：工作目录（默认: /tmp）
  env?: Record<string, string>;  // 可选：环境变量
  provider?: 'codex' | 'native' | 'docker';  // 可选：沙箱提供商
  timeout?: number;         // 可选：超时时间（毫秒，默认: 120000）
}
```

#### 响应

```json
{
  "success": true,
  "provider": "codex",
  "exitCode": 0,
  "stdout": "output...",
  "stderr": "",
  "duration": 3000
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/sandbox/run/node \
  -H "Content-Type: application/json" \
  -d '{
    "script": "console.log(\"Hello World\")"
  }'
```

---

### 6. 流式执行命令

**POST** `/sandbox/exec/stream`

以流式方式执行命令，实时返回输出。

#### 请求体

```typescript
{
  command: string;          // 必需：要执行的命令
  args?: string[];          // 可选：命令参数
  image?: string;           // 可选：镜像名称
  cwd?: string;             // 可选：工作目录
  env?: Record<string, string>;  // 可选：环境变量
  provider?: 'codex' | 'native' | 'docker';  // 可选：沙箱提供商
}
```

#### 响应

**Content-Type**: `text/event-stream` (SSE 流式响应)

#### SSE 事件类型

- `started`: 执行开始
- `stdout`: 标准输出
- `stderr`: 标准错误
- `done`: 执行完成
- `error`: 错误信息

#### 示例

```bash
curl -X POST http://localhost:3000/sandbox/exec/stream \
  -H "Content-Type: application/json" \
  -d '{
    "command": "npm",
    "args": ["install"]
  }'
```

---

### 7. 停止所有沙箱

**POST** `/sandbox/stop-all`

停止所有正在运行的沙箱实例。

#### 响应

```json
{
  "success": true,
  "message": "All sandbox providers stopped"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/sandbox/stop-all
```

---

## Health 接口

系统健康检查和依赖管理相关接口。

### 1. 基础健康检查

**GET** `/health/`

获取系统基础健康状态。

#### 响应

```json
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "uptime": 3600
}
```

#### 示例

```bash
curl http://localhost:3000/health/
```

---

### 2. 检查依赖状态

**GET** `/health/dependencies`

检查所有依赖的安装状态。

#### 响应

```json
{
  "success": true,
  "allRequiredInstalled": true,
  "claudeCode": true,
  "codex": false,
  "dependencies": [
    {
      "id": "claude-code",
      "name": "Claude Code",
      "description": "Agent Runtime for task processing",
      "required": true,
      "installed": true,
      "version": "1.0.0",
      "installUrl": "https://docs.anthropic.com/en/docs/claude-code/getting-started"
    },
    {
      "id": "codex",
      "name": "Codex",
      "description": "Sandbox for script execution",
      "required": false,
      "installed": false,
      "installUrl": "https://github.com/openai/codex-cli"
    }
  ]
}
```

#### 示例

```bash
curl http://localhost:3000/health/dependencies
```

---

### 3. 获取依赖安装命令

**GET** `/health/dependencies/:id/install-commands`

获取指定依赖的安装命令。

#### 参数

- `id` (路径参数): 依赖 ID（如 `claude-code`, `codex`）

#### 响应

```json
{
  "success": true,
  "id": "claude-code",
  "name": "Claude Code",
  "commands": {
    "npm": "npm install -g @anthropic-ai/claude-code",
    "brew": "brew install claude-code",
    "manual": "Visit https://docs.anthropic.com/claude-code/install"
  },
  "installUrl": "https://docs.anthropic.com/en/docs/claude-code/getting-started"
}
```

#### 示例

```bash
curl http://localhost:3000/health/dependencies/claude-code/install-commands
```

---

### 4. 安装依赖

**POST** `/health/dependencies/:id/install`

安装指定的依赖。

#### 参数

- `id` (路径参数): 依赖 ID

#### 请求体

```typescript
{
  method?: 'npm' | 'brew' | 'auto';  // 可选：安装方法（默认: auto）
}
```

#### 响应

```json
{
  "success": true,
  "installed": true,
  "version": "1.0.0",
  "output": "安装输出...",
  "message": "Claude Code installed successfully"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/health/dependencies/claude-code/install \
  -H "Content-Type: application/json" \
  -d '{
    "method": "auto"
  }'
```

---

### 5. 检查单个依赖

**GET** `/health/dependencies/:id`

检查单个依赖的状态。

#### 参数

- `id` (路径参数): 依赖 ID

#### 响应

```json
{
  "success": true,
  "id": "claude-code",
  "name": "Claude Code",
  "description": "Agent Runtime for task processing",
  "required": true,
  "installed": true,
  "version": "1.0.0",
  "location": "native",
  "installUrl": "https://docs.anthropic.com/en/docs/claude-code/getting-started"
}
```

#### location 说明

- `native`: 本地安装
- `wsl`: WSL 环境（Windows）
- `sidecar`: 捆绑的侧边加载版本

#### 示例

```bash
curl http://localhost:3000/health/dependencies/claude-code
```

---

## MCP 接口

Model Context Protocol 配置管理相关接口。

### 1. 读取 MCP 配置

**GET** `/mcp/config`

读取 WorkAny 的 MCP 配置文件。

#### 响应

```json
{
  "success": true,
  "data": {
    "mcpServers": {
      "server1": {
        "command": "node",
        "args": ["./server.js"]
      }
    }
  },
  "path": "/Users/user/.workany/mcp.json"
}
```

#### 示例

```bash
curl http://localhost:3000/mcp/config
```

---

### 2. 写入 MCP 配置

**POST** `/mcp/config`

写入 WorkAny 的 MCP 配置文件。

#### 请求体

```typescript
{
  mcpServers: Record<string, {
    command?: string;       // stdio 模式：命令
    args?: string[];        // stdio 模式：参数
    env?: Record<string, string>;  // stdio 模式：环境变量
    url?: string;           // HTTP 模式：URL
    headers?: Record<string, string>;  // HTTP 模式：请求头
  }>;
}
```

#### 响应

```json
{
  "success": true,
  "message": "MCP config saved",
  "path": "/Users/user/.workany/mcp.json"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/mcp/config \
  -H "Content-Type: application/json" \
  -d '{
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
      }
    }
  }'
```

---

### 3. 获取配置文件路径

**GET** `/mcp/path`

获取 MCP 配置文件的路径。

#### 响应

```json
{
  "success": true,
  "path": "/Users/user/.workany/mcp.json"
}
```

#### 示例

```bash
curl http://localhost:3000/mcp/path
```

---

### 4. 获取所有配置

**GET** `/mcp/all-configs`

获取所有来源的 MCP 配置（WorkAny 和 Claude）。

#### 响应

```json
{
  "success": true,
  "configs": [
    {
      "name": "workany",
      "path": "/Users/user/.workany/mcp.json",
      "exists": true,
      "servers": {
        "server1": {...}
      }
    },
    {
      "name": "claude",
      "path": "/Users/user/.claude/settings.json",
      "exists": true,
      "servers": {
        "server2": {...}
      }
    }
  ]
}
```

#### 示例

```bash
curl http://localhost:3000/mcp/all-configs
```

---

## Providers 接口

沙箱和 Agent 提供商管理相关接口。

### 1. 列出所有沙箱提供商

**GET** `/providers/sandbox`

列出所有沙箱提供商及其元数据。

#### 响应

```json
{
  "providers": [
    {
      "type": "codex",
      "name": "Codex Sandbox",
      "description": "High-security VM-based sandbox",
      "isolation": "vm",
      "available": true,
      "current": true
    },
    {
      "type": "native",
      "name": "Native Sandbox",
      "description": "Process-based isolation",
      "isolation": "process",
      "available": true,
      "current": false
    }
  ],
  "current": "codex"
}
```

#### 示例

```bash
curl http://localhost:3000/providers/sandbox
```

---

### 2. 列出可用的沙箱提供商

**GET** `/providers/sandbox/available`

列出当前系统中可用的沙箱提供商。

#### 响应

```json
{
  "available": ["codex", "native"]
}
```

#### 示例

```bash
curl http://localhost:3000/providers/sandbox/available
```

---

### 3. 获取沙箱提供商详情

**GET** `/providers/sandbox/:type`

获取指定沙箱提供商的详细信息。

#### 参数

- `type` (路径参数): 提供商类型

#### 响应

```json
{
  "type": "codex",
  "name": "Codex Sandbox",
  "description": "High-security VM-based sandbox",
  "isolation": "vm",
  "available": true,
  "current": true
}
```

#### 示例

```bash
curl http://localhost:3000/providers/sandbox/codex
```

---

### 4. 切换沙箱提供商

**POST** `/providers/sandbox/switch`

切换到不同的沙箱提供商。

#### 请求体

```typescript
{
  type: string;             // 必需：提供商类型
  config?: Record<string, unknown>;  // 可选：提供商配置
}
```

#### 响应

```json
{
  "success": true,
  "current": "native",
  "message": "Switched to sandbox provider: native"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/providers/sandbox/switch \
  -H "Content-Type: application/json" \
  -d '{
    "type": "native"
  }'
```

---

### 5. 列出所有 Agent 提供商

**GET** `/providers/agents`

列出所有 Agent 提供商及其元数据。

#### 响应

```json
{
  "providers": [
    {
      "type": "claude",
      "name": "Claude Agent",
      "description": "Anthropic Claude AI agent",
      "available": true,
      "current": true
    },
    {
      "type": "codex",
      "name": "Codex Agent",
      "description": "OpenAI Codex agent",
      "available": false,
      "current": false
    }
  ],
  "current": "claude"
}
```

#### 示例

```bash
curl http://localhost:3000/providers/agents
```

---

### 6. 列出可用的 Agent 提供商

**GET** `/providers/agents/available`

列出当前系统中可用的 Agent 提供商。

#### 响应

```json
{
  "available": ["claude"]
}
```

#### 示例

```bash
curl http://localhost:3000/providers/agents/available
```

---

### 7. 获取 Agent 提供商详情

**GET** `/providers/agents/:type`

获取指定 Agent 提供商的详细信息。

#### 参数

- `type` (路径参数): 提供商类型

#### 响应

```json
{
  "type": "claude",
  "name": "Claude Agent",
  "description": "Anthropic Claude AI agent",
  "available": true,
  "current": true
}
```

#### 示例

```bash
curl http://localhost:3000/providers/agents/claude
```

---

### 8. 切换 Agent 提供商

**POST** `/providers/agents/switch`

切换到不同的 Agent 提供商。

#### 请求体

```typescript
{
  type: string;             // 必需：提供商类型
  config?: Record<string, unknown>;  // 可选：提供商配置（包含 apiKey, baseUrl, model 等）
}
```

#### 响应

```json
{
  "success": true,
  "current": "claude",
  "message": "Switched to agent provider: claude"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/providers/agents/switch \
  -H "Content-Type: application/json" \
  -d '{
    "type": "claude",
    "config": {
      "apiKey": "sk-...",
      "model": "claude-sonnet-4-5-20250929"
    }
  }'
```

---

### 9. 同步设置

**POST** `/providers/settings/sync`

将前端设置同步到后端。

#### 请求体

```typescript
{
  sandboxProvider?: string;  // 可选：沙箱提供商
  sandboxConfig?: Record<string, unknown>;  // 可选：沙箱配置
  agentProvider?: string;    // 可选：Agent 提供商
  agentConfig?: Record<string, unknown>;  // 可选：Agent 配置（包含 apiKey, baseUrl, model）
  defaultProvider?: string;  // 可选：默认 AI 提供商
  defaultModel?: string;     // 可选：默认模型
}
```

#### 响应

```json
{
  "success": true,
  "config": {
    "sandbox": {
      "type": "codex",
      "config": {}
    },
    "agent": {
      "type": "claude",
      "config": {
        "apiKey": "sk-...",
        "model": "claude-sonnet-4-5-20250929"
      }
    }
  }
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/providers/settings/sync \
  -H "Content-Type: application/json" \
  -d '{
    "sandboxProvider": "codex",
    "agentProvider": "claude",
    "agentConfig": {
      "apiKey": "sk-...",
      "model": "claude-sonnet-4-5-20250929"
    }
  }'
```

---

### 10. 获取当前配置

**GET** `/providers/config`

获取当前的提供商配置。

#### 响应

```json
{
  "sandbox": {
    "type": "codex",
    "config": {}
  },
  "agent": {
    "type": "claude",
    "config": {
      "apiKey": "sk-...",
      "model": "claude-sonnet-4-5-20250929"
    }
  }
}
```

#### 示例

```bash
curl http://localhost:3000/providers/config
```

---

## Files 接口

文件系统操作相关接口。

### 1. 读取目录

**POST** `/files/readdir`

递归读取目录内容。

#### 请求体

```typescript
{
  path: string;             // 必需：目录路径
  maxDepth?: number;        // 可选：最大深度（默认: 3）
}
```

#### 响应

```json
{
  "success": true,
  "path": "/Users/user/projects",
  "files": [
    {
      "name": "src",
      "path": "/Users/user/projects/src",
      "isDir": true,
      "children": [...]
    },
    {
      "name": "package.json",
      "path": "/Users/user/projects/package.json",
      "isDir": false
    }
  ]
}
```

#### 安全限制

- 只能读取用户主目录（`~/`）和临时目录（`/tmp`）下的文件
- 自动忽略常见文件和目录（如 `node_modules`, `.git` 等）

#### 示例

```bash
curl -X POST http://localhost:3000/files/readdir \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/projects",
    "maxDepth": 2
  }'
```

---

### 2. 检查路径状态

**POST** `/files/stat`

检查路径是否存在及其类型。

#### 请求体

```typescript
{
  path: string;             // 必需：文件/目录路径
}
```

#### 响应

```json
{
  "exists": true,
  "isFile": true,
  "isDirectory": false,
  "size": 1024,
  "mtime": "2025-01-15T10:30:00.000Z"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/files/stat \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/file.txt"
  }'
```

---

### 3. 读取文件内容

**POST** `/files/read`

读取文本文件内容。

#### 请求体

```typescript
{
  path: string;             // 必需：文件路径
}
```

#### 响应

```json
{
  "success": true,
  "content": "文件内容..."
}
```

#### 安全限制

- 只能读取用户主目录（`~/`）和临时目录（`/tmp`）下的文件

#### 示例

```bash
curl -X POST http://localhost:3000/files/read \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/file.txt"
  }'
```

---

### 4. 读取二进制文件

**POST** `/files/read-binary`

以 base64 格式读取二进制文件。

#### 请求体

```typescript
{
  path: string;             // 必需：文件路径
}
```

#### 响应

```json
{
  "success": true,
  "fileName": "image.png",
  "content": "base64编码的内容...",
  "size": 12345
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/files/read-binary \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/image.png"
  }'
```

---

### 5. 获取技能目录

**GET** `/files/skills-dir`

获取技能目录路径。

#### 响应

```json
{
  "path": "/Users/user/.workany/skills",
  "exists": true,
  "directories": [
    {
      "name": "workany",
      "path": "/Users/user/.workany/skills",
      "exists": true
    },
    {
      "name": "claude",
      "path": "/Users/user/.claude/skills",
      "exists": true
    }
  ]
}
```

#### 示例

```bash
curl http://localhost:3000/files/skills-dir
```

---

### 6. 检测代码编辑器

**GET** `/files/detect-editor`

检测系统中可用的代码编辑器。

#### 响应

```json
{
  "success": true,
  "editor": "Cursor",
  "command": "cursor"
}
```

#### 支持的编辑器

1. Cursor
2. VS Code
3. VS Code Insiders
4. Sublime Text
5. Atom
6. WebStorm
7. PyCharm

#### 示例

```bash
curl http://localhost:3000/files/detect-editor
```

---

### 7. 在编辑器中打开文件

**POST** `/files/open-in-editor`

在检测到的代码编辑器中打开文件。

#### 请求体

```typescript
{
  path: string;             // 必需：文件路径
}
```

#### 响应

```json
{
  "success": true,
  "editor": "Cursor"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/files/open-in-editor \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/file.ts"
  }'
```

---

### 8. 打开文件（系统默认）

**POST** `/files/open`

使用系统默认应用打开文件或目录。

#### 请求体

```typescript
{
  path: string;             // 必需：文件/目录路径（支持 ~ 路径）
}
```

#### 响应

```json
{
  "success": true
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/files/open \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/user/projects"
  }'
```

---

## Preview 接口

Vite 预览服务器管理相关接口。

### 1. 检查 Node.js 可用性

**GET** `/preview/node-available`

检查系统是否安装了 Node.js（用于 Live Preview）。

#### 响应

```json
{
  "available": true
}
```

#### 示例

```bash
curl http://localhost:3000/preview/node-available
```

---

### 2. 启动预览服务器

**POST** `/preview/start`

为指定任务启动 Vite 预览服务器。

#### 请求体

```typescript
{
  taskId: string;           // 必需：任务 ID
  workDir: string;          // 必需：工作目录
  port?: number;            // 可选：端口号（自动分配）
}
```

#### 响应

```json
{
  "status": "running",
  "taskId": "task_12345",
  "url": "http://localhost:5173",
  "port": 5173
}
```

#### status 可能的值

- `running`: 正在运行
- `stopped`: 已停止
- `error`: 错误

#### 示例

```bash
curl -X POST http://localhost:3000/preview/start \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task_12345",
    "workDir": "/Users/user/projects/my-app"
  }'
```

---

### 3. 停止预览服务器

**POST** `/preview/stop`

停止指定任务的预览服务器。

#### 请求体

```typescript
{
  taskId: string;           // 必需：任务 ID
}
```

#### 响应

```json
{
  "status": "stopped",
  "taskId": "task_12345"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/preview/stop \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task_12345"
  }'
```

---

### 4. 获取预览服务器状态

**GET** `/preview/status/:taskId`

获取指定任务的预览服务器状态。

#### 参数

- `taskId` (路径参数): 任务 ID

#### 响应

```json
{
  "status": "running",
  "taskId": "task_12345",
  "url": "http://localhost:5173",
  "port": 5173
}
```

#### 示例

```bash
curl http://localhost:3000/preview/status/task_12345
```

---

### 5. 停止所有预览服务器

**POST** `/preview/stop-all`

停止所有正在运行的预览服务器。

#### 响应

```json
{
  "success": true,
  "message": "All preview servers stopped"
}
```

#### 示例

```bash
curl -X POST http://localhost:3000/preview/stop-all
```

---

## 错误响应格式

所有接口在出错时返回统一的错误格式：

```json
{
  "error": "错误描述信息"
}
```

或带 HTTP 状态码的详细错误：

```json
{
  "success": false,
  "error": "错误描述信息",
  "details": {}  // 可选的额外信息
}
```

### 常见 HTTP 状态码

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `403 Forbidden`: 无权限访问
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

---

## SSE 流式响应

部分接口（如 Agent 执行）使用 Server-Sent Events (SSE) 返回流式数据。

### 连接示例

```javascript
const eventSource = new EventSource('http://localhost:3000/agent/plan');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);

  if (data.type === 'done') {
    eventSource.close();
  }
};

eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
  eventSource.close();
};
```

### Fetch API 示例

```javascript
const response = await fetch('http://localhost:3000/agent/plan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: '创建一个登录页面' })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const text = decoder.decode(value);
  const lines = text.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      console.log('Received:', data);
    }
  }
}
```

---

## 安全说明

### 文件访问限制

所有文件操作接口都受到以下限制：

1. 只能访问用户主目录（`~/`）和系统临时目录（`/tmp`）
2. 路径会被规范化处理
3. Windows 下路径比较不区分大小写

### API 密钥安全

- API 密钥不应在日志中完整输出
- 前端传输时应使用 HTTPS
- 建议通过环境变量或配置文件管理密钥

---

## 开发和测试

### 启动开发服务器

```bash
cd src-api
pnpm dev
```

### 构建生产版本

```bash
pnpm build
pnpm start
```

### API 测试示例

使用 `curl` 测试接口：

```bash
# 健康检查
curl http://localhost:3000/health/

# 检查依赖
curl http://localhost:3000/health/dependencies

# 执行 Agent 任务
curl -X POST http://localhost:3000/agent/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "创建一个 Hello World 页面"}'
```

---

## 更新日志

### v0.1.16

- 添加 Agent 两阶段执行模式（规划 + 执行）
- 优化沙箱提供商切换逻辑
- 改进依赖检测和自动安装
- 支持多种沙箱提供商（Codex、Native、Docker）
- 添加 MCP 配置管理

---

## 技术栈

- **框架**: Hono v4.7.10
- **运行时**: Node.js 20+
- **语言**: TypeScript 5.x
- **AI SDK**: @anthropic-ai/claude-agent-sdk v0.2.7
- **沙箱**: @anthropic-ai/sandbox-runtime v0.0.28
- **MCP**: @modelcontextprotocol/sdk v1.25.2

---

## 许可证

请参考项目根目录的 LICENSE 文件。
