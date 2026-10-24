# SmartStock 智能量化交易系统

<p align="center">
  <img src="docs/logo.png" alt="SmartStock" width="200"/>
</p>

<p align="center">
  <a href="https://gitee.com/enjoydt/smartstock">
    <img src="https://img.shields.io/badge/Gitee-SmartStock-green" alt="Gitee">
  </a>
  <a href="https://gitee.com/enjoydt/smartstock">
    <img src="https://img.shields.io/badge/Version-1.0-blueprint" alt="Version">
  </a>
</p>

---

## 📖 项目简介

**SmartStock** 是一款面向个人投资者的智能量化交易辅助系统，致力于让专业的量化交易不再遥不可及。系统集成 AI 量化助手，提供量化自选、量化选股、策略管理、舆情监控、智能盯盘等核心功能，帮助投资者科学决策、提升投资效率。

---

## 🎯 核心功能

### 1️⃣ 量化自选
![量化自选](docs/quant_selected.png)

个性化管理您关注的股票，实时监控行情变化，智能分析趋势，助您把握投资机会。

- 一键添加关注股票，自定义分类管理
- 实时行情监控，异动提醒
- 多维度数据分析，提供投资参考
- 历史走势对比，把握市场脉搏

### 2️⃣ 量化选股
![量化选股](docs/quant_select.png)

基于多因子模型的智能选股系统，通过大数据分析和机器学习算法，帮您筛选优质股票。

- 多种选股策略，满足不同投资风格
- 自定义选股条件，灵活组合指标
- 回测验证，提升选股成功率
- 定期更新，把握市场热点

### 3️⃣ 策略管理
![策略管理](docs/strategy.png)

创建、测试和管理您的量化交易策略。

- 丰富的技术指标和交易条件
- 策略回测和优化，提升策略表现
- 策略组合管理，分散投资风险

### 4️⃣ 舆情监控
![舆情监控](docs/quant_news.png)

实时采集和分析市场新闻、社交媒体、研究报告等信息，帮您把握市场情绪和热点。

- 多渠道信息整合，全面了解市场舆情
- 智能情感分析，把握市场情绪变化
- 关键词监控，不错过重要信息
- 关联分析，发现潜在投资机会

### 5️⃣ 智能盯盘
![智能盯盘](docs/quant_monitor.png)

7×24 小时监控市场变化，根据您设置的策略自动推送买卖点和买卖金额建议。

- 自带小程序端，方便随时随地监控
- 实时监控市场变化，不错过交易时机
- 智能分析买卖点，提供交易建议
- 个性化风险控制，保障资金安全
- 多渠道提醒，及时获取交易信号

---

## 🛠️ 技术架构
- **后台框架**：Pear Admin Flask
- **前端**：Layui + HTML5 + CSS3
- **后端**：Python + Flask
- **小程序**：Vue.js + TypeScript + uni-app
- **数据库**：MySQL
- **量化引擎**：支持 Python 策略编写与回测

---

## 项目优势 
1、可作为搭建个人量化交易系统的基础框架，极易二次开发。  
2、个人量化交易辅助系统，无需专业基础即可使用。  
3、完全开源免费，您可以自由使用、修改和分发。     

---
## 启动
1、导入数据库文件：docs/db.sql  
2、修改数据库配置：applications/config.py  
3、启动项目
```shell 
pip install -r requirements.txt  # 安装依赖  
python app.py  # 启动项目  
```
管理员账号：admin  
管理员密码：123456  

4、如需启动小程序：
```shell
cd minapp  # 进入小程序目录
npm install  # 安装依赖
npm run dev  # 启动小程序
```

## 📦 开源声明

本项目完全开源免费，您可以自由使用、修改和分发。

🔗 **Gitee 仓库**：[https://gitee.com/enjoydt/smartstock](https://gitee.com/enjoydt/smartstock)

---

## 🚀 立即体验

[开启您的量化交易之旅](https://gitee.com/enjoydt/smartstock) —— 让智能算法成为您的投资助手，提升投资效率和收益。

---

## 如果觉得项目有帮助，请给它一个 Star 🌟
<p align="center">
  <a href="https://gitee.com/enjoydt/smartstock">
    <img src="https://img.shields.io/badge/Star-1000-blueprint" alt="Star">
  </a>
</p>
