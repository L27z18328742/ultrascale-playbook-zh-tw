# 附录 A2　LLM 训练的典型尺度（Typical Scales in LLM Training）

> 译自 Hugging Face nanotron 团队《The Ultra-Scale Playbook: Training LLMs on GPU Clusters》（Apache 2.0），原文为 [Hugging Face Space](https://huggingface.co/spaces/nanotron/ultrascale-playbook)。

本节直观展示 LLM 训练中的典型数量级。讨论内存或计算量时，我们通常先计算“元素”（element）数量，也就是张量中数值的个数。要换算为实际内存字节数，还需乘以每个数值所占的空间，例如 bf16 为 2 字节、fp32 为 4 字节。

以下是一些快速的粗略估算数字：

- **输入 token**：每个批量我们会处理 $seq \cdot mbs$ 个 token，其中 $mbs$ 是微批量大小（micro-batch size），$seq$ 是序列长度。
- **激活值（隐藏状态）**：对单层而言，隐藏状态张量的大小为 $seq \cdot mbs \cdot h$ 个元素。
- **模型权重与梯度**：模型中的每个权重矩阵（例如线性层中的权重）大约有 $h^2$ 个元素。这是以单个权重矩阵计。梯度的大小与权重相同。
- **优化器状态**：对每个权重矩阵（$h^2$ 个元素）而言，如果你使用像 Adam 这类优化器搭配混合精度训练，它会以 fp32 精度保存动量（momentum）与方差（variance）状态（$2 \times 2h^2$），再加上 fp32 的主权重（master weights）（$2h^2$）。因此，每个权重矩阵的优化器状态总计约为 $6h^2$。
- **模型参数总量**：每个 transformer 块会存储：
  - 注意力参数：
    - QKV 投影：$3h^2$ 个参数
    - 输出投影：$h^2$ 个参数
  - 使用 GLU（Gated Linear Unit）的 MLP 参数：
    - Gate 与 up 投影：$8h^2$ 个参数（2 个大小为 $h \times 4h$ 的矩阵）
    - Down 投影：$4h^2$ 个参数（1 个大小为 $4h \times h$ 的矩阵）
  - 每个块总计：使用 GLU MLP 时为 $16h^2$，不使用 GLU 时为 $12h^2$
  - 完整模型：$16h^2 \cdot num\_layers$（使用 GLU 时）
  - 额外参数：
    - 输入嵌入（input embeddings）：$vocab\_size \cdot h$
    - LM head：$vocab\_size \cdot h$（若未与输入嵌入绑定共用）
    - 位置嵌入（若有使用）：$max\_seq\_len \cdot h$
- **前向与反向传播计算量（FLOPs）**：前向传播的 FLOPs 有一个非常粗略的估算式：$2 \cdot num\_tokens \cdot num\_params$。反向传播的计算量则是它的两倍：$4 \cdot num\_tokens \cdot num\_params$。

> 📝 **注**：更精确的前向＋反向传播 FLOPs 公式应为 $6 \cdot seq\_len \cdot num\_params + 12 \cdot num\_layers \cdot h \cdot seq\_len^2$，它把注意力运算在整条序列上的二次方扩展也纳入考虑；但为了简化数学，我们假设 $seq\_len^2 \ll h$。
