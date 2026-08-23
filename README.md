# Rotaeno_leaderboard_web_go

Rotaeno 玩家排行榜 Web 的 Go 重写版（上游：Rotaeno_leaderboard_web，本仓库工作在 `go` 分支）。

## 当前状态

仅搭建 Web 骨架（目录结构与占位文件），业务实现规划见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 目录

```
cmd/server       入口
internal/
  config         配置
  db             PostgreSQL 连接池
  models         数据结构
  services       查询服务层
  handlers       HTTP 路由/中间件/页面/API
  cache          内存缓存
  visit          访问计数
  scheduler      定时任务
templates/       网页模板
static/          前端资源
data/            数据文件
docs/            文档
```
