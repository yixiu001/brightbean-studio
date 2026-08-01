# BrightBean Studio 中文国际化设计

## 目标

为 BrightBean Studio 增加完整的简体中文与英文切换能力。首次访问默认显示简体中文，用户可在界面中切换英文，选择结果在后续请求中保持。同时为仓库内所有现有英文 Markdown 文档创建独立中文版本，不修改英文原文。

## 范围

### 网站界面

- 覆盖项目自有 Django 模板中的可见文案、标题、按钮、表单标签、占位符、空状态、提示、确认信息和无障碍标签。
- 覆盖项目自有 Python 代码向用户展示的校验错误、消息、通知和状态说明。
- 使用第三方依赖自身提供的语言包处理 Django Admin、django-allauth 和 django-oauth-toolkit 页面，不修改第三方包源码。
- 数据库中的用户内容、客户名称、帖子正文和平台返回内容不自动翻译。

### Markdown 文档

为以下 6 份文档在原目录创建中文版本：

- `README_cn.md`
- `CONTRIBUTING_cn.md`
- `SECURITY_cn.md`
- `development_specs/architecture_cn.md`
- `development_specs/feature-spec-social-media-management-v2_cn.md`
- `development_specs/meta-analytics-manual-tests_cn.md`

英文文档保持逐字不变。中文文档保留原文标题层级、表格、代码块、命令、文件路径、URL、变量名、接口字段和功能编号，只翻译自然语言内容。

## 技术方案

采用 Django 原生国际化体系：

- 默认语言设为简体中文 `zh-hans`。
- 支持语言为简体中文和英文。
- 在 SessionMiddleware 后加入 LocaleMiddleware。
- 添加 Django 官方 `set_language` 路由。
- 模板使用 `{% trans %}` 和 `{% blocktrans %}`。
- Python 使用 `gettext` 或 `gettext_lazy`。
- 中文翻译集中存放在 `locale/zh_Hans/LC_MESSAGES/django.po`，并编译生成 `django.mo`。
- 在全局导航提供中文 / English 切换入口。
- `<html lang>` 根据当前活动语言输出。
- 语言选择由 Django 的语言 Cookie 保持，HTMX 请求自动沿用该 Cookie。

## 组件与数据流

1. 首次请求没有语言 Cookie 时，Django 使用 `zh-hans`。
2. 用户点击语言切换入口，表单 POST 到 `set_language`。
3. Django 写入语言 Cookie，并重定向回当前页面。
4. 后续普通请求与 HTMX 请求由 LocaleMiddleware 激活相同语言。
5. 模板和 Python 消息通过 gettext 查找当前语言对应文本。

## 错误处理

- 缺少某条中文翻译时，Django 回退到代码中的英文原文，页面仍可使用。
- 切换语言后重定向地址只接受站内安全地址，避免开放重定向。
- 翻译不得修改格式化占位符、模板变量、HTML 结构或 API 字段。
- JavaScript 中的用户可见字符串优先通过模板翻译后注入；不能直接由模板提供的字符串使用 Django JavaScriptCatalog。

## 验证

- 配置测试：默认语言、支持语言、LocaleMiddleware 和语言路由正确。
- 切换测试：中文切英文、英文切中文、Cookie 保持和安全重定向。
- 页面测试：关键页面在两种语言下均正常渲染。
- 翻译检查：扫描项目自有模板与 Python 用户文案，检查未标记的英文字符串。
- Markdown 检查：6 个 `_cn.md` 文件全部存在，英文文件哈希保持不变，代码块和链接结构未被破坏。
- 回归测试：运行现有 Django 测试集和模板相关测试。

## 非目标

- 不翻译用户创建的内容或社交平台返回的数据。
- 不修改数据库结构。
- 不改变现有业务流程、页面布局或品牌视觉。
- 不为第三方依赖维护自定义翻译补丁。
