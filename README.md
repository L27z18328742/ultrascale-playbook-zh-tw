# Ultra-Scale Playbook 中文版 — 超大规模训练实战手册（交互版）

> **非官方社区翻译（Unofficial Community Translation）**
> 本项目是 Hugging Face nanotron 团队《[The Ultra-Scale Playbook: Training LLMs on GPU Clusters](https://huggingface.co/spaces/nanotron/ultrascale-playbook)》的简体中文（zh-CN）完整译本，由台湾 [Twinkle AI Community](https://github.com/ai-twinkle) 翻译并维护。原作者：Nouamane Tazi、Ferdinand Mom、Haojun Zhao、Phuc Nguyen、Mohamed Mekkouri、Leandro von Werra、Thomas Wolf。原作基于 Apache 2.0 许可证发布，译文采用相同许可。

**📖 在线阅读：<https://apps.twinkleai.tw/ultrascale-playbook-zh-tw/>**

从单 GPU 的内存剖析出发，一路走到数据／张量／上下文／流水线／专家五维并行、GPU kernel 优化与混合精度训练。**每一章都配备交互实验**——原网页的交互图表精神在中文版以自制组件重现。

## 交互实验一览

| 章节 | 实验 |
|---|---|
| 导论 | 5D 并行策略交互地图 |
| 第 1 章 单 GPU 训练 | 内存计算器（权重/梯度/优化器/激活 + 重计算策略） |
| 第 2 章 数据并行 | ZeRO 1/2/3 内存分片可视化 |
| 第 3 章 张量并行 | column/row-linear 切分动画 + TP/SP 流程 |
| 第 4 章 上下文并行 | Ring Attention 动画 + Zig-Zag 负载平衡 |
| 第 5 章 流水线并行 | AFAB vs 1F1B 气泡调度模拟器 |
| 第 6 章 专家并行 | MoE 路由与 all-to-all 可视化 |
| 第 7 章 5D 并行速览 | 5D 配置探索器（GPU 网格图 + 合理性检查） |
| 第 8 章 最佳配置 | 三步配置向导 |
| 第 9 章 深入 GPU | 矩阵乘 tiling 与内存合并动画 |
| 第 10 章 FA 与混合精度 | 浮点格式探索器（FP32/BF16/FP16/FP8） |
| 结语 | 全书回顾小测验 |
| 附录 A0–A3 | 集体通信动画台／profiler trace 示例／数量级计算器／重叠条件计算器 |

## 目录结构与使用

```
├── content/          # 逐章译文 Markdown（12 章 + 4 附录 + 参考资源）
├── webapp/           # 交互网站（纯静态、可离线使用）
├── src/              # 原文 HTML 与 bibliography（对照用）
├── ultra_blog.md     # 原文 markdown 来源
└── build.py          # 构建：content/*.md → webapp
```

```bash
cd webapp && python3 -m http.server 8643   # 浏览 http://localhost:8643
```

修改译稿或组件后，重新运行 `python3 build.py`。

## 翻译说明

- 以原始 `ultra_blog.md` 为主要底本、`src/index.html`（distill 源代码）为对照，还原格式转换遗失的数学定界符、修复损坏的代码块
- 原网页中的交互图表用“🔬”标记并链接回原文；如有静态版本，也会一并附上
- 并行策略缩写（DP/TP/PP/CP/EP/SP）、ZeRO、集体通信操作名（all-reduce 等）保留英文
- 134 张插图取自原始 assets（非 PDF 抽取）

## Citation

引用原作：

```bibtex
@misc{ultrascale_playbook,
  title={The Ultra-Scale Playbook: Training LLMs on GPU Clusters},
  author={Nouamane Tazi and Ferdinand Mom and Haojun Zhao and Phuc Nguyen and Mohamed Mekkouri and Leandro Werra and Thomas Wolf},
  year={2025},
  publisher={Hugging Face},
  url={https://huggingface.co/spaces/nanotron/ultrascale-playbook}
}
```
