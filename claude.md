# 开发规范 (Claude.md)

## 代码风格
- **Python (后端)**: 遵循 PEP 8 规范。函数/变量使用 `snake_case`（蛇形命名），类使用 `PascalCase`（帕斯卡命名）。
- **JavaScript/Vue (前端)**: 遵循 Vue.js 风格指南。变量/函数使用 `camelCase`（驼峰命名），组件使用 `PascalCase`。
- **注释**: 复杂逻辑需编写清晰的注释。函数和类应使用文档字符串 (docstrings)。

## Git 提交信息规范
- 格式: `type(scope): subject`
- 类型 (Type):
  - `feat`: 新功能
  - `fix`: 修复 Bug
  - `docs`: 文档变更
  - `style`: 代码格式（不影响代码运行的变动）
  - `refactor`: 重构（既不是新增功能也不是修改 bug 的代码变动）
  - `test`: 增加测试
  - `chore`: 构建过程或辅助工具的变动
- 示例: `feat(auth): 实现登录接口`

## 文档维护
- 每次进行重大更改后，请更新 `progress.md` (进度) 和 `phase.md` (阶段设计)。
