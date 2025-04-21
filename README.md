# CC Bucks 积分管理系统

本项目是一个基于 Flask + HTML/JS 的家庭行为积分管理系统，适用于家庭内部对孩子行为进行量化管理和奖励。系统支持行为自定义、积分自动统计、周积分目标、积分兑换等功能。

## 主要功能

- **行为自定义**：支持按类别和频率（每日、每周、偶尔）自定义行为及其积分。
- **自动积分统计**：勾选行为或填写次数后自动加/减积分，积分实时同步。
- **多孩子支持**：可为多个孩子分别管理积分，切换不会丢失各自的行为记录。
- **积分进度展示**：每周积分进度条、总积分展示，支持兑换规则说明。
- **行为表格**：支持按类别和频率查看所有行为及分数。
- **行为编辑**：支持拖拽排序和分数修改，实时保存到后端。
- **本地状态保存**：每个孩子的行为勾选和输入状态自动保存在浏览器本地，切换不会丢失。

## 项目结构

```
cc_bucks/
│
├── app.py                  # Flask 后端主程序
├── behaviors.json          # 行为定义（支持编辑）
├── points.json             # 积分数据（自动生成/更新）
├── calc_max_weekly_score.py# 计算理论最高周积分脚本
├── requirements.txt        # Python依赖
│
├── static/
│   ├── index.html                  # 主页面（积分管理）
│   ├── behaviors.html              # 行为表（按类别）
│   ├── behaviors_by_frequency.html # 行为表（按频率）
│   ├── behaviors_by_category.html  # 行为表（按类别）
│   ├── edit_behaviors.html         # 行为编辑页面
│   ├── css/
│   │   └── style.css               # 页面样式
│   └── js/
│       ├── behaviors.js            # 行为表格渲染逻辑
│       └── common.js               # 通用JS工具
```

## 快速开始

1. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

2. **运行服务**

   ```bash
   python app.py
   ```

3. **访问系统**

   打开浏览器访问 [http://localhost:5000](http://localhost:5000)

## 主要页面说明

- **Dashboard（index.html）**  
  行为打卡、积分进度、孩子切换、积分自动统计。

- **Behaviors Table（behaviors.html, behaviors_by_frequency.html, behaviors_by_category.html）**  
  查看所有行为及分数，支持按类别/频率分组。

- **Edit Behaviors（edit_behaviors.html）**  
  拖拽排序、修改分数，保存后自动同步到后端。

## 数据说明

- **behaviors.json**  
  行为定义，包含名称、描述、类别、频率、分数等字段。

- **points.json**  
  每个孩子的总积分、周积分，自动维护。

## 技术栈

- 后端：Python 3 + Flask
- 前端：HTML5 + Bootstrap 5 + 原生 JS
- 数据存储：JSON 文件

## 注意事项

- 本系统为本地家庭使用，未做复杂权限和安全校验。
- 所有积分和行为状态仅保存在本地浏览器和服务器端 JSON 文件。
- 如需重置积分或行为，直接编辑对应 JSON 文件或在页面操作。

## License

MIT License

---

如有问题或建议，欢迎反馈！