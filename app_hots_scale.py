import random
import math
from html import escape

import streamlit as st
import plotly.graph_objects as go


# =========================================================
# 页面配置
# =========================================================
st.set_page_config(
    page_title="GenAI-HOTS 高阶思维能力自评",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.7rem 1.8rem;
        border: 1px solid rgba(49, 51, 63, 0.18);
        border-radius: 18px;
        margin-bottom: 1.2rem;
    }
    .score-box {
        padding: 1.4rem 1.2rem;
        border: 1px solid rgba(49, 51, 63, 0.18);
        border-radius: 16px;
        text-align: center;
        height: 100%;
    }
    .score-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.05;
        margin: .2rem 0 .3rem 0;
    }
    .muted {
        opacity: .72;
        font-size: .92rem;
    }
    .dimension-card {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(49, 51, 63, 0.16);
        border-radius: 14px;
        margin-bottom: .85rem;
    }
    .small-tag {
        display: inline-block;
        border: 1px solid rgba(49, 51, 63, 0.20);
        border-radius: 999px;
        padding: .18rem .55rem;
        font-size: .82rem;
        margin-right: .35rem;
    }
    div[data-testid="stRadio"] > label {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 量表：来自“高阶思维能力自评”
# 共 7 个维度、23 个题项
# =========================================================
QUESTIONS = [
    # 批判性思维能力（4）
    {
        "dimension": "批判性思维能力",
        "text": "在面对生成式 AI 提供的信息时，我会有意识地判断其准确性和可靠性。",
    },
    {
        "dimension": "批判性思维能力",
        "text": "我会将 AI 的答案与其他来源的信息进行对比，以发现可能存在的矛盾或偏见。",
    },
    {
        "dimension": "批判性思维能力",
        "text": "我能识别出 AI 生成内容中逻辑不清晰或证据不足的部分。",
    },
    {
        "dimension": "批判性思维能力",
        "text": "即使 AI 给出了一个现成答案，我仍倾向于自己深入思考问题的本质。",
    },

    # 创造性思维能力（4）
    {
        "dimension": "创造性思维能力",
        "text": "我能利用生成式 AI 产生新颖、独特的想法或解决方案。",
    },
    {
        "dimension": "创造性思维能力",
        "text": "AI 提供的灵感能够帮助我打破思维定势，从新的角度思考问题。",
    },
    {
        "dimension": "创造性思维能力",
        "text": "我经常将 AI 生成的不同元素进行组合、重构，以创造出新的内容。",
    },
    {
        "dimension": "创造性思维能力",
        "text": "使用 AI 后，我感觉自己在学习和创作中的想象力更丰富了。",
    },

    # 问题解决能力（3）
    {
        "dimension": "问题解决能力",
        "text": "遇到复杂学习任务时，我会先利用 AI 拆解问题，再把大目标分成可执行的小步骤。",
    },
    {
        "dimension": "问题解决能力",
        "text": "当原有方法无效时，我会借助 AI 提供的多种思路，主动尝试新的解题策略。",
    },
    {
        "dimension": "问题解决能力",
        "text": "面对真实情境问题（课程设计、项目实践等），我能综合 AI 建议与多方信息，拟定可行方案。",
    },

    # 自我调节学习能力（3）
    {
        "dimension": "自我调节学习能力",
        "text": "使用 AI 前，我会给自己设定清晰的学习目标与时间安排，并告知 AI 我的需求边界。",
    },
    {
        "dimension": "自我调节学习能力",
        "text": "发现 AI 反馈效率不高时，我会主动调整提示词或更换学习策略。",
    },
    {
        "dimension": "自我调节学习能力",
        "text": "学习结束后，我会根据 AI 输出与实际效果的差距，适当修改下一步的学习方法与资源选择。",
    },

    # 人机协同能力（3）
    {
        "dimension": "人机协同能力",
        "text": "使用各类数字工具（含 AI）时，我会针对自己的需求设计合适的提问或操作方式。",
    },
    {
        "dimension": "人机协同能力",
        "text": "当 AI 结果不理想时，我能通过补充信息、调整提示或切换工具，让输出更符合我的需求。",
    },
    {
        "dimension": "人机协同能力",
        "text": "我善于把 AI 给出的建议与自己的想法结合，形成更完善的解决方案或作品。",
    },

    # 元认知能力（3）
    {
        "dimension": "元认知能力",
        "text": "借助与 AI 的对话，我能主动觉察自己是否真正理解当前内容，而非“看过去就算”。",
    },
    {
        "dimension": "元认知能力",
        "text": "我大致清楚自己在哪些知识或能力上比较薄弱，并会利用 AI 进行针对性训练。",
    },
    {
        "dimension": "元认知能力",
        "text": "完成一项 AI 辅助任务后，我会反思：本次人机协同中哪些地方高效、哪些地方流于表面。",
    },

    # 计算思维能力（3）
    {
        "dimension": "计算思维能力",
        "text": "在分析问题时，我会先用 AI 帮我提取关键变量及其关系，再构建解决框架。",
    },
    {
        "dimension": "计算思维能力",
        "text": "面对多步骤任务，我能够借助 AI 设计出清晰、有逻辑的操作流程图或伪代码。",
    },
    {
        "dimension": "计算思维能力",
        "text": "遇到重复性学习任务时，我会利用 AI 生成脚本、公式或宏命令，实现自动化处理。",
    },
]

DIMENSIONS = [
    "批判性思维能力",
    "创造性思维能力",
    "问题解决能力",
    "自我调节学习能力",
    "人机协同能力",
    "元认知能力",
    "计算思维能力",
]

DIMENSION_INFO = {
    "批判性思维能力": {
        "meaning": "关注你是否会核验 AI 信息、识别逻辑与证据问题，并保持独立判断。",
        "tips": [
            "对重要 AI 结论执行“二次核验”：至少找 1 个独立来源交叉验证。",
            "看到结论时追问三个问题：证据是什么？是否有反例？还可能有哪些解释？",
            "让 AI 先给答案，再要求它列出假设、证据不足处和可能的错误点，由你最终判断。",
        ],
    },
    "创造性思维能力": {
        "meaning": "关注你能否借助 AI 打破思维定势、重组信息，并形成有自己特色的新想法。",
        "tips": [
            "同一问题要求 AI 从 3 种完全不同的角色或视角提出方案，再自行筛选与重组。",
            "不要直接采用第一个答案，至少生成 3 个版本，比较后再形成自己的方案。",
            "练习“组合创新”：把两个看似不相关的概念、案例或方法进行重新连接。",
        ],
    },
    "问题解决能力": {
        "meaning": "关注你能否拆解复杂任务、比较多种路径，并把 AI 建议转化为可执行方案。",
        "tips": [
            "复杂任务先写清“目标—约束—步骤—验证标准”，再让 AI 辅助补充。",
            "遇到卡点时，不只问“答案是什么”，而要问“有哪些路径、各自风险是什么”。",
            "完成方案后做一次可行性检查：资源、时间、风险、替代方案是否明确。",
        ],
    },
    "自我调节学习能力": {
        "meaning": "关注你是否能在使用 AI 前设定目标，在过程中调整策略，并在结束后复盘。",
        "tips": [
            "使用 AI 前先写下本次任务目标和“哪些部分必须自己完成”。",
            "给 AI 使用设置时间上限，例如 20 分钟后必须回到自己的整理与输出。",
            "每次任务结束记录一句：AI 帮助了什么、干扰了什么、下次要怎么改。",
        ],
    },
    "人机协同能力": {
        "meaning": "关注你能否通过提问、补充信息和工具切换，让 AI 真正服务于自己的目标。",
        "tips": [
            "提示词中明确四项：任务目标、背景信息、限制条件、期望输出格式。",
            "第一次结果不理想时，不直接重来；指出具体问题并逐轮补充上下文。",
            "把 AI 定位为“协作伙伴”：AI 负责发散与整理，你负责判断、取舍和最终负责。",
        ],
    },
    "元认知能力": {
        "meaning": "关注你是否清楚自己会什么、不会什么，并能监控“我是否真的理解”。",
        "tips": [
            "学完后关闭 AI，用自己的话复述核心内容；说不清的地方就是下一步重点。",
            "让 AI 出 3 个递进问题进行自测，但答案先由你独立作答，再进行对照。",
            "建立“知识薄弱清单”，记录反复出错的概念、步骤或判断点。",
        ],
    },
    "计算思维能力": {
        "meaning": "关注你能否识别变量关系、设计流程，并把重复任务转化为规则或自动化步骤。",
        "tips": [
            "遇到复杂问题先画流程：输入是什么、处理步骤是什么、输出是什么。",
            "把多步骤任务写成伪代码或编号流程，再让 AI 帮你检查逻辑遗漏。",
            "对重复操作主动寻找可复用模板、公式、脚本或自动化方式。",
        ],
    },
}


# =========================================================
# 评分函数
# =========================================================
def mean(values):
    return sum(values) / len(values) if values else 0.0


def to_ten_point(likert_mean):
    """
    1~5 级量表线性转换为 0~10 分：
    1 -> 0
    3 -> 5
    5 -> 10
    """
    return round((likert_mean - 1) / 4 * 10, 2)


def score_level(score):
    # 10 分制，显示更细的层级
    if score >= 9.0:
        return "卓越"
    if score >= 8.0:
        return "优秀"
    if score >= 7.0:
        return "良好"
    if score >= 6.0:
        return "中上"
    if score >= 5.0:
        return "中等"
    if score >= 4.0:
        return "发展中"
    return "优先提升"


def dimension_status(score):
    if score >= 8.5:
        return "优势突出"
    if score >= 7.0:
        return "表现良好"
    if score >= 5.5:
        return "基本稳定"
    if score >= 4.0:
        return "仍有提升空间"
    return "建议优先训练"


def overall_interpretation(score, spread):
    if score >= 8.5:
        base = "你的高阶思维自评整体处于较高水平，说明你在 AI 辅助学习中已经形成较成熟的判断、调节与协作意识。"
    elif score >= 7.0:
        base = "你的整体表现较好，多数高阶思维环节已经能够主动使用，但仍有少数维度可以进一步从“会用”提升到“稳定、可迁移地使用”。"
    elif score >= 5.5:
        base = "你的整体表现处于中等偏上水平，已经具备一定的高阶思维习惯，但在复杂任务或缺少 AI 支持时，部分能力可能还不够稳定。"
    elif score >= 4.0:
        base = "你的高阶思维能力正在发展中。你已经表现出部分有效做法，但还需要把零散习惯转化为更稳定的学习策略。"
    else:
        base = "当前自评显示，你在 AI 辅助学习中的高阶思维策略使用还比较有限。建议先从最薄弱的 1—2 个维度开始进行可执行的小训练。"

    if spread < 1.2:
        structure = "七个维度之间差距较小，能力结构相对均衡。"
    elif spread < 2.5:
        structure = "不同维度之间存在一定差异，说明你已经形成部分优势，但能力结构仍有优化空间。"
    else:
        structure = "不同维度之间差异较明显，呈现“优势突出、短板也较明显”的结构，优先补齐弱项会比平均用力更有效。"

    return base + structure


def build_scores():
    dim_raw = {d: [] for d in DIMENSIONS}
    item_results = []

    for idx, q in enumerate(QUESTIONS):
        value = st.session_state.get(f"q_{idx}")
        if value is None:
            continue
        dim_raw[q["dimension"]].append(value)
        item_results.append(
            {
                "index": idx,
                "dimension": q["dimension"],
                "text": q["text"],
                "likert": value,
                "score10": to_ten_point(value),
            }
        )

    dim_scores = {
        d: to_ten_point(mean(dim_raw[d]))
        for d in DIMENSIONS
    }

    # 7 个维度等权，避免 4 题维度比 3 题维度天然权重更大
    overall = round(mean(list(dim_scores.values())), 2)
    return overall, dim_scores, item_results


def build_report_text(overall, dim_scores, item_results):
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = ranked[:2]
    priorities = ranked[-2:]
    lowest_items = sorted(item_results, key=lambda x: (x["likert"], x["index"]))[:3]

    lines = []
    lines.append("GenAI-HOTS 高阶思维能力自评报告")
    lines.append("=" * 34)
    lines.append(f"综合得分：{overall:.2f}/10")
    lines.append(f"综合等级：{score_level(overall)}")
    lines.append("")
    lines.append("一、七维度得分")
    for d in DIMENSIONS:
        lines.append(f"- {d}：{dim_scores[d]:.2f}/10（{dimension_status(dim_scores[d])}）")

    lines.append("")
    lines.append("二、当前优势")
    for d, s in strengths:
        lines.append(f"- {d}（{s:.2f}/10）：{DIMENSION_INFO[d]['meaning']}")

    lines.append("")
    lines.append("三、优先提升方向")
    for d, s in priorities:
        lines.append(f"- {d}（{s:.2f}/10）")
        for tip in DIMENSION_INFO[d]["tips"]:
            lines.append(f"  · {tip}")

    lines.append("")
    lines.append("四、最值得关注的具体行为")
    for x in lowest_items:
        lines.append(f"- [{x['dimension']}] {x['text']}（本题：{x['likert']}/5）")

    lines.append("")
    lines.append("五、说明")
    lines.append("本结果基于自评量表，反映的是你对自己在 AI 辅助学习情境中的行为与能力感知，不等同于标准化能力考试，也不用于医学、心理或教育诊断。")
    return "\n".join(lines)


# =========================================================
# 初始化 Session State
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "page" not in st.session_state:
    st.session_state.page = 0

if "question_order" not in st.session_state:
    # 每个访问会话随机打乱题目；答题时不显示维度名，降低“按维度刷高分”的倾向
    st.session_state.question_order = random.sample(
        range(len(QUESTIONS)), len(QUESTIONS)
    )


# =========================================================
# 首页
# =========================================================
if st.session_state.stage == "intro":
    st.markdown(
        """
        <div class="hero">
            <h1>🧠 GenAI-HOTS 高阶思维能力自评</h1>
            <p>
                这不是“答对几题”的知识测验，而是一份基于日常 AI 学习行为的自我评估。
                请根据你<strong>最近 4 周</strong>的真实情况作答，而不是选择你认为“更优秀”的选项。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("题目数量", "23 题")
    with c2:
        st.metric("预计用时", "4–6 分钟")
    with c3:
        st.metric("结果维度", "7 个")

    st.info(
        "作答采用 1–5 级评分：1=完全不符合，2=比较不符合，3=一般，"
        "4=比较符合，5=完全符合。题目没有标准答案。"
    )

    st.markdown("#### 测评后你将得到")
    st.markdown(
        """
        - **0–10 分综合得分**，保留两位小数；
        - **7 个能力维度画像**与雷达图；
        - 你的**优势维度**与**优先提升维度**；
        - 精确到具体题项的**短板提示**；
        - 针对薄弱维度的**可执行训练建议**；
        - 可下载的个人文字版测评报告。
        """
    )

    consent = st.checkbox("我会尽量根据真实情况作答，不刻意追求高分。")
    if st.button("开始测评", type="primary", use_container_width=True, disabled=not consent):
        st.session_state.stage = "survey"
        st.session_state.page = 0
        st.rerun()


# =========================================================
# 答题页
# =========================================================
elif st.session_state.stage == "survey":
    QUESTIONS_PER_PAGE = 5
    total_pages = math.ceil(len(QUESTIONS) / QUESTIONS_PER_PAGE)
    page = st.session_state.page

    start = page * QUESTIONS_PER_PAGE
    end = min(start + QUESTIONS_PER_PAGE, len(QUESTIONS))
    current_indices = st.session_state.question_order[start:end]

    answered_count = sum(
        st.session_state.get(f"q_{idx}") is not None
        for idx in range(len(QUESTIONS))
    )

    st.title("🧠 高阶思维能力自评")
    st.progress(answered_count / len(QUESTIONS))
    st.caption(
        f"第 {page + 1}/{total_pages} 页 · 已回答 {answered_count}/{len(QUESTIONS)} 题"
    )

    st.info("请依据最近 4 周真实行为作答。答题过程中不显示所属能力维度。")

    LABELS = {
        1: "1 · 完全不符合",
        2: "2 · 比较不符合",
        3: "3 · 一般",
        4: "4 · 比较符合",
        5: "5 · 完全符合",
    }

    for position, idx in enumerate(current_indices, start=start + 1):
        q = QUESTIONS[idx]
        st.markdown(f"### {position}. {q['text']}")
        st.radio(
            label="请选择最符合你的情况：",
            options=[1, 2, 3, 4, 5],
            index=None,
            format_func=lambda x: LABELS[x],
            key=f"q_{idx}",
            horizontal=True,
            label_visibility="collapsed",
        )
        st.divider()

    left, mid, right = st.columns([1, 1, 2])

    with left:
        if page > 0:
            if st.button("← 上一页", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    page_complete = all(
        st.session_state.get(f"q_{idx}") is not None
        for idx in current_indices
    )

    with right:
        if page < total_pages - 1:
            if st.button(
                "下一页 →",
                type="primary",
                use_container_width=True,
                disabled=not page_complete,
            ):
                st.session_state.page += 1
                st.rerun()
        else:
            all_complete = all(
                st.session_state.get(f"q_{idx}") is not None
                for idx in range(len(QUESTIONS))
            )
            if st.button(
                "生成我的测评报告",
                type="primary",
                use_container_width=True,
                disabled=not all_complete,
            ):
                st.session_state.stage = "result"
                st.rerun()

    if not page_complete:
        st.warning("本页题目全部完成后才能进入下一页。")


# =========================================================
# 结果页
# =========================================================
elif st.session_state.stage == "result":
    overall, dim_scores, item_results = build_scores()
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strongest = ranked[0]
    weakest = ranked[-1]
    spread = strongest[1] - weakest[1]

    st.markdown(
        """
        <div class="hero">
            <h1>📊 你的高阶思维能力自评报告</h1>
            <p>
                以下结果不是“正确题数量”，而是根据 23 个行为陈述形成的七维度画像。
                综合分与各维度均转换为 0–10 分，并保留两位小数。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1.15, 1, 1])
    with c1:
        st.markdown(
            f"""
            <div class="score-box">
                <div class="muted">综合得分</div>
                <div class="score-number">{overall:.2f}</div>
                <div>/ 10</div>
                <p><strong>{score_level(overall)}</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.metric("当前最强维度", strongest[0], f"{strongest[1]:.2f}/10")
        st.caption(DIMENSION_INFO[strongest[0]]["meaning"])

    with c3:
        st.metric("优先提升维度", weakest[0], f"{weakest[1]:.2f}/10")
        st.caption(DIMENSION_INFO[weakest[0]]["meaning"])

    st.markdown("## 1. 综合画像")
    st.write(overall_interpretation(overall, spread))
    st.caption(
        "注意：这是自评结果，表示你对自身行为的感知，不代表与全体大学生相比的百分位排名。"
    )

    # 雷达图
    st.markdown("## 2. 七维度能力雷达图")
    labels = DIMENSIONS + [DIMENSIONS[0]]
    values = [dim_scores[d] for d in DIMENSIONS] + [dim_scores[DIMENSIONS[0]]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            name="你的得分",
            hovertemplate="%{theta}<br>%{r:.2f}/10<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickvals=[0, 2, 4, 6, 8, 10],
            )
        ),
        showlegend=False,
        margin=dict(l=45, r=45, t=30, b=30),
        height=520,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 维度详解
    st.markdown("## 3. 各维度详细解释")
    for d, s in ranked:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="dimension-card">
                <strong>{escape(d)}</strong>
                <span class="small-tag">{s:.2f}/10</span>
                <span class="small-tag">{dimension_status(s)}</span>
                <p style="margin-top:.65rem">{escape(info['meaning'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(max(s / 10, 0.0), 1.0))

        if s >= 8.5:
            st.write(
                "这一维度已经是你的明显优势。下一步重点不是继续“刷高分”，"
                "而是把这种能力迁移到更复杂、更陌生的课程或项目任务中。"
            )
        elif s >= 7.0:
            st.write(
                "你在这一维度已经形成较稳定的有效习惯，但在高难度任务、时间压力"
                "或 AI 输出质量较差时，仍需要保持同样的策略。"
            )
        elif s >= 5.5:
            st.write(
                "你已经具备这一能力的基本意识，但使用可能不够稳定。建议把它从"
                "“偶尔会做”变成有固定步骤的学习习惯。"
            )
        elif s >= 4.0:
            st.write(
                "这一维度存在较明显提升空间。优先选择一个具体行为连续练习 1–2 周，"
                "比一次尝试很多方法更有效。"
            )
        else:
            st.write(
                "这一维度目前是你的重点发展区。建议从最简单、最可执行的步骤开始，"
                "并减少把 AI 当作“直接答案提供者”的使用方式。"
            )

    # 优势
    st.markdown("## 4. 你的主要优势")
    for i, (d, s) in enumerate(ranked[:2], start=1):
        st.success(
            f"**优势 {i}：{d}（{s:.2f}/10）**  \n"
            f"{DIMENSION_INFO[d]['meaning']}"
        )

    # 短板 + 行动建议
    st.markdown("## 5. 最需要优先提升的方向")
    for i, (d, s) in enumerate(ranked[-2:][::-1], start=1):
        st.warning(f"**优先级 {i}：{d}（{s:.2f}/10）**")
        st.write(DIMENSION_INFO[d]["meaning"])
        st.markdown("**建议从下面 3 个动作开始：**")
        for tip in DIMENSION_INFO[d]["tips"]:
            st.markdown(f"- {tip}")

    # 题项级短板
    st.markdown("## 6. 精确到具体行为的短板")
    lowest_items = sorted(
        item_results,
        key=lambda x: (x["likert"], dim_scores[x["dimension"]], x["index"])
    )[:5]

    for i, x in enumerate(lowest_items, start=1):
        st.markdown(
            f"**{i}. {x['text']}**  \n"
            f"所属维度：{x['dimension']} ｜ 你的选择：{x['likert']}/5"
        )
        if x["likert"] <= 2:
            st.caption("这是当前非常值得优先练习的具体行为。")
        elif x["likert"] == 3:
            st.caption("你已经有一定基础，但还没有形成稳定习惯。")
        else:
            st.caption("这一项并不弱，只是在你的个人画像中相对更值得继续加强。")

    # 7天训练计划
    st.markdown("## 7. 给你的 7 天微型提升计划")
    priority_dims = [d for d, _ in ranked[-2:]]
    d1, d2 = priority_dims[0], priority_dims[1]

    st.markdown(
        f"""
**第 1–2 天：聚焦「{d1}」**  
从该维度建议中任选 1 个动作，在一次真实作业/学习任务中执行，并记录执行前后的差异。

**第 3–4 天：聚焦「{d2}」**  
不要追求复杂方法，只固定练习 1 个行为，例如交叉验证、拆解任务、复述自测或调整提示词。

**第 5 天：无 AI 独立检查**  
选择一个已经借助 AI 学过的内容，暂时关闭 AI，用自己的语言复述、解题或重建框架，检查自己是否真正掌握。

**第 6 天：人机协同复盘**  
回看一次 AI 辅助任务，分别写出：AI 做得好的地方、AI 可能误导的地方、最终由自己判断的地方。

**第 7 天：重新测评**  
再次完成本量表，重点看薄弱维度是否发生变化。单次分数变化只作参考，更重要的是具体行为是否更稳定。
        """
    )

    # 评分说明
    with st.expander("查看评分方法与结果解释规则"):
        st.markdown(
            """
**1. 原始作答：** 每题 1–5 分，1=完全不符合，5=完全符合。  

**2. 维度得分：** 先计算该维度题目的平均分，再线性换算到 0–10 分：  

`10分制得分 = (该维度平均分 - 1) ÷ 4 × 10`

因此：
- 1 分 → 0 分
- 2 分 → 2.5 分
- 3 分 → 5 分
- 4 分 → 7.5 分
- 5 分 → 10 分

**3. 综合得分：** 7 个维度等权平均。  
这样不会因为“批判性思维、创造性思维各有 4 题，而其他维度多为 3 题”而产生题目数量造成的额外权重。

**4. 等级标签：**
- 9.00–10.00：卓越
- 8.00–8.99：优秀
- 7.00–7.99：良好
- 6.00–6.99：中上
- 5.00–5.99：中等
- 4.00–4.99：发展中
- 0–3.99：优先提升

这些等级用于本网页的反馈呈现，不是全国常模或临床/教育诊断标准。
            """
        )

    # 下载报告
    report_text = build_report_text(overall, dim_scores, item_results)
    st.download_button(
        "📥 下载个人测评报告（TXT）",
        data=report_text.encode("utf-8-sig"),
        file_name="GenAI-HOTS_高阶思维能力自评报告.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()
    st.caption(
        "本测评反映的是 AI 辅助学习情境下的高阶思维能力自我感知。"
        "若用于正式研究，应进一步进行信度、效度检验，并依据正式样本建立解释标准。"
    )

    if st.button("重新测评", use_container_width=True):
        keys_to_delete = [
            k for k in list(st.session_state.keys())
            if k.startswith("q_")
        ]
        for k in keys_to_delete:
            del st.session_state[k]
        st.session_state.stage = "intro"
        st.session_state.page = 0
        st.session_state.question_order = random.sample(
            range(len(QUESTIONS)), len(QUESTIONS)
        )
        st.rerun()
