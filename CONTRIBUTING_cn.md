# 为 Brightbean 做出贡献

感谢您有兴趣贡献！本指南将帮助您入门。

## 开始使用

1. 分叉存储库并克隆您的分叉
2.按照[README.md](README.md)中的设置说明进行操作（Docker或本地开发）
3. 安装预提交钩子（参见下面的[预提交钩子](#pre-commit-hooks)）
4.为你的工作创建一个分支：`git checkout -b your-branch-name`

### 预提交挂钩

我们使用 [pre-commit](https://pre-commit.com) 对每次提交运行 lint、格式、类型和秘密扫描检查。克隆后安装一次：

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

从那时起，钩子就会自动运行。要针对存储库中的每个文件运行它们（在引入较大更改后很有用）：

```bash
pre-commit run --all-files
```

这些钩子执行与 CI 相同的规则，因此在本地传递它们意味着您的 PR 将通过自动检查。

## 开发工作流程

### 运行应用程序

有关完整的设置说明，请参阅 [README](README.md)。快速版本：

```bash
cp .env.example .env
# Edit .env if needed (defaults work for local dev with Docker PostgreSQL)
docker compose up postgres -d
python manage.py migrate
python manage.py runserver
```

### 运行测试

```bash
pytest
```

覆盖范围：

```bash
pytest --cov=apps --cov-report=term-missing
```

### 代码风格

我们使用 [Ruff](https://docs.astral.sh/ruff/) 进行 linting 和格式化，使用 [mypy](https://mypy-lang.org/) 进行类型检查。在提交 PR 之前运行这些：

```bash
ruff check .              # lint
ruff format --check .     # format check
mypy apps/ config/ providers/ tests/ --ignore-missing-imports
```

自动修复 lint 和格式问题：

```bash
ruff check --fix .
ruff format .
```

CI 在每个 PR 上自动运行所有这些检查，以及 [gitleaks](https://github.com/gitleaks/gitleaks) 秘密扫描。切勿提交真实的 API 密钥、令牌或密码。将它们放入本地 `.env`（已 gitignored）中，并在 `.env.example` 中按名称引用它们。

## 提交更改

1. **保持 PR 的重点。** 每个 PR 一个功能或修复。小 PR 的审核速度更快。
2. **编写描述性提交消息。** 解释*什么*和*为什么*，而不仅仅是*如何*。
3. **添加新功能测试**或尽可能修复错误。
4. **确保 CI 通过。** PR 必须通过 lint、类型检查和测试检查。
5. **如果您的更改影响设置、配置或面向用户的行为，请更新文档**。

### 公关流程

1. 将你的分支推到你的叉子上
2. 针对 `main` 发起拉取请求
3.填写PR模板
4. [`.github/CODEOWNERS`](.github/CODEOWNERS) 中列出的维护者会自动请求审核
5.等待审核，我们会尽力在几天内回复
6.解决新提交中的审核反馈（在批准之前不要强制推送，以便审核者可以看到差异）
7.一旦获得批准，维护者会将你的 PR 压缩合并为 `main`

## 项目结构

```
apps/           # Django applications (accounts, composer, calendar, etc.)
providers/      # Social platform API integrations (one file per platform)
config/         # Django settings, URLs, WSGI/ASGI
templates/      # Django HTML templates
theme/          # Tailwind CSS theme (django-tailwind)
static/         # Static assets (JS, favicons)
tests/          # Test suite
```

## 添加新的社交平台提供商

提供商位于 `providers/`，每个平台一个文件。要添加新的：

1、创建`providers/your_platform.py`
2. 按照现有提供程序中的模式实现提供程序类（例如，简单示例为 `providers/bluesky.py`，完整 OAuth 流程为 `providers/facebook.py`）
3、主要实施方法：
   - `get_authorization_url()` - 构建 OAuth 重定向 URL
   - `exchange_code()` - 将授权码交换为令牌
   - `refresh_token()` - 刷新过期令牌
   - `publish()` - 发布内容到平台
   - `get_comments()` / `reply_to_comment()` - 收件箱支持（可选）
4. 在平台选择和连接流程中注册提供商
5、添加平台所需的环境变量为`.env.example`
6. 在 **Platform Credentials** 下的 README 添加设置说明
7.在`tests/providers/`中添加测试

## 报告错误

使用 GitHub 上的[错误报告模板](https://github.com/brightbeanxyz/brightbean-studio/issues/new?template=bug_report.yml)。包括：

- 重现步骤
- 预期行为与实际行为
- 您的环境（Docker/本地、操作系统、浏览器）

## 请求功能

使用 GitHub 上的[功能请求模板](https://github.com/brightbeanxyz/brightbean-studio/issues/new?template=feature_request.yml)。

## 安全问题

**不要针对安全漏洞公开发布问题。** 请参阅 [SECURITY.md](SECURITY.md) 了解负责任的披露说明。

## 许可证

通过贡献，您同意您的贡献将根据 [8800000000000000888-3.0 许可证](LICENSE) 获得许可。
