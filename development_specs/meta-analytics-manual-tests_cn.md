# 元分析手动测试计划

使用已授予分析范围的页面/Instagram 帐户并替换
具有真实值的 ID/令牌。

## 脸书页面

```text
/{page_id}/insights?metric=page_media_view,page_total_media_view_unique,page_follows,page_post_engagements&period=day&since={since}&until={until}
```

## 脸书帖子

```text
/{facebook_post_id}/insights?metric=post_media_view,post_total_media_view_unique,post_clicks,post_reactions_by_type_total
```

## Facebook 帖子字段

```text
/{facebook_post_id}?fields=id,message,created_time,permalink_url,full_picture,shares,comments.limit(0).summary(true),reactions.limit(0).summary(true)
```

## Instagram 用户

```text
/{ig_user_id}?fields=id,username,name,profile_picture_url,followers_count,media_count
```

## Instagram 帐户洞察

```text
/{ig_user_id}/insights?metric=reach,views,accounts_engaged,total_interactions&period=day&since={since}&until={until}
```

## Instagram 媒体字段

```text
/{ig_user_id}/media?fields=id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count
```

## Instagram 媒体洞察

```text
/{ig_media_id}/insights?metric=reach,views,likes,comments,saved,shares,total_interactions
```

预期的 UI 检查：

- Facebook 显示的是浏览量，而不是印象数。
- Facebook 使用反应，而不是点赞。
- Instagram 显示观看次数。
- 当观看次数和覆盖范围为 0 时，参与度为 0。
- 不支持的指标会记录警告，并且不会阻止仪表板加载。
- 7D、30D 和 90D 过滤器更新总计和图表数据。
- Instagram 关注者增长源自个人资料总数 `followers_count`（已弃用
  `profile_views` 不再请求洞察力，因此没有每次同步警告）。
