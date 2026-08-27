#!/usr/bin/env python3
"""Ultra-Scale Playbook 中文版构建脚本：
content/*.md → webapp/chapters/*.html + webapp/index.html
重新运行即可整站重建。
"""
import html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
WEBAPP = os.path.join(ROOT, "webapp")
CHAPDIR = os.path.join(WEBAPP, "chapters")

CHAPTERS = [
    dict(id="ch00", no="导论", zh="导论与全书鸟瞰", en="Introduction & High-Level Overview",
         desc="为什么要学大规模训练、全书地图与速查表。"),
    dict(id="ch01", no="第 1 章", zh="第一步：单 GPU 训练", en="First Steps: Training on one GPU",
         desc="Transformer 内存剖析、激活重计算与梯度累积。"),
    dict(id="ch02", no="第 2 章", zh="数据并行", en="Data Parallelism",
         desc="DP 通信与计算重叠、全局批量大小，与 ZeRO 1/2/3 分片。"),
    dict(id="ch03", no="第 3 章", zh="张量并行", en="Tensor Parallelism",
         desc="行/列切分线性层、Transformer 块的 TP 与序列并行。"),
    dict(id="ch04", no="第 4 章", zh="上下文并行", en="Context Parallelism",
         desc="超长序列的激活内存、Ring Attention 与 Zig-Zag 平衡。"),
    dict(id="ch05", no="第 5 章", zh="流水线并行", en="Pipeline Parallelism",
         desc="AFAB、1F1B、交错阶段到 Zero Bubble 与 DualPipe。"),
    dict(id="ch06", no="第 6 章", zh="专家并行", en="Expert Parallelism",
         desc="MoE 模型的专家分片与路由。"),
    dict(id="ch07", no="第 7 章", zh="5D 并行速览", en="5D Parallelism in a Nutshell",
         desc="DP／TP／SP／CP／PP／EP 六种并行策略的统一视角与组合原则。"),
    dict(id="ch08", no="第 8 章", zh="寻找最佳训练配置", en="Finding the Best Training Configuration",
         desc="三步：让模型装入内存、达到目标批量并最大化吞吐量；以及从数千组实测中总结的经验。"),
    dict(id="ch09", no="第 9 章", zh="深入 GPU：架构与内核", en="Diving in the GPUs: Architecture & Kernels",
         desc="GPU 架构速成、线程与内存层级、写出高效 kernel。"),
    dict(id="ch10", no="第 10 章", zh="融合内核、Flash Attention 与混合精度", en="Fused Kernels, Flash Attention & Mixed Precision",
         desc="kernel 融合、FA1-3 的内存魔法，与 FP32/BF16/FP8 训练。"),
    dict(id="ch11", no="结语", zh="结语与展望", en="Conclusion",
         desc="全书回顾、下一步，与致谢。"),
    dict(id="appa", no="附录 A0", zh="并行编程速成", en="A0: Parallel Programming Crash Course",
         desc="broadcast、all-reduce、scatter/gather 等集体通信操作。"),
    dict(id="appb", no="附录 A1", zh="分布式训练性能分析", en="A1: Distributed Training Profiling",
         desc="用 profiler 看懂 kernel 与通信的时间轴。"),
    dict(id="appc", no="附录 A2", zh="LLM 训练的典型尺度", en="A2: Typical Scales in LLM Training",
         desc="模型、批量、集群规模的数量级速查。"),
    dict(id="appd", no="附录 A3", zh="计算／通信重叠的数学", en="A3: Math for Compute/Communication Overlap",
         desc="各并行策略下重叠条件的推导。"),
    dict(id="references", no="参考资源", zh="参考资源", en="References",
         desc="里程碑论文，以及训练框架、调试与硬件方面的参考资料。"),
]

PAGE_TMPL = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Ultra-Scale Playbook 中文版</title>
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="../index.html">Ultra-Scale Playbook 中文版<span>在 GPU 集群上训练 LLM</span></a>
  <nav class="chapnav">{prev_top}<span class="chapnav-current">{no}</span>{next_top}<a class="gh-star" href="https://github.com/ai-twinkle/ultrascale-playbook-zh-tw" target="_blank" rel="noopener" data-gh-repo="ai-twinkle/ultrascale-playbook-zh-tw"><span class="star-ico">★</span><span class="gh-label">Star</span><b class="gh-count" hidden></b></a></nav>
</header>
<div class="layout">
  <aside class="sidebar"><nav id="toc" class="toc"><h2>本章目录</h2></nav></aside>
  <main class="main">
    <div id="lab-banner"></div>
    <article id="content" class="prose"></article>
    <section id="lab" class="lab" hidden>
      <h2 class="lab-title">🧪 交互实验室</h2>
      <div id="lab-intro"></div>
      <div id="lab-root"></div>
    </section>
    <nav class="pager">{prev_card}{next_card}</nav>
    <footer class="pagefoot">本站是 <a href="https://github.com/ai-twinkle">Twinkle AI Community</a>（台湾）制作的<strong>非官方社区译本</strong> · 译自 Hugging Face nanotron 团队《<a href="https://huggingface.co/spaces/nanotron/ultrascale-playbook">The Ultra-Scale Playbook</a>》· 原作基于 Apache 2.0 许可证发布，译文采用相同许可，仅供学习研究使用。</footer>
  </main>
</div>
<script type="text/markdown" id="chapter-md">
{md}
</script>
<script src="../assets/marked.min.js"></script>
<script src="../assets/katex/katex.min.js"></script>
<script src="../assets/katex/auto-render.min.js"></script>
{widget_tag}<script src="../assets/app.js"></script>
<script src="../assets/gh-star.js"></script>
</body>
</html>
"""

INDEX_TMPL = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ultra-Scale Playbook 中文版 — 在 GPU 集群上训练 LLM</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<section class="hero">
  <div class="eyebrow">简体中文全译本 · 交互版</div>
  <h1>超大规模训练实战手册<br>The Ultra-Scale Playbook</h1>
  <p class="sub">Hugging Face nanotron 团队著（Nouamane Tazi、Ferdinand Mom、Haojun Zhao、Phuc Nguyen、Mohamed Mekkouri、Leandro von Werra、Thomas Wolf）。内容从单 GPU 的内存分析讲起，逐步深入数据／张量／上下文／流水线／专家五维并行、GPU 内核优化与混合精度，系统介绍在 GPU 集群上训练大语言模型所需的关键知识。每章均配有交互实验。</p>
  <p class="sub" style="font-size:.82rem">由台湾 <a href="https://github.com/ai-twinkle">Twinkle AI Community</a> 翻译维护的非官方社区翻译版本。</p>
  <div class="meta">
    <div><b>{n_ch}</b>章节</div>
    <div><b>{n_app}</b>附录</div>
    <div><b>{n_fig}</b>插图</div>
    <div><b>{n_lab}</b>交互实验</div>
    <a href="https://github.com/ai-twinkle/ultrascale-playbook-zh-tw" target="_blank" rel="noopener" data-gh-repo="ai-twinkle/ultrascale-playbook-zh-tw"><b class="gh-count">—</b>GitHub ★</a>
  </div>
</section>
<div class="grid-wrap">
  <h2>章节</h2>
  <div class="chapter-grid">
{chapter_cards}
  </div>
  <h2>附录与资源</h2>
  <div class="chapter-grid">
{appendix_cards}
  </div>
</div>
<footer class="foot">本站是 <a href="https://github.com/ai-twinkle">Twinkle AI Community</a>（台湾）制作的<strong>非官方社区译本</strong>（unofficial community translation）· 译自 Hugging Face nanotron 团队《<a href="https://huggingface.co/spaces/nanotron/ultrascale-playbook">The Ultra-Scale Playbook: Training LLMs on GPU Clusters</a>》· 原作基于 Apache 2.0 许可证发布，译文采用相同许可 · 仅供学习研究使用 · <a href="https://github.com/ai-twinkle/ultrascale-playbook-zh-tw">GitHub 源代码</a></footer>
<script src="assets/gh-star.js"></script>
</body>
</html>
"""


def build_pages():
    os.makedirs(CHAPDIR, exist_ok=True)
    built = {c["id"]: os.path.exists(os.path.join(CONTENT, c["id"] + ".md")) for c in CHAPTERS}
    n_built = 0
    for i, ch in enumerate(CHAPTERS):
        if not built[ch["id"]]:
            continue
        with open(os.path.join(CONTENT, ch["id"] + ".md")) as f:
            md = f.read().replace("</script", "<\\/script")
        prev = next((c for c in reversed(CHAPTERS[:i]) if built[c["id"]]), None)
        nxt = next((c for c in CHAPTERS[i + 1:] if built[c["id"]]), None)
        prev_top = f'<a href="{prev["id"]}.html">← {prev["no"]}</a>' if prev else ""
        next_top = f'<a href="{nxt["id"]}.html">{nxt["no"]} →</a>' if nxt else ""
        prev_card = (f'<a class="prev" href="{prev["id"]}.html"><span class="dir">← 上一章</span>'
                     f'<div class="ttl">{prev["no"]}　{prev["zh"]}</div></a>') if prev else "<span></span>"
        next_card = (f'<a class="next" href="{nxt["id"]}.html"><span class="dir">下一章 →</span>'
                     f'<div class="ttl">{nxt["no"]}　{nxt["zh"]}</div></a>') if nxt else ""
        widget = os.path.join(WEBAPP, "assets", "widgets", ch["id"] + ".js")
        widget_tag = (f'<script src="../assets/widgets/{ch["id"]}.js"></script>\n'
                      if os.path.exists(widget) else "")
        page = PAGE_TMPL.format(
            title=f'{ch["no"]}　{ch["zh"]}', no=f'{ch["no"]}　{ch["zh"]}',
            prev_top=prev_top, next_top=next_top,
            prev_card=prev_card, next_card=next_card,
            md=md, widget_tag=widget_tag)
        with open(os.path.join(CHAPDIR, ch["id"] + ".html"), "w") as f:
            f.write(page)
        n_built += 1
    return built, n_built


def build_index(built):
    def card(ch):
        has_widget = os.path.exists(os.path.join(WEBAPP, "assets", "widgets", ch["id"] + ".js"))
        badge = '<span class="badge">交互实验</span>' if has_widget else ""
        inner = (f'{badge}<span class="no">{html.escape(ch["no"])}</span>'
                 f'<span class="zh">{html.escape(ch["zh"])}</span>'
                 f'<span class="en">{html.escape(ch["en"])}</span>'
                 f'<span class="desc">{html.escape(ch["desc"])}</span>')
        if built.get(ch["id"]):
            return f'    <a class="card" href="chapters/{ch["id"]}.html">{inner}</a>'
        return f'    <div class="card disabled">{inner}<span class="badge">翻译中</span></div>'

    main_ids = [c for c in CHAPTERS if c["id"].startswith("ch")]
    app_ids = [c for c in CHAPTERS if not c["id"].startswith("ch")]
    ch_cards = "\n".join(card(c) for c in main_ids)
    app_cards = "\n".join(card(c) for c in app_ids)
    figdir = os.path.join(WEBAPP, "assets", "images")
    n_fig = len(os.listdir(figdir)) if os.path.isdir(figdir) else 0
    widgets = os.path.join(WEBAPP, "assets", "widgets")
    n_lab = len([f for f in os.listdir(widgets) if f.endswith(".js")]) if os.path.isdir(widgets) else 0
    page = INDEX_TMPL.format(n_ch=12, n_app=4, n_fig=n_fig, n_lab=n_lab,
                             chapter_cards=ch_cards, appendix_cards=app_cards)
    with open(os.path.join(WEBAPP, "index.html"), "w") as f:
        f.write(page)


if __name__ == "__main__":
    built, n = build_pages()
    build_index(built)
    missing = [k for k, v in built.items() if not v]
    print(f"built {n} chapter pages; missing: {', '.join(missing) if missing else 'none'}")
