# Easyjb dev note

- LOG:
  - 重新启用了Xshell+Xftp8，因为涉及到了大文件传输(9G的压缩包)，浏览器和vscode上传都经常中断
    - 传的也挺慢的，几MB每秒，哈哈
  - [Copilot tutorial](https://vscode.js.cn/docs/copilot/copilot-chat)

- TODO：
  - EasyJailbreak框架阅读
  - **更简便的图形化控制面板**，一键执行越狱攻击，类似整合包
    - 这个框架还挺好的，起码一键安装依赖能跑起来，有的byd代码依赖都有冲突
- 问题1：Vscode远程连接autodl后，无法使用copilot
  - 解决：**远程与本地共享一个我fork的仓库，在本地进行开发，远程每次进行`git pull`然后调试代码；或者在本地也配置好`wsl`的环境，调试好了再上远程**
    - 进一步解决：原来只是我把对话框扔到右边去了，导致左边侧边栏没找到，`Ctrl+I`调出来就好了，fuck me
- 问题2：Vscode ssh的markdown扩展，实在是太卡了
  - 解决：禁用所有扩展，代价就是现在我要手动输入`tab`(两个空格)
    - 还是卡，复制粘贴都得卡半天，git也卡，什么都卡，是因为vscode in ssh占用的是远程机器的资源吗，0.5核2G
    - 最终解决：还是在wsl上调试、做笔记，然后部署到远程机器上吧，不然要卡死我，哈哈

## attacker

## constraint

- `ConstraintBase.py`：定义抽象约束基类 `ConstraintBase`
- `DeleteHarmLess.py`：

## selector

### EXP3SelectPolicy

EXP3（Exponential-weight algorithm for Exploration and Exploitation）是一种用于多臂老虎机问题的算法，旨在平衡探索和利用之间的权衡。该算法的核心思想是通过指数加权的方法来选择动作（或实例），并根据反馈动态调整权重。

以下是该选择算法的核心原理：

1. **初始化**：
    * 在初始化阶段，所有实例的权重都设置为1。权重表示每个实例被选择的优先级。
    * 概率列表初始化为0，用于存储每个实例被选择的概率。

2. **选择实例**：
    * 在选择阶段，算法根据当前的权重计算每个实例被选择的概率。概率计算公式如下：
      \[
      p_i = (1 - \gamma) \frac{w_i}{\sum_{j} w_j} + \frac{\gamma}{n}
      \]
      其中，\( p_i \) 是第 \( i \) 个实例被选择的概率，\( w_i \) 是第 \( i \) 个实例的权重，\( \gamma \) 是控制探索和利用权衡的参数，\( n \) 是实例的总数。
    * 根据计算出的概率分布，随机选择一个实例。

3. **更新权重**：
    * 在选择实例后，根据实例的反馈（奖励或损失）更新权重。更新公式如下：
      \[
      w_i \leftarrow w_i \cdot \exp\left( - \frac{\gamma \cdot \text{reward}}{p_i \cdot n}\right)
      \]
      其中，\( \text{reward} \) 是实例的反馈，\( p_i \) 是实例被选择的概率，\( n \) 是实例的总数。
    * 通过这种方式，表现好的实例（高奖励）会增加其权重，从而在未来更有可能被选择。

4. **探索与利用**：
    * 参数 \( \gamma \) 控制探索和利用之间的权衡。当 \( \gamma \) 较大时，算法更倾向于探索（随机选择实例）；当 \( \gamma \) 较小时，算法更倾向于利用（选择权重较大的实例）。

### MCTSExploreSelectPolicy

#### 数学公式总结：

```markdown
1. 节点选择得分：
   \[
   \text{Score}(pn) = \frac{\text{rewards}[pn.index]}{pn.visited\_num + 1} + \text{ratio} \cdot \sqrt{\frac{2 \log(\text{step})}{pn.visited\_num + 0.01}}
   \]

2. 更新奖励：
   \[
   \text{reward} = \frac{\text{succ\_num}}{|\text{Questions}| \times |\text{prompt\_nodes}|}
   \]

3. 奖励更新：
   \[
   \text{rewards}[prompt\_node.index] += \text{reward} \times \max(\beta, 1 - 0.1 \times \text{last\_choice\_node.level})
   \]
```

#### 1. `__init__` 方法（初始化）

`__init__` 方法初始化了 `MCTSExploreSelectPolicy` 类的实例。这个方法设置了选择策略的基本参数，并为后续的选择和更新过程准备了所需的变量。

##### 核心步骤：
- `dataset`：初始化时传入的数据集，从中选择实例。
- `inital_prompt_pool`：初始的提示池，包含一组开始时用于选择的提示。
- `Questions`：要回答的任务或问题集，供选择的实例使用。
- `ratio`：控制探索与利用之间的平衡的参数。默认值为 0.5。
- `alpha`：用于控制探索时跳出子节点的概率，值越高则越倾向于探索新的节点。
- `beta`：奖励缩放因子，用于调整节点的奖励值。
- `step`：步骤计数器，用于计算 MCTS 中的探索部分。
- `mctc_select_path`：选择路径，记录所选节点的历史路径。
- `last_choice_index`：上次选择的节点的索引。
- `rewards`：存储每个节点的奖励，用于评估节点的选择效果。

##### 数学描述：
- `ratio` 控制了探索和利用的权重，`alpha` 和 `beta` 控制了节点选择过程中的惩罚和奖励因素。

```python
self.ratio = ratio
self.alpha = alpha
self.beta = beta
```

#### 2. `select` 方法（选择策略）

`select` 方法根据蒙特卡洛树搜索（MCTS）算法选择一个实例。它平衡了**探索**和**利用**，并使用已知的奖励信息指导选择过程。

##### 核心步骤：
1. **初始化和奖励扩展**：
   - 如果数据集中包含的实例数大于奖励列表的长度，扩展奖励列表。
   
2. **选择当前节点**：
   - 从初始提示池中选择一个节点 `cur`。选择的标准是：
     \[
     \text{Score}(pn) = \frac{\text{rewards}[pn.index]}{pn.visited\_num + 1} + \text{ratio} \cdot \sqrt{\frac{2 \log(\text{step})}{pn.visited\_num + 0.01}}
     \]
     其中：
     - `rewards[pn.index]` 是节点的当前奖励。
     - `pn.visited_num` 是节点的访问次数。
     - `step` 是当前的步骤数。
     - `ratio` 控制了探索与利用的平衡，`log(step)` 则反映了随着步骤增加而对未被充分探索节点的偏好。

3. **递归选择子节点**：
   - 若当前节点有子节点，则继续从子节点中选择，直到到达叶节点或者随机跳出。选择子节点的标准与选择当前节点相同。

4. **更新访问次数**：
   - 在选择路径上的所有节点的 `visited_num` 加 1。

5. **返回选择的节点**：
   - 返回所选择的实例。

##### 数学公式：
选择一个节点的得分：
\[
\text{Score}(pn) = \frac{\text{rewards}[pn.index]}{pn.visited\_num + 1} + \text{ratio} \cdot \sqrt{\frac{2 \log(\text{step})}{pn.visited\_num + 0.01}}
\]

#### 3. `update` 方法（更新策略）

`update` 方法根据所选节点的表现（成功次数）更新 MCTS 树中的节点权重。更新的奖励依据是节点的表现，并通过奖励缩放因子 `beta` 进行调整。

##### 核心步骤：
1. **计算成功数量**：
   - `succ_num` 计算的是当前提示节点（`prompt_nodes`）中成功破狱的数量，即每个节点的 `num_jailbreak` 总和。

2. **更新节点奖励**：
   - 对选择路径上的每个节点进行奖励更新。更新的公式为：
     \[
     \text{reward} = \frac{\text{succ\_num}}{|\text{Questions}| \times |\text{prompt\_nodes}|}
     \]
     - 其中，`succ_num` 是成功的次数，`Questions` 是问题集，`prompt_nodes` 是当前更新的节点集。

3. **应用缩放因子**：
   - 更新节点的奖励时，还需要应用一个奖励缩放因子 `beta`，以进一步调整节点的权重：
     \[
     \text{rewards}[prompt\_node.index] += \text{reward} \times \max(\beta, 1 - 0.1 \times \text{last\_choice\_node.level})
     \]
     - `beta` 是一个奖励缩放因子，`last_choice_node.level` 用来控制节点的奖励下降速率。

##### 数学公式：
更新的奖励为：
\[
\text{reward} = \frac{\text{succ\_num}}{|\text{Questions}| \times |\text{prompt\_nodes}|}
\]
奖励更新公式：
\[
\text{rewards}[prompt\_node.index] += \text{reward} \times \max(\beta, 1 - 0.1 \times \text{last\_choice\_node.level})
\]

### UCBSelectPolicy

UCB（上置信度界限）算法，以选择从GPTFuzzer收集的后续更新的种子。

1. UCB得分：
   \[
   \text{score}_i = \frac{\text{rewards}[i]}{\text{smooth\_visited\_num}} + \text{explore\_coeff} \cdot \sqrt{\frac{2 \log(\text{step})}{\text{smooth\_visited\_num}}}
   \]

2. 更新奖励：
   \[
   \text{rewards}[self.last\_choice\_index] += \frac{\text{succ\_num}}{\text{len(Dataset)}}
   \]

### RoundRobinSelectPolicy

RoundRobinSelectPolicy 是一种基于 轮询（Round-Robin）策略的选择策略。该策略按顺序循环选择数据集中的实例，选择完所有实例后重新从头开始。

1. 选择实例：
   \[
   \text{index} = (\text{index} + 1) \% \text{len(Datasets)}
   \]
   
2. 更新索引：
   \[
   \text{index} = (\text{index} - 1 + \text{len(Datasets)}) \% \text{len(Datasets)}
   \]

### SelectBasedOnScores

基于 评分（scores）的选择策略。

```markdown
1. 随机打乱数据集中的实例顺序：
   \[
   \text{np.random.shuffle}(list\_dataset)
   \]

2. 按评分排序（降序）：
   \[
   \text{list\_dataset.sort}(key = \lambda x: x.eval\_results[-1], \text{reverse} = True)
   \]

3. 选择评分大于 0 的实例：
   \[
   \text{truncated\_list} = \left[ \text{list\_dataset}[i] \, | \, x.eval\_results[-1] > 0 \right]
   \]

4. 保证至少选择两个实例：
   \[
   \text{if len(truncated\_list) == 0: truncated\_list = [list\_dataset[0], list\_dataset[1]]}
   \]

### 