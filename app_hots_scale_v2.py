import random
import math
import time
from collections import Counter
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
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 高阶思维量表
# 基于原问卷第四部分的 7 个维度、23 个题项改写
# 为减少机械作答，采用“正向题—反向题—正向题—反向题……”交替呈现
# 反向题在后台自动反向计分，答题者看不到题目方向
# =========================================================
QUESTIONS = [
    # 1 正向
    {
        "dimension": "批判性思维能力",
        "text": "在面对生成式 AI 提供的信息时，我会有意识地判断其准确性和可靠性。",
        "reverse": False,
    },
    # 2 反向
    {
        "dimension": "创造性思维能力",
        "text": "使用 AI 时，我常常会被它给出的现成思路限制，很难再从新的角度产生自己的想法。",
        "reverse": True,
    },
    # 3 正向
    {
        "dimension": "问题解决能力",
        "text": "遇到复杂学习任务时，我会先利用 AI 拆解问题，再把大目标分成可执行的小步骤。",
        "reverse": False,
    },
    # 4 反向
    {
        "dimension": "自我调节学习能力",
        "text": "使用 AI 前，我通常不会事先设定清晰的学习目标、时间安排或使用边界。",
        "reverse": True,
    },
    # 5 正向
    {
        "dimension": "人机协同能力",
        "text": "使用各类数字工具（含 AI）时，我会针对自己的需求设计合适的提问或操作方式。",
        "reverse": False,
    },
    # 6 反向
    {
        "dimension": "元认知能力",
        "text": "看到 AI 给出的解释或答案后，我有时会直接觉得自己已经懂了，而不会再检查自己是否真正理解。",
        "reverse": True,
    },
    # 7 正向
    {
        "dimension": "计算思维能力",
        "text": "在分析问题时，我会先用 AI 帮我提取关键变量及其关系，再构建解决框架。",
        "reverse": False,
    },
    # 8 反向
    {
        "dimension": "批判性思维能力",
        "text": "当 AI 的回答看起来比较合理时，我通常会直接接受，而不会再与其他来源进行核对。",
        "reverse": True,
    },
    # 9 正向
    {
        "dimension": "创造性思维能力",
        "text": "我经常将 AI 生成的不同元素进行组合、重构，以创造出新的内容。",
        "reverse": False,
    },
    # 10 反向
    {
        "dimension": "问题解决能力",
        "text": "当原有方法无效时，我往往会依赖 AI 给出的第一个方案，而不会主动比较其他解题策略。",
        "reverse": True,
    },
    # 11 正向
    {
        "dimension": "自我调节学习能力",
        "text": "发现 AI 反馈效率不高时，我会主动调整提示词或更换学习策略。",
        "reverse": False,
    },
    # 12 反向
    {
        "dimension": "人机协同能力",
        "text": "当 AI 的结果不理想时，我通常会直接接受或放弃，而很少继续补充信息、调整提示或切换工具。",
        "reverse": True,
    },
    # 13 正向
    {
        "dimension": "元认知能力",
        "text": "我大致清楚自己在哪些知识或能力上比较薄弱，并会利用 AI 进行针对性训练。",
        "reverse": False,
    },
    # 14 反向
    {
        "dimension": "计算思维能力",
        "text": "面对多步骤任务时，我更倾向于让 AI 直接给出最终结果，而很少自己梳理清楚操作流程和逻辑关系。",
        "reverse": True,
    },
    # 15 正向
    {
        "dimension": "批判性思维能力",
        "text": "我能识别出 AI 生成内容中逻辑不清晰或证据不足的部分。",
        "reverse": False,
    },
    # 16 反向
    {
        "dimension": "创造性思维能力",
        "text": "对于 AI 给出的内容，我通常只是做少量修改，很少进一步重组并形成真正属于自己的新表达或新方案。",
        "reverse": True,
    },
    # 17 正向
    {
        "dimension": "问题解决能力",
        "text": "面对真实情境问题（课程设计、项目实践等），我能综合 AI 建议与多方信息，拟定可行方案。",
        "reverse": False,
    },
    # 18 反向
    {
        "dimension": "自我调节学习能力",
        "text": "完成 AI 辅助学习任务后，我很少回顾 AI 输出与实际效果之间的差距，也很少据此调整下一步学习方法。",
        "reverse": True,
    },
    # 19 正向
    {
        "dimension": "人机协同能力",
        "text": "我善于把 AI 给出的建议与自己的想法结合，形成更完善的解决方案或作品。",
        "reverse": False,
    },
    # 20 反向
    {
        "dimension": "元认知能力",
        "text": "完成一项 AI 辅助任务后，我通常不会专门反思哪些地方真正有效、哪些地方只是表面上完成了任务。",
        "reverse": True,
    },
    # 21 正向
    {
        "dimension": "计算思维能力",
        "text": "遇到重复性学习任务时，我会利用 AI 生成脚本、公式或宏命令，实现自动化处理。",
        "reverse": False,
    },
    # 22 反向
    {
        "dimension": "批判性思维能力",
        "text": "即使 AI 已经给出了一个现成答案，我通常也不会再独立追问问题的本质或重新思考其推理过程。",
        "reverse": True,
    },
    # 23 正向
    {
        "dimension": "创造性思维能力",
        "text": "AI 提供的灵感能够帮助我打破思维定势，从新的角度思考问题。",
        "reverse": False,
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
# 工具函数
# =========================================================
def mean(values):
    return sum(values) / len(values) if values else 0.0


def to_ten_point(likert_mean):
    return round((likert_mean - 1) / 4 * 10, 2)


def score_level(score):
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


def make_alternating_order():
    """
    正向题与反向题分别随机打乱，再严格交替：
    正 -> 反 -> 正 -> 反 ...
    这样既保持一正一负，又避免每次题目内容完全相同。
    """
    positive = [i for i, q in enumerate(QUESTIONS) if not q["reverse"]]
    negative = [i for i, q in enumerate(QUESTIONS) if q["reverse"]]
    random.shuffle(positive)
    random.shuffle(negative)

    order = []
    for i in range(max(len(positive), len(negative))):
        if i < len(positive):
            order.append(positive[i])
        if i < len(negative):
            order.append(negative[i])
    return order


def save_answer(idx):
    """
    关键修复：
    Streamlit 在翻页后会销毁上一页没有继续渲染的 widget key。
    因此答案不能只存在 radio 自己的 key 中，而要立即复制到一个独立的
    st.session_state.answers 字典里。
    """
    widget_key = f"_widget_q_{idx}"
    if widget_key in st.session_state:
        st.session_state.answers[idx] = st.session_state[widget_key]


def build_scores():
    dim_raw = {d: [] for d in DIMENSIONS}
    item_results = []

    for idx, q in enumerate(QUESTIONS):
        raw_value = st.session_state.answers.get(idx)
        if raw_value is None:
            continue

        # 反向题：1↔5，2↔4，3不变
        scored_value = 6 - raw_value if q["reverse"] else raw_value

        dim_raw[q["dimension"]].append(scored_value)
        item_results.append(
            {
                "index": idx,
                "dimension": q["dimension"],
                "text": q["text"],
                "raw_likert": raw_value,
                "scored_likert": scored_value,
                "reverse": q["reverse"],
                "score10": to_ten_point(scored_value),
            }
        )

    dim_scores = {
        d: to_ten_point(mean(dim_raw[d]))
        for d in DIMENSIONS
    }

    # 7 个维度等权
    overall = round(mean(list(dim_scores.values())), 2)
    return overall, dim_scores, item_results


def response_quality():
    answers = list(st.session_state.answers.values())
    if not answers:
        return []

    warnings = []

    counts = Counter(answers)
    most_common_ratio = max(counts.values()) / len(answers)

    if len(answers) >= 15 and most_common_ratio >= 0.80:
        warnings.append(
            "你的作答中有超过 80% 选择了同一个选项，可能存在较明显的机械作答倾向。"
        )

    if "survey_start_time" in st.session_state and len(answers) == len(QUESTIONS):
        elapsed = time.time() - st.session_state.survey_start_time
        if elapsed < 60:
            warnings.append(
                "本次 23 题完成时间不足 1 分钟，作答速度较快，结果建议谨慎参考。"
            )

    return warnings


def build_report_text(overall, dim_scores, item_results):
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = ranked[:2]
    priorities = ranked[-2:]
    lowest_items = sorted(
        item_results,
        key=lambda x: (x["scored_likert"], x["index"])
    )[:3]

    lines = []
    lines.append("GenAI-HOTS 高阶思维能力自评报告")
    lines.append("=" * 34)
    lines.append(f"综合得分：{overall:.2f}/10")
    lines.append(f"综合等级：{score_level(overall)}")
    lines.append("")
    lines.append("一、七维度得分")
    for d in DIMENSIONS:
        lines.append(
            f"- {d}：{dim_scores[d]:.2f}/10（{dimension_status(dim_scores[d])}）"
        )

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
        lines.append(
            f"- [{x['dimension']}] {x['text']}（能力方向换算：{x['scored_likert']}/5）"
        )

    lines.append("")
    lines.append("五、评分说明")
    lines.append("正向题按原分计分；反向题采用 6-原始分进行反向计分。")
    lines.append("各维度先求平均分，再换算为 0—10 分；综合分为 7 个维度等权平均。")
    lines.append("")
    lines.append("六、说明")
    lines.append(
        "本结果基于自评量表，反映的是你对自己在 AI 辅助学习情境中的行为与能力感知，"
        "不等同于标准化能力考试，也不用于医学、心理或教育诊断。"
    )
    return "\n".join(lines)


# =========================================================
# 初始化 Session State
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "page" not in st.session_state:
    st.session_state.page = 0

# 独立、持久的答案容器 —— 翻页后不会被 widget 清理
if "answers" not in st.session_state:
    st.session_state.answers = {}

if "question_order" not in st.session_state:
    st.session_state.question_order = make_alternating_order()


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
        "4=比较符合，5=完全符合。题目没有标准答案，请逐题阅读。"
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

    consent = st.checkbox("我会逐题阅读，并根据真实情况作答。")
    if st.button(
        "开始测评",
        type="primary",
        use_container_width=True,
        disabled=not consent,
    ):
        st.session_state.stage = "survey"
        st.session_state.page = 0
        st.session_state.answers = {}
        st.session_state.question_order = make_alternating_order()
        st.session_state.survey_start_time = time.time()

        # 清掉可能残留的 widget 临时状态
        for key in list(st.session_state.keys()):
            if key.startswith("_widget_q_"):
                del st.session_state[key]

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

    answered_count = len(st.session_state.answers)

    st.title("🧠 高阶思维能力自评")
    st.progress(answered_count / len(QUESTIONS))
    st.caption(
        f"第 {page + 1}/{total_pages} 页 · 已回答 {answered_count}/{len(QUESTIONS)} 题"
    )

    st.info(
        "请依据最近 4 周的真实行为作答。题目中既有正向表述，也有反向表述，"
        "请不要按固定规律选择。"
    )

    LABELS = {
        1: "1 · 完全不符合",
        2: "2 · 比较不符合",
        3: "3 · 一般",
        4: "4 · 比较符合",
        5: "5 · 完全符合",
    }

    for position, idx in enumerate(current_indices, start=start + 1):
        q = QUESTIONS[idx]
        widget_key = f"_widget_q_{idx}"

        # 如果之前已经答过（例如返回上一页），恢复到原选项
        if idx in st.session_state.answers and widget_key not in st.session_state:
            st.session_state[widget_key] = st.session_state.answers[idx]

        st.markdown(f"### {position}. {q['text']}")
        st.radio(
            label="请选择最符合你的情况：",
            options=[1, 2, 3, 4, 5],
            index=None,
            format_func=lambda x: LABELS[x],
            key=widget_key,
            on_change=save_answer,
            args=(idx,),
            horizontal=True,
            label_visibility="collapsed",
        )
        st.divider()

    left, mid, right = st.columns([1, 1, 2])

    page_complete = all(
        idx in st.session_state.answers
        for idx in current_indices
    )

    with left:
        if page > 0:
            if st.button("← 上一页", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

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
            all_complete = len(st.session_state.answers) == len(QUESTIONS)
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
                以下结果根据 23 个行为陈述形成七维度画像。
                正向题按原分计分，反向题已在后台自动反向计分。
                综合分与各维度均转换为 0–10 分，并保留两位小数。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quality_warnings = response_quality()
    for warning in quality_warnings:
        st.warning("作答质量提示：" + warning)

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

    st.markdown("## 4. 你的主要优势")
    for i, (d, s) in enumerate(ranked[:2], start=1):
        st.success(
            f"**优势 {i}：{d}（{s:.2f}/10）**  \n"
            f"{DIMENSION_INFO[d]['meaning']}"
        )

    st.markdown("## 5. 最需要优先提升的方向")
    for i, (d, s) in enumerate(ranked[-2:][::-1], start=1):
        st.warning(f"**优先级 {i}：{d}（{s:.2f}/10）**")
        st.write(DIMENSION_INFO[d]["meaning"])
        st.markdown("**建议从下面 3 个动作开始：**")
        for tip in DIMENSION_INFO[d]["tips"]:
            st.markdown(f"- {tip}")

    st.markdown("## 6. 精确到具体行为的短板")
    lowest_items = sorted(
        item_results,
        key=lambda x: (
            x["scored_likert"],
            dim_scores[x["dimension"]],
            x["index"],
        )
    )[:5]

    for i, x in enumerate(lowest_items, start=1):
        st.markdown(
            f"**{i}. {x['text']}**  \n"
            f"所属维度：{x['dimension']} ｜ 能力方向换算：{x['scored_likert']}/5"
        )
        if x["scored_likert"] <= 2:
            st.caption("这是当前非常值得优先练习的具体行为。")
        elif x["scored_likert"] == 3:
            st.caption("你已经有一定基础，但还没有形成稳定习惯。")
        else:
            st.caption("这一项并不弱，只是在你的个人画像中相对更值得继续加强。")

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

    with st.expander("查看评分方法与结果解释规则"):
        st.markdown(
            """
**1. 原始作答：** 每题 1–5 分，1=完全不符合，5=完全符合。  

**2. 正向题：** 直接按 1–5 分计分。  

**3. 反向题：** 后台采用 `6 - 原始分` 自动反向计分：
- 原选 1 → 计 5
- 原选 2 → 计 4
- 原选 3 → 计 3
- 原选 4 → 计 2
- 原选 5 → 计 1

**4. 维度得分：** 先计算该维度反向处理后的平均分，再线性换算到 0–10 分：  

`10分制得分 = (该维度平均分 - 1) ÷ 4 × 10`

因此，处理后的：
- 1 分 → 0 分
- 2 分 → 2.5 分
- 3 分 → 5 分
- 4 分 → 7.5 分
- 5 分 → 10 分

**5. 综合得分：** 7 个维度等权平均。  

**6. 等级标签：**
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
        for key in list(st.session_state.keys()):
            if key.startswith("_widget_q_"):
                del st.session_state[key]

        st.session_state.stage = "intro"
        st.session_state.page = 0
        st.session_state.answers = {}
        st.session_state.question_order = make_alternating_order()
        st.session_state.pop("survey_start_time", None)
        st.rerun()
