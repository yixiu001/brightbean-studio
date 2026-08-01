<p对齐=“中心”>
  <a href="https://github.com/brightbeanxyz/brightbean-studio">
    <img src=".github/assets/brightbean-studio-logo.webp" alt="BrightBean Studio" width="280">
  </a>
</p>

<p对齐=“中心”>
  <strong>面向创作者、代理机构和中小企业的开源社交媒体管理。</strong>
</p>

<p对齐=“中心”>
  <a href="https://github.com/brightbeanxyz/brightbean-studio/actions/workflows/ci.yml"><img src="https://github.com/brightbeanxyz/brightbean-studio/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-blue.svg" alt="许可证：AGPL-3.0"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="Python 3.12+"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.x-green.svg" alt="Django 5.x"></a>
</p>

<p对齐=“中心”>
  <a href="https://brightbean.xyz/studio/"><img src="https://img.shields.io/badge/Free%20hosted%20version-brightbean.xyz%2Fstudio-FFB300?style=for-the-badge" alt="免费托管版本，位于 Brightbean.xyz/studio"></a>
</p>

---

## 关于 BrightBean 工作室

BrightBean Studio 是一个开源、可自托管的社交媒体管理平台，专为创作者、代理机构和中小型企业而构建。它的功能与 Sendible、SocialPilot 或 ContentStudio 的功能相同，但免费且没有每个席位、每个频道或每个工作空间的限制。从单个多工作区仪表板规划、撰写、安排、批准、发布和监控 Facebook、Instagram、LinkedIn、TikTok、YouTube、Pinterest、Threads、Bluesky、Google Business Profile、Mastodon 和 DEV.to 上的内容。

它适合在同一屋檐下管理多个客户帐户的人们，他们宁愿拥有自己的社交堆栈，也不愿每月向 SaaS 供应商支付 100-300 美元。每个功能都可供每个用户使用。没有付费等级，没有功能门，没有追加销售。

免费托管版本可在 [brightbean.xyz/studio](https://brightbean.xyz/studio/) 上获得。您还可以在 Heroku、Render 或 Railway 上自行一键部署，通过 Docker 在您自己的 VPS 上运行，或者在本地运行。所有平台集成都使用您自己的开发人员凭证直接与官方第一方 API 对话，因此没有聚合中间人，没有供应商锁定，也没有第三方介于您和您的数据之间。

## 特点

| | |
|---|---|
| **多工作空间和团队** | 无限组织 → 工作空间 → 成员。粒度 RBAC，具有自定义角色、邀请和外部协作者的单独客户角色。 |
| **内容编辑器** | 丰富的编辑器，具有每个平台的标题/媒体覆盖、版本历史记录、可重复使用的模板、内容类别和标签、看板创意板。 |
| **日历和日程安排** | 可视化日历，每个帐户每周定期发帖时段，以及自动将帖子分配到下一个可用时段的命名队列。 |
| **发布引擎** | 直接第一方 API 集成（无聚合器）、自动重试、每个帐户速率限制跟踪和 90 天发布审核日志。 |
| **审批工作流程** | 可配置阶段（无/可选/内部/内部+客户端）、内部和外部评论、提醒和完整审核跟踪。 |
| **统一社交收件箱** | 来自每个连接平台的评论、提及、私信和评论都集中在一个地方，包括情绪分析、作业、线索回复和历史回填。 |
| **分析** | 每个连接平台的本机 API 的每帖子和频道级性能，带有 KPI 个卡片、7/30/90 天趋势图和可排序所有帖子表，显示观看次数、参与度、关注者增长、覆盖范围和观看时间。 |
| **媒体库** | 组织范围和工作区范围的库，具有嵌套文件夹、自动生成的平台优化变体、替代文本以及编辑器中内置的 Unsplash 库存照片搜索。 |
| **客户端门户** | 无密码 30 天魔术链接访问，因此客户无需创建帐户即可批准或拒绝帖子。 |
| **通知** | 应用内、电子邮件和 Webhook 传送，以及每种事件类型的每个用户首选项。 |
| **安全和操作** | 加密令牌和凭证存储、Google SSO、Sentry 支持和 14 天可逆组织删除宽限期。 2FA (TOTP) 已在路线图上。 |
| **白标签友好** | 每个工作区的品牌（徽标、颜色）以及话题标签、第一条评论和发布模板的工作区默认值。 |

### 快速浏览

<表>
  <tr>
<td colspan="2"><img src=".github/assets/BrightBean%20Studio%20Calendar.webp" alt="日历视图"><br><sub><b>可视日历</b> - 具有重复槽和队列的拖放计划。</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src=".github/assets/BrightBean%20Studio%20Post%20Editor.webp" alt="帖子编辑器"><br><sub><b>帖子编辑器</b> - 具有每个平台覆盖和预览功能的编辑器。</sub></td>
    <td width="50%"><img src=".github/assets/BrightBean%20Studio%20Idea%20Kanban%20Board.webp" alt="Idea kanban board"><br><sub><b>创意板</b> - 用于跟踪所有帖子创意的看板工作流程。</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src=".github/assets/BrightBean%20Social%20Media%20Platforms.webp" alt="连接平台"><br><sub><b>连接任何内容</b> - 10 多个第一方集成，无聚合器。</sub></td>
    <td width="50%"><img src=".github/assets/BrightBean%20Studio%20Analytics.webp" alt="Analytics dashboard"><br><sub><b>效果分析</b> - 每个帖子和频道级别的指标，包含 KPI 张卡片和趋势图。</sub></td>
  </tr>
</表>

## 支持的平台

| 平台 | 发布 | 评论 | DM | 见解|
|---|:---:|:---:|:---:|:---:|
| <img src="https://cdn.simpleicons.org/facebook" width="16" height="16"> Facebook | ✓ | ✓ | ✓ | ✓ |
| <img src="https://cdn.simpleicons.org/instagram" width="16" height="16"> Instagram | ✓ | ✓ | ✓ | ✓ |
| <img src="https://cdn.simpleicons.org/instagram" width="16" height="16"> Instagram（直接）| ✓ | ✓ | ✓ | ✓ |
| <img src="https://api.iconify.design/logos/linkedin-icon.svg" width="16" height="16"> LinkedIn（个人） | ✓ | ✓ | — | ✓ |
| <img src="https://api.iconify.design/logos/linkedin-icon.svg" width="16" height="16"> LinkedIn（公司） | ✓ | ✓ | — | ✓ |
| <img src="https://cdn.simpleicons.org/tiktok" width="16" height="16"> TikTok | ✓ | — | — | ✓ |
| <img src="https://cdn.simpleicons.org/youtube" width="16" height="16"> YouTube | ✓ | ✓ | — | ✓ |
| <img src="https://cdn.simpleicons.org/pinterest" width="16" height="16"> Pinterest | ✓ | — | — | ✓ |
| <img src="https://cdn.simpleicons.org/threads" width="16" height="16"> 线程 | ✓ | ✓ | — | ✓ |
| <img src="https://cdn.simpleicons.org/bluesky" width="16" height="16"> 蓝天 | ✓ | ✓ | — | — |
| <img src="https://api.iconify.design/logos/google-icon.svg" width="16" height="16"> Google 商家资料 | ✓ | — | — | ✓ |
| <img src="https://cdn.simpleicons.org/mastodon" width="16" height="16"> 乳齿象 | ✓ | ✓ | — | — |
| <img src="https://cdn.simpleicons.org/devdotto/000000" width="16" height="16"> DEV.to | ✓ | — | — | — |

---

### 托管版本

Brightbean Studio 的免费托管版本可在 [brightbean.xyz/studio](https://brightbean.xyz/studio/) 上获取。它运行与此存储库相同的代码库，无需设置或维护。

如果您希望自行托管，请选择以下选项之一。

### 一键部署

| Heroku | 渲染 | 铁路 |
|:------:|:------:|:-------:|
| [![部署到 Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/brightbeanxyz/brightbean-studio) | [![部署到渲染](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/brightbeanxyz/brightbean-studio) | [![在铁路上部署](https://railway.com/button.svg)](https://railway.com/deploy/brightbean-studio?referralCode=brightbean) |

部署后，在平台的仪表板中设置这些环境变量：

| 变量 | 必需 | 描述 |
|----------|----------|-------------|
| `DJANGO_SETTINGS_MODULE` | 自动设置 | `config.settings.production`。如果部署配置未放置它，则设置它。 |
| `SECRET_KEY` | 自动生成的 | Django 密钥。通过部署按钮自动设置。 |
| `ENCRYPTION_KEY_SALT` | 自动生成的 | 加密盐。通过部署按钮自动设置。 |
| `DATABASE_URL` | 自动配置 | PostgreSQL 连接字符串。自动设置。 |
| `ALLOWED_HOSTS` | 是 | 您的应用程序的域，例如`your-app.herokuapp.com` |
| `APP_URL` | 是 | 完全公开 URL，例如`https://your-app.herokuapp.com` |
| `STORAGE_BACKEND` | 否 | 对于 S3/R2 存储，设置为 `s3`。默认值：`local`。Heroku、Render 和 Railway 具有临时文件系统，因此在没有 S3 的情况下重新部署时上传的文件会丢失。 |
| `S3_ENDPOINT_URL` | 如果使用 S3 | S3 兼容端点 URL |
| `S3_ACCESS_KEY_ID` | 如果使用 S3 | S3 访问密钥 |
| `S3_SECRET_ACCESS_KEY` | 如果使用 S3 | S3 密钥 |
| `S3_BUCKET_NAME` | 如果使用 S3 | S3 存储桶名称 |
| `EMAIL_HOST` | 否 | SMTP 用于发送邀请和密码重置的服务器|
| `EMAIL_PORT` | 否 | SMTP 端口（默认： `587`) |
| `EMAIL_HOST_USER` | 否 | SMTP 用户名 |
| `EMAIL_HOST_PASSWORD` | 无 | SMTP 密码 |
| `GOOGLE_AUTH_CLIENT_ID` | 否 | 用于 Google OAuth 登录。从 [Google Cloud Console](https://console.cloud.google.com/) → 凭证获取。 |
| `GOOGLE_AUTH_CLIENT_SECRET` | 否 | Google OAuth 机密 |
| `UNSPLASH_ACCESS_KEY` | 否 | 在编辑器中启用 Unsplash 库存照片搜索。在 [unsplash.com/developers](https://unsplash.com/developers) 创建免费应用程序。 |

对于社交媒体 API 密钥，请参阅[平台凭证](#platform-credentials)。完整变量参考：`.env.example`。

## 快速入门（Docker）

```bash
git clone https://github.com/brightbeanxyz/brightbean-studio.git
cd brightbean-studio
cp .env.example .env
```

编辑 `.env` - 将 `DATABASE_URL` 更改为指向 Docker 服务名称：

```
DATABASE_URL=postgres://postgres:postgres@postgres:5432/brightbean
```

然后开始一切：

```bash
docker compose up -d --build
docker compose exec app python manage.py createsuperuser
```

数据库迁移之前通过 `migrate` Compose 服务自动运行
`app` 和 `worker` 服务启动，因此没有单独的迁移步骤。

Tailwind 通过 `tailwind` Compose 服务自动编译。第一次构建
大约需要 60–90 秒（在新容器中运行 `npm install`）；随后的
启动是即时的。使用 `docker compose logs -f tailwind` 观看进度。

打开 http://localhost:8000 - 你正在运行。


## 完全本地开发（无需 Docker）

本地运行所有内容 - 无需 Docker，无需安装 PostgreSQL。使用 SQLite 作为数据库。

### 先决条件

-Python 3.12+
- Node.js 20+

### 设置

**1.克隆和配置**

```bash
git clone https://github.com/brightbeanxyz/brightbean-studio.git
cd brightbean-studio
cp .env.example .env
```

**2.切换到 SQLite**

打开 `.env` 并替换 `DATABASE_URL` 行：

```
DATABASE_URL=sqlite:///db.sqlite3
```

就是这样 - 无需安装或管理数据库服务器。

**3.设置Python**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**4.设置 Tailwind CSS**

```bash
cd theme/static_src
npm install
cd ../..
```

**5.运行数据库迁移**

```bash
python manage.py migrate
```

**6。创建您的管理员帐户**

```bash
python manage.py createsuperuser
```

**7.启动应用程序（3 个终端选项卡）**

选项卡 1 - 顺风观察者：
```bash
cd theme/static_src && npm run start
```

选项卡 2 - Django 开发服务器：
```bash
source .venv/bin/activate
python manage.py runserver
```

选项卡 3 - 后台工作人员：
```bash
source .venv/bin/activate
python manage.py process_tasks
```

打开 http://localhost:8000 并使用您创建的超级用户登录。

### 日常工作流程（无 Docker）

```bash
source .venv/bin/activate                # activate Python env
python manage.py runserver               # start web server
# (open another tab)
python manage.py process_tasks           # start worker
```

> **注意：** SQLite 适合本地开发和小型部署。对于生产或大量并发使用，请切换到 PostgreSQL。

## 运行测试

```bash
pytest
```

覆盖范围：

```bash
pytest --cov=apps --cov-report=term-missing
```

## Linting 和类型检查

```bash
ruff check .                             # lint
ruff format --check .                    # format check
mypy apps/ config/ --ignore-missing-imports  # type check
```

自动修复 lint 问题：

```bash
ruff check --fix .
ruff format .
```

## 生产部署

### Docker Compose 在 VPS 上（推荐）

```bash
# On your server:
git clone https://github.com/brightbeanxyz/brightbean-studio.git
cd brightbean-studio
cp .env.example .env
# Edit .env:
#   SECRET_KEY=<generate a random 50+ char string>
#   DEBUG=false
#   ALLOWED_HOSTS=yourdomain.com
#   APP_URL=https://yourdomain.com
#   DATABASE_URL=postgres://postgres:<strong-password>@postgres:5432/brightbean

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose exec app python manage.py createsuperuser
```

这将启动 5 个容器：app (Gunicorn)、worker、PostgreSQL、Caddy (auto-HTTPS) 和一个在启动时自动运行数据库迁移的一次性迁移容器。使用您的域名编辑 `Caddyfile`。

更新：

```bash
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### 其他平台

| 平台 | 配置文件 | 注释 |
|----------|-------------|-------|
| **Heroku** | `Procfile` + `app.json` | 部署按钮就绪。必须使用 Basic+ dynos（Eco dynos 会破坏工人）。 |
| **铁路** | `railway.toml` | [一键模板](https://railway.com/deploy/brightbean-studio) 提供三种服务：Web（Gunicorn、运行）启动时为 `migrate`)、工作线程 (`python manage.py process_tasks`) 和托管 PostgreSQL。 Web 服务的启动 `migrate` 会触发注册重复任务的 `post_migrate` 挂钩，因此调度可以开箱即用。 |
| **渲染** | `render.yaml` | 带有 Web、worker、PostgreSQL 的蓝图。必须使用付费等级。 |

所有具有临时文件系统的平台都需要 `STORAGE_BACKEND=s3` - 有关 S3 配置，请参阅 `.env.example`。

有关每个平台的详细说明和成本细目，请参阅 `architecture.md`。

## 项目结构

```
brightbean-studio/
├── config/
│   ├── settings/
│   │   ├── base.py            # Shared settings
│   │   ├── development.py     # Local dev overrides
│   │   ├── production.py      # Production hardening
│   │   └── test.py            # Test overrides
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/              # Custom User model, auth, OAuth, sessions
│   ├── organizations/         # Organization management
│   ├── workspaces/            # Workspace CRUD
│   ├── members/               # RBAC, invitations, middleware, decorators
│   ├── settings_manager/      # Configurable defaults with cascade logic
│   ├── credentials/           # Platform API credential storage (encrypted)
│   └── common/                # Shared: encrypted fields, scoped model managers
├── providers/                 # Social platform API modules (one file per platform)
├── templates/                 # Django templates
│   ├── base.html              # Layout with sidebar + nav
│   └── components/            # Reusable HTMX partials
├── static/
│   └── js/                    # Vendored HTMX + Alpine.js
├── theme/                     # django-tailwind theme app
│   └── static_src/
│       ├── src/styles.css     # Tailwind directives
│       └── tailwind.config.js
├── Dockerfile
├── docker-compose.yml         # Dev: app + worker + postgres
├── docker-compose.prod.yml    # Prod override: adds Caddy, uses Gunicorn
├── Caddyfile                  # Reverse proxy + auto-HTTPS config
├── .env.example               # All environment variables
├── Procfile                   # Heroku
├── app.json                   # Heroku deploy button
├── railway.toml               # Railway config
└── render.yaml                # Render blueprint
```

> **设置选择：** `DJANGO_SETTINGS_MODULE` 环境变量控制 Django 使用哪个设置文件。每个上下文的默认值已连接：8800000000000001888 使用 `development`、`wsgi.py`/`asgi.py` 使用 `production` 和`pytest` 使用 `test`（通过 `pyproject.toml`）。 Docker Compose 文件和平台部署配置（Heroku、Render）也明确设置了它。如果您想要特定命令的非默认模块，例如，您只需要手动覆盖它。 `DJANGO_SETTINGS_MODULE=config.settings.production python manage.py check --deploy`。

## 平台凭证

要连接社交媒体帐户，您需要来自每个平台的开发者门户的 API 凭据。您可以通过 `.env` 中的环境变量进行设置（请参阅 `.env.example`），或者针对每个组织，通过 Django 管理员在 `{APP_URL}/admin/` → **凭证 → 平台凭证**（仅限超级用户）。如果在两个位置都配置了平台，则 `.env` 值优先。

**管理员 UI 访问权限（仅限超级用户）：** `{APP_URL}/admin/` (for example `https://brightbean.example.com/admin/`) 的 Django 管理员仅限于超级用户帐户 — 只有超级用户可以在此处查看或编辑平台凭据。如果您还没有，请创建一个超级用户，然后登录并打开 **凭据 → 平台凭据**：

```bash
python manage.py createsuperuser
# Docker: docker compose exec app python manage.py createsuperuser
```

**重定向 URI：** 在任何平台上注册您的应用程序时，请将 OAuth 重定向 URI 设置为：

```
{APP_URL}/social-accounts/callback/{platform}/
```

例如，如果您的 `APP_URL` 是 `https://brightbean.example.com`，则 Facebook 重定向 URI 将为 `https://brightbean.example.com/social-accounts/callback/facebook/`。

> **TikTok：** 使用 slug `social1` 而不是 `tiktok` — TikTok 拒绝包含其品牌名称的重定向 URI。请参阅 [TikTok](#tiktok) 部分。

### 元（Facebook、Instagram、话题）

Facebook、Instagram 和 Threads 都使用相同的 Meta 应用程序凭据。

1. 进入 [Meta for Developers](https://developers.facebook.com/) 并创建一个新应用程序（类型：**Business**）
2. 在**应用程序设置 → 基本**下，复制您的**应用程序 ID** 和 **应用程序密钥**
3. 在应用程序仪表板中，转到 **用例** 并添加以下四个用例。对于每个用例，单击进入并转到 **权限和功能** 以添加所需的可选权限：

   **用例：“管理页面上的所有内容”** (Facebook)
   - 此用例自动包含 `business_management`、`pages_show_list` 和 `public_profile`
   - 添加以下可选权限：`pages_manage_posts`、`pages_manage_engagement`、`pages_read_engagement`、`pages_read_user_content`、`pages_manage_metadata`、 `read_insights`

   **用例：“Meta Messenger”**（Facebook 消息传递）
   - 需要启用 `pages_messaging` 权限，该权限在“管理页面”用例下不可用
   - 添加可选权限：`pages_messaging`

   **用例：“管理 Instagram 上的消息和内容”** (Instagram)
   - 添加以下权限：`instagram_basic`、`instagram_content_publish`、`instagram_manage_comments`、`instagram_manage_insights`

   **用例：“访问线程 API”**（线程）
- 此用例自动包含 `threads_basic`
   - 添加这些可选权限：`threads_content_publish`、`threads_manage_insights`、`threads_manage_replies`

4. 在 **Facebook 登录 → 设置 → 有效 OAuth 重定向 URI** 下，添加以下重定向 URI：
   ```
   {APP_URL}/social-accounts/callback/facebook/
   {APP_URL}/social-accounts/callback/instagram/
   {APP_URL}/social-accounts/callback/threads/
   ```
5.设置环境变量：
   ```
   PLATFORM_FACEBOOK_APP_ID=your-app-id
   PLATFORM_FACEBOOK_APP_SECRET=your-app-secret
   ```

### Instagram（直接，通过 Instagram 登录）

Instagram（直接）连接器使用 **Instagram API 和 Instagram 登录** - 与上面基于 Facebook 登录的 Instagram 连接器不同的 OAuth 流程。它适用于 **专业** Instagram 帐户（企业或创作者）**无需** 需要链接的 Facebook 页面。

> **帐户类型要求：** 自 Instagram 基本显示 API 于 2024 年 12 月 4 日停用以来，个人 Instagram 帐户没有 API 访问权限。用户必须先将其帐户转换为专业帐户（免费，在 IG 设置 → *帐户类型和工具* → *切换到专业帐户*）。

1. 在同一个 Meta 应用程序中，转到 **用例** 并添加 **“Instagram API”** 用例
2. 在 **API 设置 Instagram 登录**下，记下您的 **Instagram 应用程序 ID** 和 **Instagram 应用程序密钥**（这些与您的 Facebook 应用程序 ID/密钥不同）
3. 转到 **权限和功能** 并添加所需的权限：
   - `instagram_business_basic`、`instagram_business_content_publish`、`instagram_business_manage_comments`、`instagram_business_manage_messages`、`instagram_business_manage_insights`
4. 在**API 设置 Instagram 登录 → 步骤 4：设置 Instagram 企业登录**下，单击 **设置** 并添加重定向 URI（必须完全匹配，包括尾部斜杠）：
   ```
   {APP_URL}/social-accounts/callback/instagram_login/
   ```
5. 在 **API 设置 Instagram 登录 → 步骤 3：配置 webhooks** 下，设置：
   - **回拨URL：** `{APP_URL}/webhooks/instagram_login/`
   - **验证令牌：** `.env` 中的 `INSTAGRAM_LOGIN_WEBHOOK_VERIFY_TOKEN` 的值（任何随机字符串；生成一个并在单击验证并保存之前设置环境变量）。验证通过后，订阅`messages`、`comments`、`mentions`字段。
6.设置环境变量：
   ```
   PLATFORM_INSTAGRAM_APP_ID=your-instagram-app-id
   PLATFORM_INSTAGRAM_APP_SECRET=your-instagram-app-secret
   INSTAGRAM_LOGIN_WEBHOOK_VERIFY_TOKEN=your-random-verify-token
   ```

### 领英

Brightbean Studio 支持两个 LinkedIn 路径。选择您的 LinkedIn 开发应用程序可以在单独的应用程序上获取的任何一个或两者。

**路径 A - 仅限个人（任何个人开发人员都可以执行此操作）：**

1. 前往 [LinkedIn 开发者门户](https://developer.linkedin.com/) 并创建一个新应用程序（无需公司页面验证）。
2. 在 **产品** 下，请求访问（均自动批准）：
   - **使用 OpenID Connect 登录 LinkedIn**
   - **在 LinkedIn 上分享**
3. 在 **Auth** 下，添加重定向 URI：
   ```
   {APP_URL}/social-accounts/callback/linkedin_personal/
   ```
4.范围：`openid`、`profile`、`email`、`w_member_social`。
5.设置环境变量：
   ```
   PLATFORM_LINKEDIN_PERSONAL_CLIENT_ID=your-client-id
   PLATFORM_LINKEDIN_PERSONAL_CLIENT_SECRET=your-client-secret
   ```

> **路径 A 的限制：** 访问令牌持续约 60 天，并且 LinkedIn 不会为这些范围颁发刷新令牌 - 用户必须每约 60 天手动重新连接一次。收件箱/评论阅读不适用于此路径上的个人帐户。

**路径 B - 公司页面（还启用完整的个人功能）：**

1. 进入[LinkedIn开发者门户](https://developer.linkedin.com/)并创建一个新应用程序。
2. 验证应用程序与 LinkedIn 公司页面的关联。
3. 在**产品**下，请求访问：
   - **社区管理 API** *（受限 - 需要 LinkedIn 审核）*
4. 在 **Auth** 下，添加 **both** 重定向 URI：
   ```
   {APP_URL}/social-accounts/callback/linkedin_personal/
   {APP_URL}/social-accounts/callback/linkedin_company/
   ```
5.范围：
   - **个人：** `r_basicprofile`、`w_member_social`、`r_member_social`
   - **公司:** `r_basicprofile`、`w_member_social`、`w_organization_social`、`r_organization_social`、`rw_organization_admin`
6.设置环境变量：
   ```
   PLATFORM_LINKEDIN_COMPANY_CLIENT_ID=your-client-id
   PLATFORM_LINKEDIN_COMPANY_CLIENT_SECRET=your-client-secret
   ```

如果您仅设置路径 B（公司）凭据，Brightbean Studio 也会自动将它们重新用于个人连接 - 刷新令牌（365 天）和收件箱都可以使用。如果您有单独的仅限个人的应用程序，则仅需要路径 A 变量。

> **注意：**“使用 OpenID Connect 登录 LinkedIn”/“在 LinkedIn 上共享”和“社区管理 API”在单个 LinkedIn 应用程序上**互斥**。路径 A 和路径 B 需要单独的应用程序。

> **向后兼容性：** 旧版 `PLATFORM_LINKEDIN_CLIENT_ID` / `PLATFORM_LINKEDIN_CLIENT_SECRET` 环境变量仍然被视为 `linkedin_personal` 和 `linkedin_company` 的后备 - 现有的自托管程序无需更改即可继续工作。假定旧凭证已获得 CM 批准；如果您的旧版应用程序仅包含 OIDC，请将其迁移到 `PLATFORM_LINKEDIN_PERSONAL_*`。

### 抖音

1. 进入 [TikTok 开发者平台](https://developers.tiktok.com/)，创建一个新应用
2.添加产品**登录套件**和**内容发布API**
3. 配置重定向 URI — 使用 `social1`，而不是 `tiktok`（TikTok 拒绝包含其品牌名称的 URI）：
   ```
   {APP_URL}/social-accounts/callback/social1/
   ```
4. 所需范围：`user.info.basic`、`video.publish`、`video.upload`、`video.list`
5. 注意：TikTok 使用**客户端密钥**（而不是客户端 ID）。从应用程序仪表板复制 **客户端密钥** 和 **客户端密钥**
6.设置环境变量：
   ```
   PLATFORM_TIKTOK_CLIENT_KEY=your-client-key
   PLATFORM_TIKTOK_CLIENT_SECRET=your-client-secret
   ```
7. 为了进行生产审核，针对 TikTok **沙盒** 录制演示视频，显示正在使用的每个请求的范围。

### Google（YouTube、Google 商家资料）

YouTube 和 Google 商家资料共享相同的 Google Cloud 凭据。

1. 进入 [Google Cloud Console](https://console.cloud.google.com/)，新建一个项目（或选择已有的项目）
2. 在 **API 和服务 → 库** 下启用以下 API：
   - **YouTube 数据 API v3**（适用于 YouTube）
   - **我的商家帐户管理 API**、**我的商家商家信息 API** 和 **Google 我的商家 API**（适用于 Google 商家资料）
3. 转到 **API 和服务 → 凭据** 并创建 **OAuth 2.0 客户端 ID**（类型：Web 应用程序）
4. 在**授权重定向 URI** 下添加以下重定向 URI：
   ```
   {APP_URL}/social-accounts/callback/youtube/
   {APP_URL}/social-accounts/callback/google_business/
   ```
5. 复制 **客户端 ID** 和 **客户端密钥**
6. 所需范围：
   - **YouTube：** `https://www.googleapis.com/auth/youtube.upload`、`https://www.googleapis.com/auth/youtube.readonly`、`https://www.googleapis.com/auth/youtube.force-ssl`、`https://www.googleapis.com/auth/yt-analytics.readonly`
   - **谷歌商家资料：** `https://www.googleapis.com/auth/business.manage`
7.设置环境变量：
   ```
   PLATFORM_GOOGLE_CLIENT_ID=your-client-id
   PLATFORM_GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### 兴趣

1. 进入[Pinterest开发者门户](https://developers.pinterest.com/)并创建一个新应用程序
2. 在您的应用程序设置下，添加重定向 URI：
   ```
   {APP_URL}/social-accounts/callback/pinterest/
   ```
3.复制**应用程序ID**和**应用程序密钥**
4. 所需范围：`user_accounts:read`、`boards:read`、`pins:read`、`pins:write`
5.设置环境变量：
   ```
   PLATFORM_PINTEREST_APP_ID=your-app-id
   PLATFORM_PINTEREST_APP_SECRET=your-app-secret
   ```

### 蓝天

无需注册开发者应用程序。用户通过输入 Bluesky 句柄和 **应用程序密码** 进行连接：

1. 登录 [Bluesky](https://bsky.app/)
2. 转到 **设置 → 隐私和安全 → 应用程序密码**
3. 创建一个新的应用程序密码，并在 Brightbean Studio 中连接您的帐户时使用它

### 乳齿象

无需注册开发者应用程序。当用户连接其帐户时，Brightbean Studio 会自动在每个 Mastodon 实例上注册 OAuth 应用程序。用户只需输入其实例 URL（例如 `mastodon.social`）。

### DEV.to

无需注册开发者应用程序。用户通过输入个人 **API 密钥**进行连接：

1. 登录 [DEV.to](https://dev.to/)，打开 **[设置 → 扩展](https://dev.to/settings/extensions)**
2. 在 **DEV Community API Keys** 下，输入说明（例如 `Brightbean`），然后单击 **生成 API 密钥**
3.复制生成的密钥并在Brightbean Studio中连接帐户时粘贴它

帖子发布为 DEV.to 文章（标题 + Markdown 正文）。可以随时从同一设置页面撤销该密钥。

## 收件箱：回填历史消息

请参阅上面的[支持的平台](#supported-platforms) 矩阵，了解每个平台的收件箱功能。

要导入历史消息（例如，过去 7 天的消息）：

```bash
python manage.py backfill_inbox --days 7
```

选项：
- `--days N` - 回填天数（默认值：7）
- `--platform NAME` - 仅回填特定平台（例如，`youtube`、`linkedin`、`tiktok`）
- `--account-id UUID` - 仅回填特定帐户

## 代理号码 API 和 MCP

BrightBean Studio 附带了 REST API 和 MCP（模型上下文协议）服务器，以便代理和脚本可以读取分析、管理媒体以及创建或安排帖子。两者共享相同的身份验证、权限模型、速率限制和审核日志。选择适合您的客户的协议。

**基数 URL:** `{APP_URL}/api/v1/` (e.g. `https://your-studio.example.com/api/v1/`)

### 身份验证

从 **组织 → API 密钥** 发出 API 密钥。密钥具有工作区范围，可以列入特定社交帐户的许可名单，并继承颁发者工作区权限的子集。撤销立即生效。将密钥作为不记名令牌发送：

```
Authorization: Bearer bb_studio_...
```

权限密钥：`create_posts`、`publish_directly`、`upload_media`、`view_analytics`。每个端点都需要相关权限；缺少权限返回 `403`。

### 速率限制

| 范围 | 限制 |
|---|---|
| 每键写入 | 120/分钟 |
| 每键读取次数 | 300/分钟 |
| 每个工作空间聚合 | 1000 / 分钟 |

速率限制响应（`429`）包括 `Retry-After`、`X-RateLimit-Limit` 和 `X-RateLimit-Remaining` 标头。

### REST 端点

| 方法 | 路径 | 用途 | 权限 |
|---|---|---|---|
| `GET` | `/me` | 检查调用者范围和工作区权限| — |
| `GET` | `/accounts` | 列出关联的社交帐户| — |
| `POST` | `/posts` | 创建草稿或计划帖子| `create_posts`（+ `publish_directly` 计划） |
| `GET` | `/posts/{post_id}` | 阅读单个帖子| — |
| `PATCH` | `/posts/{post_id}` | 更新草稿字段 | `create_posts` |
| `POST` | `/posts/{post_id}/schedule` | 安排草稿 | `create_posts` + `publish_directly` |
| `POST` | `/posts/{post_id}/cancel` | 将预定帖子恢复为草稿| `create_posts` |
| `GET` | `/analytics/accounts/{account_id}` | 渠道分析摘要（7/30/90 天窗口） | `view_analytics` |
| `GET` | `/analytics/posts/{post_id}` | 使用每个平台指标进行后期分析| `view_analytics` |
| `POST` | `/media` | 上传媒体文件（分段） | `upload_media` |
| `GET` | `/media/{media_id}` | 检索媒体资产| — |
| `GET` | `/media` | 列出媒体资产（过滤、分页） | — |
| `POST` | `/mcp` | JSON-RPC MCP 个客户端的 2.0 端点 | — |

所有写入端点都接受 `idempotency_key` （或 `Idempotency-Key` 标头）以进行安全重试。

### MCP 工具

MCP 服务器位于 `POST {APP_URL}/api/v1/mcp`，并通过 Streamable HTTP 讲 JSON-RPC 2.0。它实现了标准`initialize`、`tools/list`、`tools/call` 和 `ping` 方法。工具：

| 工具 | 用途 | 权限 |
|---|---|---|
| `list_accounts` | 列出此 API 密钥可以作用的社交帐户 | — |
| `create_draft` | 创建草稿帖子（标题、标题、媒体、第一条评论、可选建议发布时间） | `create_posts` |
| `schedule_post` | 一步创建并安排帖子 | `create_posts` + `publish_directly` |
| `schedule_draft` | 安排现有草稿 | `create_posts` + `publish_directly` |
| `get_post` | 检索具有聚合状态和每个平台状态的帖子 | — |
| `cancel_post` | 将预定帖子恢复为草稿 | `create_posts` |
| `search_media` | 按查询、类型、标签或文件夹查找媒体资产 | — |
| `get_media` | 按 ID 检索单个媒体资产 | — |
| `upload_media` | 上传一个小型 Base64 编码文件（≤ 1 MB 原始文件）。对于较大的文件，请使用 REST `POST /media`。 | `upload_media` |
| `get_account_analytics` | 7-90 天滚动窗口的渠道分析 | `view_analytics` |
| `get_post_analytics` | 单个帖子的每平台指标（可安全投票草稿） 8800000000000003888 `view_analytics` |

### 连接 MCP 客户端

服务器位于 `{APP_URL}/api/v1/mcp`，支持两种身份验证模式 - 选择您的客户端使用的模式。

**Claude Desktop（和其他本机 OAuth 连接器）。** 在 Claude Desktop 中，打开 **设置 → 连接器 → 添加自定义连接器**，为其命名，然后输入服务器 URL `{APP_URL}/api/v1/mcp`。Claude 自行注册（动态客户端注册）并打开浏览器以登录 BrightBean Studio 并批准访问 — **否需要 API 密钥**。任何 Studio 用户都可以连接；连接以**他们自己的**工作区权限进行操作（只读角色获得读取工具，而发布/计划/上传需要匹配的权限），在其最后活动的工作区上进行操作。要求 Studio 通过公共 **https** URL 提供服务。

**Claude 代码、光标、自定义代理（静态 API 密钥）。** 将客户端指向同一个 URL 并发送 API 密钥作为承载令牌 (`Authorization: Bearer bb_studio_...`)。对于克劳德代码：

```bash
claude mcp add --transport http brightbean {APP_URL}/api/v1/mcp \
  --header "Authorization: Bearer bb_studio_..."
```

### 预建代理技能

不想连接您自己的客户端？配套的 [brightbean-studio-agent](https://github.com/brightbeanxyz/brightbean-studio-agent) 存储库托管整体代理技能，通过上面记录的 REST API 和 MCP 工具端到端驱动 BrightBean Studio。

---

## 技术堆栈

| 层 | 技术 |
|-------|-----------|
| 后端 | Django 5.x |
| 前端 | Django 模板、HTMX、Alpine.js |
| CSS | Tailwind CSS 4 通过 django-tailwind |
| 数据库 | PostgreSQL 16+ |
| 后台作业 | django-background-tasks（不需要 Redis） |
| 身份验证 | django-allauth （电子邮件 + Google OAuth） |
| 媒体 | 枕头（图像）、FFmpeg（视频） |
| 部署 | Docker、Gunicorn、Caddy |

---

## 故障排除

**Docker：`postgres` 容器不健康**
在 `docker compose up` 后等待 10-15 秒，让运行状况检查通过，然后重试命令。使用 `docker compose logs postgres` 检查日志。

**`python manage.py migrate` 因连接错误而失败**
确保 PostgreSQL 正在运行且健康。对于 Docker：`docker compose ps` 应将 postgres 显示为“健康”。对于本地：验证 `.env` 中的 `DATABASE_URL` 是否与您的设置匹配。

**Tailwind CSS 更改未出现**
确保 Tailwind 观察程序正在运行：`cd theme/static_src && npm run start`。如果样式仍然没有更新，请尝试 `npm run build` 进行完全重建。

**OAuth 回调错误（“重定向 URI 不匹配”）**
平台注册的重定向URI必须与`{APP_URL}/social-accounts/callback/{platform}/`完全匹配。检查`.env`中的88000000000002888是否与您正在访问的URL匹配（包括`http` 与 `https` 和端口号）。

**后台任务未运行（帖子未发布）**
确保工作进程正在运行：`python manage.py process_tasks`。在 Docker 中：检查 `docker compose logs worker`。

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解开发设置、编码指南以及如何提交拉取请求。

## 安全

要报告安全漏洞，请参阅 [SECURITY.md](SECURITY.md)。不要打开公共问题。

## 许可证

[AGPL-3.0](LICENSE) - 有关详细信息，请参阅 LICENSE。
