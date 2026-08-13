import random
import math
import time
from collections import Counter
from html import escape

import streamlit as st
import plotly.graph_objects as go


# =========================================================
# App
# =========================================================
APP_TITLE = "思维罗盘｜生成式 AI 高阶思维能力测评"
APP_SUBTITLE = "看见你的思维优势，找到下一步成长方向"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    :root {
        --ink: #192033;
        --sub: #687086;
        --purple: #6C63FF;
        --purple2: #8D7CFF;
        --blue: #4C8DFF;
        --cyan: #4BC8D9;
        --bg: #F7F8FC;
        --card: rgba(255,255,255,.92);
        --line: rgba(31,39,66,.10);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(108,99,255,.10), transparent 26rem),
            radial-gradient(circle at 95% 5%, rgba(76,141,255,.09), transparent 25rem),
            linear-gradient(180deg, #FBFCFF 0%, #F7F8FC 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2.2rem;
        padding-bottom: 3.5rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* ---------- Hero ---------- */
    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .38rem .72rem;
        border-radius: 999px;
        background: rgba(108,99,255,.10);
        border: 1px solid rgba(108,99,255,.14);
        color: #5C54DE;
        font-weight: 700;
        font-size: .88rem;
        margin-bottom: 1rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.4rem 2.55rem;
        border-radius: 28px;
        background:
            linear-gradient(135deg, rgba(255,255,255,.98), rgba(248,249,255,.94));
        border: 1px solid rgba(108,99,255,.12);
        box-shadow: 0 18px 55px rgba(39,48,87,.08);
        margin-bottom: 1.25rem;
    }

    .hero::after {
        content: "✦";
        position: absolute;
        right: 2.2rem;
        top: 1.2rem;
        font-size: 7rem;
        color: rgba(108,99,255,.08);
        transform: rotate(12deg);
    }

    .hero-title {
        font-size: clamp(2.15rem, 4vw, 3.8rem);
        line-height: 1.07;
        margin: 0 0 .9rem 0;
        font-weight: 850;
        color: #171D31;
    }

    .hero-gradient {
        background: linear-gradient(90deg, #6C63FF, #4C8DFF, #4BC8D9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.85;
        color: #687086;
        max-width: 760px;
        margin-bottom: 0;
    }

    /* ---------- Small feature cards ---------- */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .85rem;
        margin: 1.15rem 0 1.3rem;
    }

    .feature-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(38,46,80,.04);
    }

    .feature-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(108,99,255,.15), rgba(76,141,255,.10));
        font-size: 1.2rem;
        margin-bottom: .65rem;
    }

    .feature-value {
        font-size: 1.23rem;
        font-weight: 800;
        color: #1D2439;
        margin-bottom: .08rem;
    }

    .feature-label {
        color: #7A8195;
        font-size: .91rem;
    }

    /* ---------- Intro / tips ---------- */
    .soft-panel {
        background: rgba(255,255,255,.82);
        border: 1px solid rgba(31,39,66,.08);
        border-radius: 18px;
        padding: 1.05rem 1.15rem;
        margin: .85rem 0 1.1rem;
    }

    .soft-panel strong {
        color: #3F47A7;
    }

    /* ---------- Survey ---------- */
    .survey-top {
        background: rgba(255,255,255,.88);
        border: 1px solid rgba(31,39,66,.08);
        border-radius: 20px;
        padding: 1.15rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 26px rgba(38,46,80,.04);
    }

    .survey-title {
        font-size: 1.65rem;
        font-weight: 820;
        margin-bottom: .18rem;
    }

    .survey-meta {
        color: #7A8195;
        font-size: .93rem;
    }

    .q-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 20px;
        padding: 1.2rem 1.3rem .7rem 1.3rem;
        margin: .85rem 0;
        box-shadow: 0 7px 20px rgba(38,46,80,.035);
    }

    .q-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 34px;
        height: 34px;
        padding: 0 .55rem;
        border-radius: 11px;
        background: linear-gradient(135deg, #7168FF, #5B8EFF);
        color: white;
        font-weight: 800;
        font-size: .88rem;
        margin-right: .55rem;
    }

    .q-text {
        display: inline;
        font-size: 1.04rem;
        line-height: 1.78;
        font-weight: 650;
        color: #222A3F;
    }

    div[role="radiogroup"] {
        gap: .2rem;
    }

    div[data-testid="stRadio"] label {
        padding: .28rem .15rem;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        border-radius: 14px !important;
        min-height: 2.9rem;
        font-weight: 750 !important;
        border: 1px solid rgba(108,99,255,.16) !important;
        transition: .18s ease !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6C63FF, #5C8DFF) !important;
        color: white !important;
        border: 0 !important;
        box-shadow: 0 9px 24px rgba(108,99,255,.22) !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
    }

    /* ---------- Results ---------- */
    .result-hero {
        padding: 1.85rem 2rem;
        border-radius: 25px;
        background: linear-gradient(135deg, #222946, #343D70 60%, #535CC3);
        color: white;
        box-shadow: 0 18px 50px rgba(30,36,74,.18);
        margin-bottom: 1.15rem;
    }

    .result-hero .eyebrow {
        opacity: .76;
        font-size: .88rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: .45rem;
    }

    .result-hero .title {
        font-size: 2rem;
        font-weight: 850;
        margin-bottom: .25rem;
    }

    .result-hero .desc {
        opacity: .82;
        line-height: 1.7;
    }

    .score-box {
        background: rgba(255,255,255,.95);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 22px;
        text-align: center;
        padding: 1.35rem 1.1rem;
        min-height: 178px;
        box-shadow: 0 10px 32px rgba(38,46,80,.055);
    }

    .score-label {
        color: #7A8195;
        font-size: .9rem;
    }

    .score-number {
        font-size: 3.15rem;
        font-weight: 900;
        line-height: 1.06;
        margin: .3rem 0 .2rem;
        background: linear-gradient(90deg, #6C63FF, #4C8DFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .score-level {
        display: inline-flex;
        padding: .28rem .7rem;
        border-radius: 999px;
        background: rgba(108,99,255,.10);
        color: #5B54D7;
        font-size: .87rem;
        font-weight: 780;
    }

    .mini-result {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 22px;
        padding: 1.25rem 1.3rem;
        min-height: 178px;
        box-shadow: 0 10px 32px rgba(38,46,80,.055);
    }

    .mini-icon {
        font-size: 1.35rem;
        margin-bottom: .42rem;
    }

    .mini-label {
        color: #7A8195;
        font-size: .88rem;
    }

    .mini-title {
        font-size: 1.13rem;
        font-weight: 820;
        margin: .2rem 0;
        color: #20273C;
    }

    .mini-score {
        color: #5E67C8;
        font-weight: 800;
        font-size: .93rem;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: .55rem;
        margin: 1.75rem 0 .72rem;
        font-size: 1.35rem;
        font-weight: 850;
        color: #1F263A;
    }

    .section-icon {
        width: 34px;
        height: 34px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background: rgba(108,99,255,.10);
    }

    .dimension-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: .7rem;
        box-shadow: 0 7px 22px rgba(38,46,80,.035);
    }

    .dim-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: .35rem;
    }

    .dim-name {
        display: flex;
        align-items: center;
        gap: .55rem;
        font-weight: 820;
        color: #20273C;
    }

    .dim-score {
        font-weight: 850;
        color: #5E67C8;
        white-space: nowrap;
    }

    .dim-desc {
        color: #6E758A;
        line-height: 1.7;
        font-size: .94rem;
    }

    .advice-card {
        background: linear-gradient(135deg, rgba(108,99,255,.07), rgba(76,141,255,.055));
        border: 1px solid rgba(108,99,255,.12);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: .65rem 0;
    }

    .behavior-card {
        background: rgba(255,255,255,.94);
        border-left: 4px solid #7A73FF;
        border-radius: 14px;
        padding: .85rem 1rem;
        margin: .6rem 0;
        box-shadow: 0 6px 18px rgba(38,46,80,.03);
    }

    .muted {
        color: #7A8195;
        font-size: .9rem;
    }

    @media (max-width: 780px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .hero {
            padding: 1.55rem 1.25rem;
        }
        .hero::after {
            display: none;
        }
        .block-container {
            padding-top: 1.2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


QUESTIONS = [
    {"dimension": "批判性思维能力", "text": "在面对生成式 AI 提供的信息时，我会有意识地判断其准确性和可靠性。", "reverse": False},
    {"dimension": "创造性思维能力", "text": "使用 AI 时，我常常会被它给出的现成思路限制，很难再从新的角度产生自己的想法。", "reverse": True},
    {"dimension": "问题解决能力", "text": "遇到复杂学习任务时，我会先利用 AI 拆解问题，再把大目标分成可执行的小步骤。", "reverse": False},
    {"dimension": "自我调节学习能力", "text": "使用 AI 前，我通常不会事先设定清晰的学习目标、时间安排或使用边界。", "reverse": True},
    {"dimension": "人机协同能力", "text": "使用各类数字工具（含 AI）时，我会针对自己的需求设计合适的提问或操作方式。", "reverse": False},
    {"dimension": "元认知能力", "text": "看到 AI 给出的解释或答案后，我有时会直接觉得自己已经懂了，而不会再检查自己是否真正理解。", "reverse": True},
    {"dimension": "计算思维能力", "text": "在分析问题时，我会先用 AI 帮我提取关键变量及其关系，再构建解决框架。", "reverse": False},
    {"dimension": "批判性思维能力", "text": "当 AI 的回答看起来比较合理时，我通常会直接接受，而不会再与其他来源进行核对。", "reverse": True},
    {"dimension": "创造性思维能力", "text": "我经常将 AI 生成的不同元素进行组合、重构，以创造出新的内容。", "reverse": False},
    {"dimension": "问题解决能力", "text": "当原有方法无效时，我往往会依赖 AI 给出的第一个方案，而不会主动比较其他解题策略。", "reverse": True},
    {"dimension": "自我调节学习能力", "text": "发现 AI 反馈效率不高时，我会主动调整提示词或更换学习策略。", "reverse": False},
    {"dimension": "人机协同能力", "text": "当 AI 的结果不理想时，我通常会直接接受或放弃，而很少继续补充信息、调整提示或切换工具。", "reverse": True},
    {"dimension": "元认知能力", "text": "我大致清楚自己在哪些知识或能力上比较薄弱，并会利用 AI 进行针对性训练。", "reverse": False},
    {"dimension": "计算思维能力", "text": "面对多步骤任务时，我更倾向于让 AI 直接给出最终结果，而很少自己梳理清楚操作流程和逻辑关系。", "reverse": True},
    {"dimension": "批判性思维能力", "text": "我能识别出 AI 生成内容中逻辑不清晰或证据不足的部分。", "reverse": False},
    {"dimension": "创造性思维能力", "text": "对于 AI 给出的内容，我通常只是做少量修改，很少进一步重组并形成真正属于自己的新表达或新方案。", "reverse": True},
    {"dimension": "问题解决能力", "text": "面对真实情境问题（课程设计、项目实践等），我能综合 AI 建议与多方信息，拟定可行方案。", "reverse": False},
    {"dimension": "自我调节学习能力", "text": "完成 AI 辅助学习任务后，我很少回顾 AI 输出与实际效果之间的差距，也很少据此调整下一步学习方法。", "reverse": True},
    {"dimension": "人机协同能力", "text": "我善于把 AI 给出的建议与自己的想法结合，形成更完善的解决方案或作品。", "reverse": False},
    {"dimension": "元认知能力", "text": "完成一项 AI 辅助任务后，我通常不会专门反思哪些地方真正有效、哪些地方只是表面上完成了任务。", "reverse": True},
    {"dimension": "计算思维能力", "text": "遇到重复性学习任务时，我会利用 AI 生成脚本、公式或宏命令，实现自动化处理。", "reverse": False},
    {"dimension": "批判性思维能力", "text": "即使 AI 已经给出了一个现成答案，我通常也不会再独立追问问题的本质或重新思考其推理过程。", "reverse": True},
    {"dimension": "创造性思维能力", "text": "AI 提供的灵感能够帮助我打破思维定势，从新的角度思考问题。", "reverse": False},
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
        "icon": "🔎",
        "short": "辨别、核验与独立判断",
        "meaning": "你是否会核验 AI 信息、识别逻辑与证据问题，并保持独立判断。",
        "tips": [
            "对重要结论至少找 1 个独立来源进行交叉验证。",
            "看到答案时追问：证据是什么？有没有反例？还有没有其他解释？",
            "让 AI 列出自身答案中可能存在的漏洞，再由你做最后判断。",
        ],
    },
    "创造性思维能力": {
        "icon": "✨",
        "short": "发散、重组与新想法",
        "meaning": "你能否借助 AI 打破思维定势、重组信息，并形成有自己特色的新想法。",
        "tips": [
            "同一问题尝试 3 种不同视角，再自行筛选与重组。",
            "不要停留在第一个答案，比较多个版本后再形成自己的方案。",
            "把两个原本不相关的概念、案例或方法重新连接，练习组合创新。",
        ],
    },
    "问题解决能力": {
        "icon": "🧩",
        "short": "拆解、比较与落地",
        "meaning": "你能否拆解复杂任务、比较多种路径，并把 AI 建议转化为可执行方案。",
        "tips": [
            "复杂任务先写清目标、约束、步骤和验证标准。",
            "遇到卡点时，让 AI 提供多种路径并比较各自利弊。",
            "方案完成后检查资源、时间、风险和替代方案。",
        ],
    },
    "自我调节学习能力": {
        "icon": "🎯",
        "short": "目标、监控与复盘",
        "meaning": "你是否能在使用 AI 前设定目标，在过程中调整策略，并在结束后复盘。",
        "tips": [
            "使用 AI 前先写下本次任务目标和必须自己完成的部分。",
            "给 AI 使用设置时间边界，避免一直停留在对话中。",
            "任务结束后记录：AI 帮助了什么、干扰了什么、下次怎么改。",
        ],
    },
    "人机协同能力": {
        "icon": "🤝",
        "short": "提问、调整与协作",
        "meaning": "你能否通过提问、补充信息和工具切换，让 AI 真正服务于自己的目标。",
        "tips": [
            "提问时明确任务目标、背景信息、限制条件和输出格式。",
            "第一次结果不理想时，指出具体问题并逐步补充上下文。",
            "让 AI 负责发散与整理，你负责判断、取舍和最终负责。",
        ],
    },
    "元认知能力": {
        "icon": "🪞",
        "short": "觉察、理解与自我检查",
        "meaning": "你是否清楚自己会什么、不会什么，并能检查“我是否真的理解”。",
        "tips": [
            "学完后关闭 AI，用自己的话复述核心内容。",
            "让 AI 出递进问题进行自测，但先由自己独立作答。",
            "建立知识薄弱清单，记录反复出错的概念和步骤。",
        ],
    },
    "计算思维能力": {
        "icon": "⚙️",
        "short": "变量、流程与自动化",
        "meaning": "你能否识别变量关系、设计流程，并把重复任务转化为规则或自动化步骤。",
        "tips": [
            "遇到复杂问题先梳理输入、处理步骤和输出。",
            "把多步骤任务写成流程或伪代码，再检查逻辑遗漏。",
            "对重复操作主动寻找可复用模板、公式、脚本或自动化方式。",
        ],
    },
}


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
    return "成长空间较大"


def dimension_status(score):
    if score >= 8.5:
        return "优势突出"
    if score >= 7.0:
        return "表现良好"
    if score >= 5.5:
        return "基础稳定"
    if score >= 4.0:
        return "仍有提升空间"
    return "建议优先加强"


def overall_interpretation(score, spread):
    if score >= 8.5:
        base = "你的整体表现处于较高水平，说明你在 AI 辅助学习中已经形成较成熟的判断、调节与协作习惯。"
    elif score >= 7.0:
        base = "你的整体表现较好，多数高阶思维环节已经能够主动使用，下一步可以继续提升稳定性与迁移能力。"
    elif score >= 5.5:
        base = "你的整体表现处于中等偏上水平，已经具备一定的高阶思维习惯，但部分能力在复杂任务中还不够稳定。"
    elif score >= 4.0:
        base = "你的高阶思维能力正在发展中。你已经表现出部分有效做法，下一步需要把零散习惯逐渐变成稳定策略。"
    else:
        base = "当前结果显示，你在 AI 辅助学习中的高阶思维策略使用相对有限，适合先从最需要加强的 1—2 个方向开始。"

    if spread < 1.2:
        structure = " 七个维度之间差距较小，整体结构比较均衡。"
    elif spread < 2.5:
        structure = " 不同维度之间存在一定差异，你已经形成部分优势，同时也有明确的提升方向。"
    else:
        structure = " 不同维度之间差异较明显，优先补强短板会比平均用力更有效。"

    return base + structure


def make_alternating_order():
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

        scored_value = 6 - raw_value if q["reverse"] else raw_value
        dim_raw[q["dimension"]].append(scored_value)

        item_results.append(
            {
                "index": idx,
                "dimension": q["dimension"],
                "text": q["text"],
                "raw_likert": raw_value,
                "scored_likert": scored_value,
            }
        )

    dim_scores = {d: to_ten_point(mean(dim_raw[d])) for d in DIMENSIONS}
    overall = round(mean(list(dim_scores.values())), 2)
    return overall, dim_scores, item_results


def response_quality():
    answers = list(st.session_state.answers.values())
    if not answers:
        return []

    notices = []
    counts = Counter(answers)
    most_common_ratio = max(counts.values()) / len(answers)

    if len(answers) >= 15 and most_common_ratio >= 0.80:
        notices.append("你的选择较为集中，建议结合真实学习经历再次确认部分题目。")

    if "survey_start_time" in st.session_state and len(answers) == len(QUESTIONS):
        elapsed = time.time() - st.session_state.survey_start_time
        if elapsed < 60:
            notices.append("本次完成速度较快，若有题目未仔细阅读，可以重新测评后再对比结果。")

    return notices


def build_report_text(overall, dim_scores, item_results):
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = ranked[:2]
    priorities = ranked[-2:]
    lowest_items = sorted(
        item_results,
        key=lambda x: (x["scored_likert"], x["index"])
    )[:3]

    lines = [
        f"{APP_TITLE}｜个人报告",
        "=" * 34,
        f"综合得分：{overall:.2f}/10",
        f"综合表现：{score_level(overall)}",
        "",
        "一、能力画像",
    ]

    for d in DIMENSIONS:
        lines.append(f"- {d}：{dim_scores[d]:.2f}/10")

    lines.extend(["", "二、优势方向"])
    for d, s in strengths:
        lines.append(f"- {d}（{s:.2f}/10）：{DIMENSION_INFO[d]['meaning']}")

    lines.extend(["", "三、优先提升方向"])
    for d, s in priorities:
        lines.append(f"- {d}（{s:.2f}/10）")
        for tip in DIMENSION_INFO[d]["tips"]:
            lines.append(f"  · {tip}")

    lines.extend(["", "四、值得关注的具体行为"])
    for x in lowest_items:
        lines.append(f"- [{x['dimension']}] {x['text']}")

    lines.extend(
        [
            "",
            "说明：",
            "本报告反映的是你在 AI 辅助学习情境中的自我感知与行为倾向，可用于自我了解和学习改进。",
        ]
    )

    return "\n".join(lines)


# =========================================================
# State
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "question_order" not in st.session_state:
    st.session_state.question_order = make_alternating_order()


# =========================================================
# Home
# =========================================================
if st.session_state.stage == "intro":
    st.markdown(
        f"""
        <div class="hero">
            <div class="brand-pill">✦ AI × HIGHER-ORDER THINKING</div>
            <div class="hero-title">
                思维罗盘<br>
                <span class="hero-gradient">高阶思维能力测评</span>
            </div>
            <p class="hero-subtitle">
                {APP_SUBTITLE}。通过一组与你日常 AI 学习行为有关的陈述，
                了解你在判断、创造、解决问题、自我调节与人机协作等方面的特点。
            </p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">◈</div>
                <div class="feature-value">23 题</div>
                <div class="feature-label">轻量完成，不增加额外负担</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">◷</div>
                <div class="feature-value">约 4–6 分钟</div>
                <div class="feature-label">依据最近一段时间的真实状态作答</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✦</div>
                <div class="feature-value">7 维画像</div>
                <div class="feature-label">结果不只是一项总分</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="soft-panel">
            <strong>作答方式</strong><br>
            请按照自己的真实情况选择。每题均为 1–5 级：
            1 表示“完全不符合”，5 表示“完全符合”。
            这里没有标准答案，也不需要追求某一种“理想选择”。
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 你将获得")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("🔷 **综合思维指数**：0–10 分的整体表现")
        st.markdown("🕸️ **七维能力雷达图**：一眼看清能力结构")
        st.markdown("🏅 **优势方向**：发现最值得保留的思维习惯")
    with c2:
        st.markdown("🧭 **提升方向**：找到最值得优先改善的能力")
        st.markdown("📝 **行为级反馈**：定位到具体学习习惯")
        st.markdown("🚀 **行动建议**：给出可以直接实践的方法")

    st.write("")
    consent = st.checkbox("我会根据真实情况认真作答。")

    if st.button(
        "开始我的测评  →",
        type="primary",
        use_container_width=True,
        disabled=not consent,
    ):
        st.session_state.stage = "survey"
        st.session_state.page = 0
        st.session_state.answers = {}
        st.session_state.question_order = make_alternating_order()
        st.session_state.survey_start_time = time.time()

        for key in list(st.session_state.keys()):
            if key.startswith("_widget_q_"):
                del st.session_state[key]

        st.rerun()


# =========================================================
# Survey
# =========================================================
elif st.session_state.stage == "survey":
    QUESTIONS_PER_PAGE = 5
    total_pages = math.ceil(len(QUESTIONS) / QUESTIONS_PER_PAGE)
    page = st.session_state.page

    start = page * QUESTIONS_PER_PAGE
    end = min(start + QUESTIONS_PER_PAGE, len(QUESTIONS))
    current_indices = st.session_state.question_order[start:end]
    answered_count = len(st.session_state.answers)

    st.markdown(
        f"""
        <div class="survey-top">
            <div class="survey-title">✦ 思维罗盘 · 高阶思维测评</div>
            <div class="survey-meta">
                第 {page + 1} / {total_pages} 页 · 已完成 {answered_count} / {len(QUESTIONS)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(answered_count / len(QUESTIONS))
    st.caption("请逐题阅读，选择最接近你真实情况的一项。")

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

        if idx in st.session_state.answers and widget_key not in st.session_state:
            st.session_state[widget_key] = st.session_state.answers[idx]

        st.markdown(
            f"""
            <div class="q-card">
                <span class="q-number">Q{position}</span>
                <span class="q-text">{escape(q["text"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.radio(
            label=f"第 {position} 题",
            options=[1, 2, 3, 4, 5],
            index=None,
            format_func=lambda x: LABELS[x],
            key=widget_key,
            on_change=save_answer,
            args=(idx,),
            horizontal=True,
            label_visibility="collapsed",
        )

    page_complete = all(idx in st.session_state.answers for idx in current_indices)

    left, spacer, right = st.columns([1, 1.4, 1.6])

    with left:
        if page > 0:
            if st.button("← 返回上一页", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    with right:
        if page < total_pages - 1:
            if st.button(
                "继续下一页 →",
                type="primary",
                use_container_width=True,
                disabled=not page_complete,
            ):
                st.session_state.page += 1
                st.rerun()
        else:
            all_complete = len(st.session_state.answers) == len(QUESTIONS)
            if st.button(
                "查看我的思维画像 ✦",
                type="primary",
                use_container_width=True,
                disabled=not all_complete,
            ):
                st.session_state.stage = "result"
                st.rerun()

    if not page_complete:
        st.caption("完成本页全部题目后即可继续。")


# =========================================================
# Result
# =========================================================
elif st.session_state.stage == "result":
    overall, dim_scores, item_results = build_scores()
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strongest = ranked[0]
    weakest = ranked[-1]
    spread = strongest[1] - weakest[1]

    st.markdown(
        f"""
        <div class="result-hero">
            <div class="eyebrow">YOUR THINKING PROFILE</div>
            <div class="title">✦ 你的思维画像已经生成</div>
            <div class="desc">
                这份结果展示的是你在 AI 辅助学习情境中的思维特点。
                重点不是追求“满分”，而是看清自己的优势与下一步成长方向。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notices = response_quality()
    for text in notices:
        st.info("💡 " + text)

    c1, c2, c3 = st.columns([1.05, 1, 1])

    with c1:
        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-label">综合思维指数</div>
                <div class="score-number">{overall:.2f}</div>
                <div class="score-level">{score_level(overall)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        info = DIMENSION_INFO[strongest[0]]
        st.markdown(
            f"""
            <div class="mini-result">
                <div class="mini-icon">🏅 {info["icon"]}</div>
                <div class="mini-label">优势最突出的方向</div>
                <div class="mini-title">{escape(strongest[0])}</div>
                <div class="mini-score">{strongest[1]:.2f} / 10</div>
                <div class="muted">{escape(info["short"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        info = DIMENSION_INFO[weakest[0]]
        st.markdown(
            f"""
            <div class="mini-result">
                <div class="mini-icon">🧭 {info["icon"]}</div>
                <div class="mini-label">最值得优先提升</div>
                <div class="mini-title">{escape(weakest[0])}</div>
                <div class="mini-score">{weakest[1]:.2f} / 10</div>
                <div class="muted">{escape(info["short"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">◈</span>综合解读</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="soft-panel">
            {escape(overall_interpretation(overall, spread))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🕸️</span>七维能力画像</div>',
        unsafe_allow_html=True,
    )

    labels = DIMENSIONS + [DIMENSIONS[0]]
    values = [dim_scores[d] for d in DIMENSIONS] + [dim_scores[DIMENSIONS[0]]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            line=dict(color="#6C63FF", width=3),
            fillcolor="rgba(108,99,255,.17)",
            marker=dict(size=6, color="#4C8DFF"),
            hovertemplate="%{theta}<br>%{r:.2f}/10<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickvals=[0, 2, 4, 6, 8, 10],
                gridcolor="rgba(31,39,66,.10)",
                linecolor="rgba(31,39,66,.08)",
                tickfont=dict(color="#8890A3", size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(31,39,66,.08)",
                tickfont=dict(color="#3D455A", size=12),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=520,
        margin=dict(l=55, r=55, t=35, b=35),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title"><span class="section-icon">✦</span>每个维度怎么看</div>',
        unsafe_allow_html=True,
    )

    for d, s in ranked:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="dimension-card">
                <div class="dim-row">
                    <div class="dim-name"><span>{info["icon"]}</span>{escape(d)}</div>
                    <div class="dim-score">{s:.2f} / 10 · {dimension_status(s)}</div>
                </div>
                <div class="dim-desc">{escape(info["meaning"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🏅</span>你的优势</div>',
        unsafe_allow_html=True,
    )
    for d, s in ranked[:2]:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="advice-card">
                <strong>{info["icon"]} {escape(d)} · {s:.2f}/10</strong><br>
                <span class="muted">{escape(info["meaning"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🧭</span>下一步优先提升</div>',
        unsafe_allow_html=True,
    )

    for d, s in ranked[-2:][::-1]:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="advice-card">
                <strong>{info["icon"]} {escape(d)} · {s:.2f}/10</strong><br>
                <span class="muted">{escape(info["meaning"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for tip in info["tips"]:
            st.markdown(f"- {tip}")

    st.markdown(
        '<div class="section-title"><span class="section-icon">📝</span>最值得关注的具体习惯</div>',
        unsafe_allow_html=True,
    )

    lowest_items = sorted(
        item_results,
        key=lambda x: (
            x["scored_likert"],
            dim_scores[x["dimension"]],
            x["index"],
        ),
    )[:5]

    for x in lowest_items:
        st.markdown(
            f"""
            <div class="behavior-card">
                <strong>{DIMENSION_INFO[x["dimension"]]["icon"]} {escape(x["dimension"])}</strong><br>
                <span class="muted">{escape(x["text"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🚀</span>7 天行动建议</div>',
        unsafe_allow_html=True,
    )

    priority_dims = [d for d, _ in ranked[-2:]]
    d1, d2 = priority_dims[0], priority_dims[1]

    day_plan_html = (
        '<div class="soft-panel">'
        f'<strong>第 1–2 天｜{DIMENSION_INFO[d1]["icon"]} 聚焦 {escape(d1)}</strong><br>'
        '从上面的建议中选择 1 个动作，在一次真实学习任务中实践。<br><br>'
        f'<strong>第 3–4 天｜{DIMENSION_INFO[d2]["icon"]} 聚焦 {escape(d2)}</strong><br>'
        '只练一个具体行为，不需要一次改变很多。<br><br>'
        '<strong>第 5 天｜🧠 无 AI 独立检查</strong><br>'
        '选择一个已经借助 AI 学过的内容，暂时关闭 AI，用自己的话复述、解题或重建框架。<br><br>'
        '<strong>第 6 天｜🤝 人机协同复盘</strong><br>'
        '回看一次 AI 辅助任务，分别写下：AI 帮助了什么、可能误导了什么、最终由自己判断了什么。<br><br>'
        '<strong>第 7 天｜✦ 再次测评</strong><br>'
        '对比自己的具体学习行为是否变得更稳定，而不仅仅看分数变化。'
        '</div>'
    )
    st.markdown(day_plan_html, unsafe_allow_html=True)

    report_text = build_report_text(overall, dim_scores, item_results)

    st.download_button(
        "下载我的个人报告 ↓",
        data=report_text.encode("utf-8-sig"),
        file_name="思维罗盘_生成式AI高阶思维能力测评报告.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.caption(
        "本测评用于了解 AI 辅助学习情境中的思维特点与学习行为，可作为自我了解与学习改进的参考。"
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
