# 技术架构

配套：功能规范 v2

---

## 1. 堆栈

| 层 | 技术 |
|-------|-----------|
| 后端 | Django 5.x、Django REST 框架 |
| 前端 | Django 模板、HTMX、Alpine.js |
| CSS | Tailwind CSS 4 通过 django-tailwind |
| 数据库 | PostgreSQL 16+（也用作作业队列） |
| 后台作业 | django-background-tasks（PostgreSQL 支持，无 Redis/Celery） |
| 缓存 | Redis（可选 - 启动时不需要，稍后添加以获得实时功能） |
| 媒体存储 | 本地文件系统（默认）或 S3 兼容（Cloudflare R2、AWS S3、MinIO、Backblaze B2） |
| 媒体处理 | FFmpeg（视频）、Pillow（图像） |
| 电子邮件 | 重新发送（云）、SMTP-可配置（自托管）|
| Web 服务器 | 球童后面的 Gunicorn (auto-HTTPS) |

---

## 2. 项目结构

```
project/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/               # F-5.1: Auth, registration, 2FA
│   ├── organizations/          # F-1.1: Org management
│   ├── workspaces/             # F-1.2: Workspace CRUD
│   ├── members/                # F-1.3: RBAC, invitations
│   ├── client_portal/          # F-1.4: Client views, magic links
│   ├── credentials/            # F-1.5: Platform API credentials
│   ├── settings_manager/       # F-1.6: Configurable defaults
│   ├── onboarding/             # F-1.7: Client onboarding, checklist
│   ├── composer/               # F-2.1: Post composer
│   ├── approvals/              # F-2.2: Approval workflows
│   ├── calendar/               # F-2.3: Calendar, scheduling, queues
│   ├── publisher/              # F-2.4: Publishing engine
│   ├── social_accounts/        # F-2.5: OAuth connection flows
│   ├── inbox/                  # F-3.1: Unified social inbox
│   ├── analytics/              # F-4.1, F-4.2: Analytics
│   ├── reports/                # F-4.3: Report builder
│   ├── whitelabel/             # F-5.2: White-label config
│   ├── integrations/           # F-5.3: Canva, stock media, Slack, AI, API, webhooks
│   ├── media_library/          # F-6.1: Media assets
│   └── notifications/          # F-7.1: Notification engine
├── providers/                  # Social platform provider modules
│   ├── base.py                 # Abstract SocialProvider interface
│   ├── facebook.py
│   ├── instagram.py
│   ├── linkedin.py
│   ├── tiktok.py
│   ├── youtube.py
│   ├── pinterest.py
│   ├── threads.py
│   ├── bluesky.py
│   ├── google_business.py
│   └── mastodon.py
├── theme/                      # django-tailwind theme app
│   └── static_src/
│       ├── src/
│       │   └── styles.css      # Tailwind directives + custom CSS
│       └── tailwind.config.js
├── templates/
│   ├── base.html
│   └── components/             # Reusable HTMX partials
├── static/                     # Compiled CSS, vendored JS (HTMX, Alpine.js)
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── railway.toml
├── render.yaml
├── Procfile                    # Heroku
├── app.json                    # Heroku "Deploy" button manifest
└── README.md
```

---

## 3. 前端架构

服务器渲染 HTML。应用程序没有 JavaScript 构建步骤。只有 Tailwind CSS 需要构建步骤（由 django-tailwind 处理）。

**顺风CSS：**
- 通过 `django-tailwind` 进行管理，它将 Tailwind CLI 包装在 Django 应用程序中。
- 开发：`python manage.py tailwind start` 个手表模板并重新编译。
- Production: Dockerfile 中的 `python manage.py tailwind build` 生成缩小后的 CSS。
- `tailwind.config.js` 内容路径包括用于正确清除的所有模板目录。
- 白标签主题 (F-5.2)：代理品牌颜色在运行时作为 CSS 自定义属性注入到 `<html>` 元素上，覆盖 Tailwind 的默认颜色标记。这允许按组织进行颜色自定义，而无需重建 CSS。

**HTMX 个句柄：**
- 页面部分、表单提交、视图切换，无需完全重新加载。
- Composer 实时预览：去抖 (500ms) `hx-post` 返回渲染预览 HTML。
- 批准操作：通过 `hx-post` + `hx-swap` 内联状态更新。
- 收件箱无限滚动：`hx-get` 与 `hx-trigger="revealed"`。
- 日历视图切换：通过 `hx-get` 交换日历容器。
- 通知徽章：每 30 秒轮询一次（稍后升级到带有 Redis 的 WebSocket）。

**Alpine.js 句柄（仅限客户端）：**
- 拖放：日历重新安排、媒体重新排序、报告部分重新排序。掉落时发射 `hx-post`。
- UI 交互：下拉菜单、模式、选项卡、切换、表情符号选择器。
- 字符计数器：根据数据属性中的平台限制计算客户端。

**已知限制：**
- Composer 预览需要服务器往返。通过保持预览端点无状态（无数据库查询）来缓解。
- 日历拖放使用乐观的 UI（Alpine 立即移动卡片，HTMX 发布更新，失败时恢复）。
- 实时收件箱需要 Redis + django-channels。以 30 秒轮询启动。

---

## 4. 社交提供商架构

每个平台都有一个实现抽象基类的专用模块。没有第三方统一API提供商。

```
SocialProvider (abstract):

  get_auth_url(redirect_uri, state) → str
  exchange_code(code, redirect_uri) → OAuthTokens
  refresh_token(refresh_token) → OAuthTokens
  get_profile(access_token) → AccountProfile
  publish_post(access_token, content) → PublishResult
  publish_comment(access_token, post_id, text) → CommentResult
  get_post_metrics(access_token, post_id) → PostMetrics
  get_account_metrics(access_token, date_range) → AccountMetrics
  get_audience_demographics(access_token) → Demographics
  get_messages(access_token, since) → list[InboxMessage]
  reply_to_message(access_token, message_id, text) → ReplyResult
  revoke_token(access_token) → bool

  platform_name → str
  max_caption_length → int
  supported_post_types → list[PostType]
  supported_media_types → list[MediaType]
  rate_limits → RateLimitConfig
```

**添加新平台：** 在 `providers/` 中创建一个文件，在提供商注册表中注册，添加到 `Platform` 枚举。发布者、收件箱、分析或任何其他系统没有变化。

---

## 5. 数据库

PostgreSQL 作为数据存储+作业队列。 django-background-tasks 将作业存储在由工作程序轮询的 PostgreSQL 表中。消除 Redis 的硬依赖。

**后台工作：**

| 作业 | 频率 |
|-----|-----------|
| 发布计划帖子 | 每 15 秒 |
| 同步收件箱消息 | 每个帐户每 5 分钟 |
| 收集后期分析 | 每小时（<48 小时）、每天（更早） |
| 收集账户指标 | 每日 |
| 收集观众人口统计数据 | 每周 |
| 刷新 OAuth 令牌 | 每小时（令牌在 24 小时内过期） |
| 生成重复帖子 | 每日（90 天前瞻） |
| 生成计划报告 | 每个计划配置 |
| 处理即将发布的帖子的媒体 | 发布后 60 分钟内的帖子 |
| 发送通知 | 事件触发 |
| 健康检查账户 | 每6小时 |
| 清理过期数据 | 每日 |

所有间隔均可通过 F-1.6 进行配置。

**数据隔离：** 自定义 Django 模型管理器按 `organization_id`/`workspace_id` 自动过滤所有查询。应用于ORM层。云版本添加了 PostgreSQL 行级安全性作为纵深防御。

**加密：** OAuth 令牌、API 密钥、通过自定义模型字段使用 AES-256-GCM 加密的凭据。密钥通过 HKDF 从 `SECRET_KEY` env var 派生。通过管理命令支持轮换。

---

## 6. 部署

### 6.1 Docker Compose（所有部署）

**开发 - 3 个容器：**

```
app:      Django runserver + volume mount
worker:   python manage.py process_tasks
postgres: postgres:16-alpine

Tailwind: `python manage.py tailwind start` on host (watches + recompiles)
```

**生产 - 4 个容器：**

```
app:      Gunicorn (4 workers, 2 threads)
worker:   python manage.py process_tasks
postgres: postgres:16-alpine
caddy:    Reverse proxy + auto-TLS

Tailwind: built during Docker image build
```

### 6.2 云（Hetzner VPS）

生产 Docker 在单个 VPS 上撰写。

| 资源 | 规格 | 成本 |
|----------|------|------|
| VPS | Hetzner CX32（4 个 vCPU，8GB RAM） | 7.59 欧元/月 |
| 媒体 | Cloudflare R2（10GB 免费）| ~€0 |
| 电子邮件 | 重新发送（3,000 个/月免费，50k 每月 20 美元）| ~€0 |
| 监控 | Sentry + UptimeRobot 免费套餐 | €0 |
| **总计** | | **~10 欧元/月** |

自动部署：GitHub Actions → SSH → 拉取 + 重新启动。备份：每天 `pg_dump` 到 R2。

**缩放路径：**

| 操作 | 增加成本 |
|--------|-----------|
| 托管 PostgreSQL | +18 欧元/月 |
| 第二个 VPS 工人 | +7.59 欧元/月 |
| 负载均衡器 + 第二个 Web VPS | +13 欧元/月 |

### 6.3 自托管：铁路

配置：仓库中的 `railway.toml`。三种服务：Web、Worker、托管 PostgreSQL。

临时文件系统 - `STORAGE_BACKEND` 必须是 `s3`。应用程序通过 `RAILWAY_ENVIRONMENT` 检测铁路并警告配置错误。

**费用：** ~15-30 美元/月。

### 6.4 自托管：渲染

配置：存储库中的 `render.yaml` 蓝图。三种服务：web (7 美元)、worker (7 美元)、PostgreSQL (7 美元)。

免费层睡眠（休息工人） - 必须使用付费。临时磁盘 - 需要 S3。

**费用：** 最低 21 美元/月。

### 6.5 自托管：Heroku

配置：`Procfile` + `app.json`（启用“部署到 Heroku”按钮）。

**过程文件：**
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2
worker: python manage.py process_tasks
```

**app.json** 预配置：基本 dynos、PostgreSQL Essential-0、自动生成 SECRET_KEY、部署后迁移、环境变量提示。 README 包括链接到 `https://heroku.com/deploy?template=https://github.com/yourorg/social-platform` 的部署按钮 - 在大约 5 分钟内运行应用程序。

| 组件 | 计划 | 成本 |
|-----------|------|------|
| Web 测功机 | 基本版 | 7 美元/月 |
| 工人测功机 | 基本 | 7 美元/月 |
| PostgreSQL | Essential-0（1GB，20 个连接） | 5 美元/月 |
| **总计** | | **19 美元/月** |

**严重警告：**
- **Eco dynos 破坏了应用程序。** 他们在 30 分钟后睡觉 - 工作人员停止，没有任何发布。必须使用基本+。
- **临时文件系统。** `STORAGE_BACKEND` 必须是 `s3`。应用程序通过 `DYNO` env var 检测 Heroku 并发出警告。
- **20 个连接限制。** 如果扩展超过 2 个网络测功机，则升级到 Essential-1（15 美元/月，40 个连接）。
- **白标签自定义域** 每个域需要手动 `heroku domains:add`。无点播TLS。
- **静态文件**通过 `whitenoise` 提供（无需单独托管）。

### 6.6 自托管：裸 VPS（Docker Compose）

主要记录路径。任何带有 Docker 的 Linux VPS。

```
1. Provision VPS (min 2 vCPU, 4GB RAM)
2. Install Docker: curl -fsSL https://get.docker.com | sh
3. Clone repo, cp .env.example .env, fill in secrets
4. docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
5. docker compose exec app python manage.py migrate
6. Open browser, complete first-run setup wizard
```

升级：`git pull && docker compose up -d --build && docker compose exec app python manage.py migrate`

媒体：默认本地文件系统（Docker 卷）。通过环境变量切换到 S3。

---

## 7. 媒体存储

单个环境变量切换后端：

```
STORAGE_BACKEND=local  →  FileSystemStorage (Docker volume)
STORAGE_BACKEND=s3     →  S3Boto3Storage via django-storages
```

**处理管道：**
- *上传时：*保存、提取元数据、生成缩略图（Pillow/FFmpeg）。
- *发布前：*后台作业在 60 分钟内处理帖子的媒体。调整图像大小、转换格式、转码视频 (H.264/AAC/MP4)。处理后的版本与原件一起存储。
- *FFmpeg 限制：* 最多 2 个并发转码（可配置），每个视频 5 分钟超时。

---

## 8. 安全性

| 关注 | 接近 |
|---------|----------|
| 密码 | bcrypt，成本因子 12 |
| 会话 | DB 支持，仅限 HTTP/Secure/SameSite=Lax，30 天滑动 8800000000000003888
| OAuth 登录 | django-allauth (Google, GitHub) |
| 2FA | TOTP 通过 django-otp，加密秘密，bcrypt 哈希恢复代码 |
| Magic links | 32字节令牌，存储为SHA-256哈希|
| API 个键 | 40 字节令牌，存储为 SHA-256 哈希，每个组织范围 |
| 静态加密 | AES-256-GCM 用于令牌/密钥/凭证，来自环境变量的密钥|
| 数据隔离 | 自定义 ORM 管理器按 org_id/workspace_id 自动过滤 |
| CSRF | Django 中间件，HTMX 自动包含令牌 |
| CSP | 通过 django-csp 的限制性策略 |
| 速率限制 | 登录时的 django-ratelimit，API，OAuth 端点 |
| 审核日志 | 仅附加、破坏性操作，保留 1 年 |
| GDPR | 每个工作区/组织导出 + 删除 |

---

## 9. 备份与恢复

### 云版本

每天通过 VPS 上的 cron 将 `pg_dump` 自动化到 Cloudflare R2。保留 30 个每日备份。媒体已经处于 R2 状态（本质上是耐用的）。

### 自托管

该存储库包括备份管理命令和记录的恢复过程。

**要备份什么：**
- PostgreSQL 数据库（所有应用程序数据）。
- 媒体存储：如果使用本地文件系统，则为 Docker 卷 (`media_data`)；如果使用 S3（已经持久），则不需要任何其他内容。

**备份命令：**

```
# Included management command - dumps database + lists media volume location
python manage.py backup --output /path/to/backup/

# Produces:
#   /path/to/backup/db_2026-03-25.sql.gz    (gzipped pg_dump)
#   /path/to/backup/manifest.json            (backup metadata: timestamp, app version, storage backend, media path)
```

通过码头工人：
```
docker compose exec app python manage.py backup --output /backups/
```

备份命令：
1. 针对配置的 `DATABASE_URL` 运行 `pg_dump`，使用 gzip 压缩。
2. 如果是 `STORAGE_BACKEND=local`，则在清单中记录媒体卷路径，以便用户知道还要备份该 Docker 卷。
3. 如果是 `STORAGE_BACKEND=s3`，则记录存储桶名称 - 无需介质备份。
4. 写入 `manifest.json`，其中包含：时间戳、应用程序版本、数据库大小、存储后端、媒体路径或存储桶名称。

**恢复命令：**

```
python manage.py restore /path/to/backup/db_2026-03-25.sql.gz
```

恢复命令：
1. 与用户确认这将覆盖所有当前数据。
2. 删除并重新创建数据库。
3. 加载 gzip 压缩的 SQL 转储。
4. 运行任何挂起的迁移（如果备份来自旧版本）。
5. 如果是 `STORAGE_BACKEND=local`，则打印一条提醒，以从用户自己的卷备份中恢复媒体 Docker 卷。

**自动备份（已记录，未内置）：**

README 记录了自动备份的 cron 作业模式：
```
# Daily backup at 2:00 AM, retain 30 days
0 2 * * * docker compose exec -T app python manage.py backup --output /backups/ && find /backups/ -name "db_*.sql.gz" -mtime +30 -delete
```

对于异地备份，README 记录了通过管道将备份传输到 S3 兼容存储：
```
docker compose exec -T app python manage.py backup --stdout | aws s3 cp - s3://my-backups/db_$(date +%F).sql.gz
```

---

## 10.入站 Webhook（平台 → 应用程序）

发布引擎将内容发送到平台（出站）。对于实时收件箱更新，某些平台通过 Webhook（入站）将数据推送回应用程序。这与 F-5.3 中的出站 Webhook 系统是分开的。

### 支持的平台

| 平台 | Webhook 支持 | 提供什么 |
|----------|----------------|-----------------|
| Facebook | 是（图 API Webhooks） | 页面评论、提及、消息、帖子反应 |
| Instagram | 是（通过 Facebook Graph API Webhooks） | 对媒体、提及、故事回复、消息的评论|
| LinkedIn | 否 | - （仅轮询）|
| TikTok | 否 | - （仅轮询）|
| YouTube | 是（YouTube 数据 API 通过 PubSubHubbub 推送通知） | 视频的新评论 |
| Pinterest | 否 | - （仅轮询）|
| 线程 | 否 | - （仅轮询） |
| Bluesky | 否（AT 协议 firehose 存在，但不是每个帐户） | -（仅轮询）|
| Google 商家资料 | 否 | -（仅轮询）|
| Mastodon | 是（通过 WebSocket 流式传输 API，而不是 HTTP webhooks） 8800000000000004888 通知、提及、新关注者 |

实际上，Facebook 和 Instagram 是唯一使用基于 HTTP 的入站 Webhook 有意义地取代轮询收件箱同步的平台。

### Webhook 端点架构

该应用程序公开特定于平台的 Webhook 接收器端点：

```
POST /webhooks/facebook/     ← Facebook & Instagram webhook events
POST /webhooks/youtube/      ← YouTube PubSubHubbub notifications
```

每个端点：
1. **在处理之前验证请求签名**。未签名或签名错误的请求将被拒绝并返回 403。
2. 解析特定于平台的有效负载。
3. 将有效负载映射到内部 `InboxMessage` 模型。
4. 排队后台作业来处理消息（重复数据删除、情绪标记、通知调度）。
5. 立即返回 200（平台需要快速响应 - 通常在 5 秒内，否则会重试/禁用 Webhook）。

### 签名验证

| 平台 | 验证方法 |
|----------|-------------------|
| Facebook / Instagram | HMAC-SHA256。 Facebook 使用 App Secret 对有效负载进行签名。接收器计算 `HMAC-SHA256(app_secret, raw_request_body)` 并将其与 `X-Hub-Signature-256` 标头进行比较。如果不匹配则拒绝。 |
| YouTube | PubSubHubbub 验证：订阅时，YouTube 会发送带有 `hub.challenge` 参数的 `GET` 质询。端点必须回显挑战。收到通知后，有效负载为 Atom XML - 如果在订阅期间配置，请验证 `hub.secret` HMAC。 |

用于 Facebook/Instagram 签名验证的 App Secret 与 F-1.5 中存储的凭证相同（平台 API 凭证）。验证函数从`PlatformCredential`模型中读取它。

### Webhook 注册

**脸书/Instagram：**
- Webhook 由平台开发人员（云）或自托管者在 Facebook 应用仪表板（开发人员控制台）中配置。
- 所需配置：回调URL、验证Token、订阅字段。
- **云版本：** 回调 URL 是 `https://app.yourdomain.com/webhooks/facebook/`。由开发人员在 Facebook App Dashboard 中配置一次。
- **自托管：** 回调 URL 是 88000000000001888。自托管者在自己的 Facebook 应用程序仪表板中对此进行配置。设置向导（首次运行）提供了精确的 URL 复制和分步说明。
- 验证令牌：存储为环境变量的随机字符串 (`FACEBOOK_WEBHOOK_VERIFY_TOKEN`)。在 Facebook 的初始 GET 验证握手期间使用。
- 订阅字段：`feed`、`mention`、`messages`（对于页面）、`comments`、`mentions`（对于Instagram）。

**YouTube：**
- 连接 YouTube 帐户 (F-2.5) 时，以编程方式创建 PubSubHubbub 订阅。
- 应用程序向 YouTube 的 PubSubHubbub 中心发送订阅请求，以获取已连接频道的活动源。
- 订阅到期（通常为 10 天），必须通过后台作业续订。
- 回调 URL 遵循相同的模式：`https://<domain>/webhooks/youtube/`。

### 自托管注意事项

- **需要 HTTPS。** Facebook 和 YouTube 拒绝对 HTTP 端点的 Webhook 回调。自托管者必须配置 TLS（Caddy 会自动处理此问题）。
- **需要公共 URL。** webhook 端点必须可从 Internet 访问。 NAT 后面的自托管程序或防火墙必须配置端口转发或使用隧道。
- **每个部署有不同的回调 URL。** 每个自托管实例都有自己的域，因此每个实例都必须向 Facebook/YouTube 注册自己的 Webhook 回调 URL。设置向导会生成正确的 URL 并提供复制粘贴就绪说明。
- **回退到轮询。** 如果自托管主机无法配置入站 Webhooks（例如，其服务器不可公开访问），平台将回退到基于轮询的收件箱同步（每 5 分钟一次）。 Webhook 配置是可选的 - 作为基线，轮询始终处于活动状态。

### 数据流

```
Platform (Facebook/Instagram) → POST /webhooks/facebook/
  → Verify signature (HMAC-SHA256 with App Secret)
  → Parse payload (identify event type, page/account, message content)
  → Match to workspace (lookup SocialAccount by platform account ID)
  → Deduplicate (check platform_message_id against existing InboxMessages)
  → Create InboxMessage record
  → Enqueue notification job (in-app badge, email, Slack per F-7.1)
  → Return 200
```

---

## 11.环境变量

```
# CORE
SECRET_KEY=
DEBUG=false
ALLOWED_HOSTS=app.yourdomain.com
APP_URL=https://app.yourdomain.com

# DATABASE
DATABASE_URL=postgres://user:pass@postgres:5432/socialapp

# STORAGE
STORAGE_BACKEND=local
MEDIA_ROOT=/app/media
S3_ENDPOINT_URL=
S3_ACCESS_KEY_ID=
S3_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
S3_CUSTOM_DOMAIN=
S3_REGION_NAME=auto

# EMAIL
# Self-hosted uses SMTP (any provider: Resend SMTP, Mailgun, SES, own server):
EMAIL_BACKEND=smtp                   # "resend" (API) or "smtp" (generic SMTP)
EMAIL_HOST=                          # SMTP only
EMAIL_PORT=587                       # SMTP only
EMAIL_HOST_USER=                     # SMTP only
EMAIL_HOST_PASSWORD=                 # SMTP only
EMAIL_USE_TLS=true                   # SMTP only
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# PLATFORM CREDENTIALS (cloud - self-hosted uses admin UI)
PLATFORM_FACEBOOK_APP_ID=
PLATFORM_FACEBOOK_APP_SECRET=
PLATFORM_LINKEDIN_CLIENT_ID=
PLATFORM_LINKEDIN_CLIENT_SECRET=
PLATFORM_TIKTOK_CLIENT_KEY=
PLATFORM_TIKTOK_CLIENT_SECRET=
PLATFORM_GOOGLE_CLIENT_ID=
PLATFORM_GOOGLE_CLIENT_SECRET=
PLATFORM_PINTEREST_APP_ID=
PLATFORM_PINTEREST_APP_SECRET=

# REDIS (optional)
REDIS_URL=

# INBOUND WEBHOOKS
FACEBOOK_WEBHOOK_VERIFY_TOKEN=       # Random string for Facebook webhook verification handshake
YOUTUBE_WEBHOOK_SECRET=              # Optional HMAC secret for YouTube PubSubHubbub

# SENTRY (optional)
SENTRY_DSN=
```

---

## 12. 开发

```bash
git clone https://github.com/yourorg/social-platform.git && cd social-platform
cp .env.example .env  # set DEBUG=true, DATABASE_URL

docker compose up postgres -d

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python manage.py tailwind install   # one-time
python manage.py tailwind start     # watches + recompiles CSS

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver           # terminal 1
python manage.py process_tasks       # terminal 2
```

或者：`docker compose up`（Tailwind 在 Dockerfile 内部构建）。

**CI (GitHub Actions)：** lint (ruff) → 类型检查 (mypy) → 测试 (pytest) → E2E (Playwright) → 构建镜像 → 合并到 main 时部署。

---

## 13. 成本汇总

**云（赫兹纳）：**

| 规模 | 每月 |
|-------|---------|
| 启动（1–100 个组织） | ~€10 |
| 增长（100–500 个组织） | ~€28 |
| 规模（500–2,000 个组织） | ~€45 |

**自托管：**

| 路径 | 每月 |
|------|---------|
| 裸 VPS (Hetzner/DO/Linode) | €5–7 |
| Heroku（基本 + Essential-0） | $19 |
| 铁路 | $15–30 |
| 渲染 | $21+ |
| 家庭服务器 | $0 |
