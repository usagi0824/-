# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime
from html import escape

# =========================
# 1. 页面设置
# =========================
st.set_page_config(
    page_title="GenAI-HOTS 高阶思维能力测评",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 24px 26px;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 18px;
        margin-bottom: 16px;
    }
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 2rem;
    }
    .muted {
        opacity: .72;
        font-size: .95rem;
    }
    .result-card {
        padding: 18px 20px;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 16px;
        margin: 10px 0;
    }
    .score-big {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.1;
    }
    div[data-testid="stRadio"] > label {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 2. 六维能力配置
# =========================
DIMENSIONS = [
    "批判性思维",
    "创造性思维",
    "问题解决能力",
    "元认知能力",
    "计算思维",
    "人机协同能力",
]

DIMENSION_SHORT = {
    "批判性思维": "批判",
    "创造性思维": "创造",
    "问题解决能力": "问题解决",
    "元认知能力": "元认知",
    "计算思维": "计算",
    "人机协同能力": "人机协同",
}

# =========================
# 3. 22道题
# 每个选项为 (显示文本, 分数)
# =========================
QUESTIONS = [
    {
        "id": 1,
        "dimension": "批判性思维",
        "title": "AI真的提高了成绩吗？",
        "stem": "某高校调查发现：经常使用生成式AI的学生平均课程成绩为84分，不使用AI的学生平均为78分。某AI工具据此认为：“数据证明，使用生成式AI可以使大学生成绩提高6分，因此学校应该鼓励所有学生使用AI。”你认为最合理的判断是：",
        "options": [
            ("两组相差6分，已经能够证明AI提高了成绩。", 0),
            ("目前只能说明AI使用与成绩存在关联，还需要考虑原有学习能力、专业、学习时间等因素。", 3),
            ("如果调查人数足够多，就可以认为AI导致了成绩提高。", 1),
            ("只要成绩差异达到统计显著，就能证明AI具有因果作用。", 1),
        ],
    },
    {
        "id": 2,
        "dimension": "批判性思维",
        "title": "哪条证据最值得相信？",
        "stem": "你需要研究“生成式AI是否会降低大学生独立思考能力”，搜索到四份材料。如果只能优先参考一项，你会选择：",
        "options": [
            ("某短视频博主根据自己使用ChatGPT的经历认为“AI让人越来越懒”。", 0),
            ("某AI企业发布用户调查，但没有公布抽样方式和完整问卷。", 1),
            ("某高校对一个专业80名学生进行问卷调查，并公布基本统计结果。", 2),
            ("一项多高校研究报告说明了样本来源、变量定义、分析方法、结果及研究局限。", 3),
        ],
    },
    {
        "id": 3,
        "dimension": "批判性思维",
        "title": "AI给出了一个可疑参考文献",
        "stem": "你让AI帮助写论文，它提供了一篇参考文献，但你在学校数据库里暂时没有搜到。最合理的处理方式是：",
        "options": [
            ("AI通常掌握大量文献，可以直接引用。", 0),
            ("再问AI一次“你确定这篇文献存在吗”，如果它说确定就使用。", 1),
            ("到学术数据库、期刊官网或DOI系统核查文献是否真实存在，在无法验证前不引用。", 3),
            ("把作者和年份删掉，只保留文献观点。", 0),
        ],
    },
    {
        "id": 4,
        "dimension": "批判性思维",
        "title": "隐藏的假设",
        "stem": "有人提出：“生成式AI能够明显缩短学生完成作业的时间，因此使用AI一定能够提升大学生的高阶思维能力。”这个论证中最关键的隐藏假设是：",
        "options": [
            ("节省出来的时间会被用于更深入的分析、反思和创造，而不是进一步减少思考投入。", 3),
            ("所有大学生都使用同一个AI工具。", 0),
            ("AI生成文字的速度比人快。", 1),
            ("大学生每天都会完成作业。", 0),
        ],
    },
    {
        "id": 5,
        "dimension": "创造性思维",
        "title": "如何减少“AI直接抄答案”？",
        "stem": "学校希望减少学生直接复制AI答案，但又不想禁止AI。下面哪组方案体现出的思路差异最大，同时又比较可实施？",
        "options": [
            ("在教学楼张贴“不要依赖AI”海报；在图书馆增加类似海报。", 0),
            ("开设AI使用讲座；增加一次AI使用专题讲座。", 1),
            ("设置“先独立思考5分钟再使用AI”的学习流程；同时在AI辅助作业中随机进行简短口头答辩。", 3),
            ("限制每天使用AI三次；同时限制每次使用AI的时间。", 1),
        ],
    },
    {
        "id": 6,
        "dimension": "创造性思维",
        "title": "怎样教学生正确使用AI？",
        "stem": "学校准备开展“生成式AI使用能力训练”。以下哪一种设计兼顾新颖性和实际效果？",
        "options": [
            ("请老师做一次“ChatGPT基本功能介绍”讲座。", 1),
            ("设置“AI找茬实验室”：学生比较AI答案与真实资料，寻找错误、偏见和遗漏，再修改提示词重新生成并记录变化。", 3),
            ("给每位学生发一份AI使用说明书。", 1),
            ("要求学生背诵20条提示词模板。", 0),
        ],
    },
    {
        "id": 7,
        "dimension": "创造性思维",
        "title": "改进一个普通方案",
        "stem": "AI为“大学生AI素养周”设计了三个活动：专家讲座、张贴宣传海报、活动结束后填写满意度调查。如果要求你在原方案基础上明显提升其价值，哪种改进最好？",
        "options": [
            ("把讲座时间从60分钟增加到90分钟。", 1),
            ("增加更多海报，让更多学生看到。", 1),
            ("把满意度调查由5题增加到20题。", 0),
            ("加入“识别AI错误—修改提示词—比较修改前后输出—反思AI适用边界”的挑战任务，并比较活动前后的表现。", 3),
        ],
    },
    {
        "id": 8,
        "dimension": "创造性思维",
        "title": "哪个研究问题更有价值？",
        "stem": "你观察到：经常使用AI的学生通常完成作业更快，但深度理解程度并不一定更高。如果围绕这一现象开展研究，哪个问题最具有探索价值？",
        "options": [
            ("在不同任务难度和不同AI核验习惯下，AI使用如何同时影响学习效率与深度理解？", 3),
            ("大学生使用AI吗？", 1),
            ("ChatGPT是什么时候发布的？", 0),
            ("使用AI的学生每天平均使用多少分钟？", 1),
        ],
    },
    {
        "id": 9,
        "dimension": "问题解决能力",
        "title": "作业质量为什么下降？",
        "stem": "某学院允许学生使用生成式AI后，教师发现部分课程的作业质量反而下降。面对这一情况，最合理的第一步是什么？",
        "options": [
            ("立即全面禁止学生使用AI。", 0),
            ("明确“作业质量下降”具体表现，并比较不同课程、学生和AI使用方式，寻找可能原因。", 3),
            ("要求所有教师增加作业数量。", 1),
            ("直接判断原因是学生变懒。", 0),
        ],
    },
    {
        "id": 10,
        "dimension": "问题解决能力",
        "title": "小组项目出现危机",
        "stem": "你们四人小组明天要提交报告。AI生成的数据分析结果与原始Excel明显不一致，而团队只剩3小时。最佳处理方案是：",
        "options": [
            ("时间不够了，直接采用AI结果。", 0),
            ("从头重新做整份报告，所有人一起检查每一个字。", 1),
            ("先定位影响结论的关键数据和计算环节，分工核查原始数据与代码，优先修正高风险错误，再检查其他内容。", 3),
            ("删除全部数据分析，只交文字部分。", 0),
        ],
    },
    {
        "id": 11,
        "dimension": "问题解决能力",
        "title": "活动报名率很低",
        "stem": "你负责一个校园活动，原计划报名300人，但三天后只有42人。下面哪种处理更合理？",
        "options": [
            ("马上投入全部预算购买广告。", 1),
            ("继续按照原计划等待，因为距离活动还有时间。", 1),
            ("把活动取消，以避免失败。", 0),
            ("先分析报名渠道、目标人群和页面转化情况，访谈少量未报名学生，再根据主要障碍调整方案并观察新的报名数据。", 3),
        ],
    },
    {
        "id": 12,
        "dimension": "问题解决能力",
        "title": "如何判断方案有没有用？",
        "stem": "学校推出了一项“AI辅助学习但防止思维依赖”的新教学方案。哪种评价方式最好？",
        "options": [
            ("在实施前设定指标，比较实施前后以及不同学生群体的表现，同时结合测试结果、使用行为和学生反馈。", 3),
            ("问负责项目的老师“感觉效果怎么样”。", 0),
            ("只统计有多少学生参加。", 1),
            ("找一个成绩提高最多的学生作为成功案例。", 0),
        ],
    },
    {
        "id": 13,
        "dimension": "元认知能力",
        "title": "AI说你懂了，你真的懂了吗？",
        "stem": "你正在学习一个比较难的统计模型。看完AI解释后感觉“好像懂了”。哪种做法最能判断自己是否真的掌握？",
        "options": [
            ("再看一遍AI答案。", 1),
            ("收藏这段对话，以后需要时查看。", 1),
            ("关闭AI，尝试用自己的话解释模型并独立解决一道新问题，再检查自己卡在哪里。", 3),
            ("让AI把解释进一步简化。", 1),
        ],
    },
    {
        "id": 14,
        "dimension": "元认知能力",
        "title": "AI和你的答案不一样",
        "stem": "你独立得到答案A，但AI给出了答案B，并且AI的解释看起来很专业。你最合理的做法是：",
        "options": [
            ("AI掌握的信息更多，因此直接改成B。", 0),
            ("分别检查自己的推理与AI推理依据，通过教材、数据或可靠资料验证关键步骤后再决定。", 3),
            ("坚持自己的答案，因为独立思考最重要。", 1),
            ("再问几个AI模型，选择出现次数最多的答案。", 1),
        ],
    },
    {
        "id": 15,
        "dimension": "元认知能力",
        "title": "发现自己的学习方法没效果",
        "stem": "你连续两周让AI整理教材、生成笔记，但测试成绩没有提高。下一步最合理的是：",
        "options": [
            ("继续使用同样方法，只是每天增加使用AI的时间。", 0),
            ("换一个更先进的大模型。", 1),
            ("暂停所有AI工具。", 1),
            ("分析自己在哪些题型和知识环节失分，将AI从“替我整理”改成“出题—独立回答—反馈—订正”，再比较效果。", 3),
        ],
    },
    {
        "id": 16,
        "dimension": "计算思维",
        "title": "如何处理一个复杂研究任务？",
        "stem": "你的任务是：分析2000份大学生问卷，研究生成式AI使用与高阶思维能力之间的关系，并形成报告。哪种任务拆解最合理？",
        "options": [
            ("明确问题 → 整理变量 → 数据清洗 → 描述分析 → 建模检验 → 结果验证 → 可视化与报告。", 3),
            ("先画图 → 写结论 → 再找能支持结论的数据。", 0),
            ("把Excel全部上传给AI，让AI自行决定分析方法。", 1),
            ("先写报告正文，再根据正文需要计算数据。", 0),
        ],
    },
    {
        "id": 17,
        "dimension": "计算思维",
        "title": "程序结果异常",
        "stem": "你写了一个程序：读取学生成绩 → 删除重复数据 → 计算平均成绩 → 按专业进行比较。结果显示总样本原本有1000人，删除重复记录后只剩430人。你怀疑程序有问题。最合理的处理方法是：",
        "options": [
            ("430看起来也不少，可以继续分析。", 0),
            ("把删除重复数据这一步直接取消。", 1),
            ("分步骤检查数据量，查看程序根据哪些字段判断“重复”，抽取被删除样本验证规则是否正确。", 3),
            ("重新运行几次，如果结果都一样就说明没有问题。", 0),
        ],
    },
    {
        "id": 18,
        "dimension": "计算思维",
        "title": "如何设计一个自动反馈系统？",
        "stem": "你想做一个系统：学生完成测试 → 根据六个维度得分 → 找出优势和短板 → 输出建议。哪种逻辑最合理？",
        "options": [
            ("每个人随机生成一段不同建议。", 0),
            ("先分别计算各维度标准化得分，再依据预先制定的等级与规则识别高低维度，最后匹配相应建议。", 3),
            ("只看总分，总分一样的人报告完全相同。", 1),
            ("直接让AI根据学生姓名猜测能力。", 0),
        ],
    },
    {
        "id": 19,
        "dimension": "人机协同能力",
        "title": "哪一个提示词质量最高？",
        "stem": "你要让AI帮助你分析“生成式AI是否影响大学生高阶思维”。下面哪一个提示词最好？",
        "options": [
            ("帮我分析AI。", 0),
            ("帮我写一篇关于AI影响大学生的文章，越详细越好。", 1),
            ("分析AI对大学生高阶思维的影响，直接告诉我结论。", 2),
            ("我正在研究生成式AI对大学生高阶思维的影响。请分别从批判性思维、创造性思维和问题解决三个方面提出可能的正负机制；区分已有证据和你的推断，并指出需要进一步验证的假设，以表格形式输出。", 3),
        ],
    },
    {
        "id": 20,
        "dimension": "人机协同能力",
        "title": "怎样验证AI答案？",
        "stem": "AI告诉你：“有研究表明，83%的大学生使用生成式AI后批判性思维显著下降。”你最合理的处理方式是：",
        "options": [
            ("要求获得原始研究名称或出处，并在论文、官方报告或可信数据库中核查样本、研究方法和原始结论。", 3),
            ("这个数字非常具体，因此可信度应该比较高。", 0),
            ("再问AI“这个数字是真的吗”。", 1),
            ("搜索互联网，只要找到另一个网页也写83%就可以引用。", 1),
        ],
    },
    {
        "id": 21,
        "dimension": "人机协同能力",
        "title": "哪种人机分工最好？",
        "stem": "要完成一份重要研究报告，以下哪种分工最合理？",
        "options": [
            ("让AI完成选题、数据分析、解释和最终结论，人只负责排版。", 0),
            ("所有事情坚持人工完成，完全不用AI。", 1),
            ("人负责研究问题、关键判断、证据核验和最终责任；AI用于头脑风暴、代码辅助、文字整理等，并由人持续检查输出。", 3),
            ("AI负责所有复杂任务，人负责简单任务。", 0),
        ],
    },
    {
        "id": 22,
        "dimension": "人机协同能力",
        "title": "哪一种AI使用过程最好？",
        "stem": "面对一个复杂课程项目，下面哪种工作方式最合理？",
        "options": [
            ("直接让AI生成完整答案 → 提交。", 0),
            ("明确任务 → 自己形成初步判断 → 请求AI提供替代思路 → 比较与质疑AI输出 → 修改方案 → 核验关键事实 → 自己做最终决定。", 3),
            ("问AI → 如果答案不好就不停点击重新生成 → 选择最长的一份。", 1),
            ("同时问多个AI → 使用多数AI一致的答案。", 1),
        ],
    },
]

# =========================
# 4. 报告文本库
# =========================
STRENGTH_TEXT = {
    "批判性思维": "你能够较好地区分“相关”与“因果”，重视证据质量、信息来源和隐藏假设，在面对AI生成内容时具有较强的审查意识。",
    "创造性思维": "你善于从不同角度重新定义问题，并能提出差异化方案，而不是只对既有方案做表面修改。",
    "问题解决能力": "你倾向于先界定问题、识别关键约束，再选择策略并验证结果，面对复杂任务时具有较强的行动组织能力。",
    "元认知能力": "你能够监控自己的理解程度，并根据反馈调整学习方式，不容易把“看懂AI解释”误当成“真正掌握”。",
    "计算思维": "你能够把复杂任务拆成步骤，重视规则、流程、调试和验证，具备较好的结构化问题处理意识。",
    "人机协同能力": "你较能把生成式AI当作辅助工具，而不是最终决策者，知道如何提出更清晰的任务、核验输出并保留人的最终判断。",
}

WEAK_TEXT = {
    "批判性思维": "你在证据可信度、因果判断或隐藏假设识别方面还有提升空间。面对AI给出的“看起来很专业”的结论时，可能较容易接受表面上的确定性。",
    "创造性思维": "你目前更容易选择常规或渐进式方案，在生成多样化想法、重新界定问题和改进既有方案方面还有提升空间。",
    "问题解决能力": "面对复杂问题时，你可能较快进入执行阶段，但对问题界定、优先级、验证指标和反馈调整考虑得还不够充分。",
    "元认知能力": "你需要进一步区分“熟悉感”和“真正掌握”。仅阅读AI解释或反复查看答案，并不能替代独立提取、迁移和自我检测。",
    "计算思维": "你在任务拆解、流程设计、异常调试和规则化表达方面还有提升空间，复杂任务容易被整体处理而缺少可验证的中间步骤。",
    "人机协同能力": "你对AI的任务分工、提示词结构或结果核验仍可加强。使用AI时需要减少“直接接受第一次输出”的倾向。",
}

ADVICE = {
    "批判性思维": [
        "采用“证据—来源—方法—结论”四步核验：看到重要结论时，至少检查一次原始来源。",
        "每周选择1个AI回答，主动寻找一个反例或替代解释。",
        "论文写作中不直接引用AI提供的文献条目，先到数据库或期刊官网核实。",
    ],
    "创造性思维": [
        "遇到开放任务时，先独立提出至少3种明显不同的方案，再让AI补充。",
        "练习“换对象、换约束、换目标、换场景”四种重新定义问题的方法。",
        "不要只让AI“优化已有方案”，可要求它提供互相冲突的替代路径，再由你比较。",
    ],
    "问题解决能力": [
        "复杂任务先写出：目标、约束、关键变量、优先级、验证指标，再开始执行。",
        "遇到异常先定位最可能影响结论的高风险环节，不要平均用力检查全部内容。",
        "每完成一个阶段都设置一个可观察的结果，用数据判断是否需要调整策略。",
    ],
    "元认知能力": [
        "学完一个知识点后关闭AI，用自己的话解释，并独立完成一道新题。",
        "建立“我以为会—实际不会”的错题记录，定期分析判断偏差来自哪里。",
        "把AI从“替我整理笔记”改成“出题—我回答—AI反馈—我订正”。",
    ],
    "计算思维": [
        "用“输入—处理—输出—检查”描述复杂任务，再把处理部分拆成3—5步。",
        "程序或数据异常时逐步记录每一步的数据量和结果，定位首次出现异常的位置。",
        "尝试把常见学习流程写成规则或流程图，训练结构化表达。",
    ],
    "人机协同能力": [
        "提示词中尽量写清楚目标、背景、约束、输出格式和需要核验的部分。",
        "重要任务采用“人先判断—AI给替代方案—人核验—人最终决策”的流程。",
        "把AI输出分成“事实、推断、建议”三类，对事实部分优先进行外部核验。",
    ],
}

# =========================
# 5. 工具函数
# =========================
def get_level(score: float) -> str:
    if score >= 90:
        return "卓越"
    if score >= 80:
        return "优秀"
    if score >= 70:
        return "良好"
    if score >= 60:
        return "中等"
    return "有待提升"


def calculate_scores(answer_scores: dict):
    raw = {d: 0 for d in DIMENSIONS}
    max_raw = {d: 0 for d in DIMENSIONS}

    for q in QUESTIONS:
        d = q["dimension"]
        max_raw[d] += 3
        raw[d] += answer_scores[q["id"]]

    dimension_scores = {
        d: round(raw[d] / max_raw[d] * 100, 1)
        for d in DIMENSIONS
    }
    overall = round(sum(dimension_scores.values()) / len(DIMENSIONS), 1)
    return dimension_scores, overall


def make_radar(scores: dict):
    labels = list(scores.keys())
    values = [scores[k] for k in labels]
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name="能力得分",
            hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
            )
        ),
        showlegend=False,
        height=480,
        margin=dict(l=55, r=55, t=45, b=45),
    )
    return fig


def make_report_html(name, grade, scores, overall):
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    strengths = [x[0] for x in sorted_dims[:2]]
    weaknesses = [x[0] for x in sorted_dims[-2:]]

    safe_name = escape(name.strip()) if name.strip() else "匿名测试者"
    safe_grade = escape(grade)

    score_rows = "".join(
        f"<tr><td>{escape(d)}</td><td>{s:.1f}</td><td>{get_level(s)}</td></tr>"
        for d, s in scores.items()
    )

    strength_html = "".join(
        f"<h3>{escape(d)}（{scores[d]:.1f}分）</h3><p>{escape(STRENGTH_TEXT[d])}</p>"
        for d in strengths
    )

    weak_html = "".join(
        f"<h3>{escape(d)}（{scores[d]:.1f}分）</h3><p>{escape(WEAK_TEXT[d])}</p>"
        for d in weaknesses
    )

    advice_html = ""
    for d in weaknesses:
        advice_html += f"<h3>{escape(d)}提升建议</h3><ul>"
        for item in ADVICE[d]:
            advice_html += f"<li>{escape(item)}</li>"
        advice_html += "</ul>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>GenAI-HOTS个人测评报告</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
    max-width: 820px; margin: 40px auto; padding: 0 28px; color: #222; line-height: 1.75;
}}
h1 {{ margin-bottom: 4px; }}
h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 8px; margin-top: 34px; }}
.hero {{ background:#f6f7f9; padding:20px 24px; border-radius:14px; }}
.big {{ font-size:40px; font-weight:800; }}
table {{ border-collapse:collapse; width:100%; margin:14px 0; }}
th, td {{ border:1px solid #ddd; padding:10px; text-align:left; }}
th {{ background:#f6f7f9; }}
.note {{ font-size:13px; color:#666; margin-top:30px; }}
@media print {{
    body {{ margin: 0 auto; }}
}}
</style>
</head>
<body>
<h1>GenAI-HOTS 大学生高阶思维能力测评</h1>
<p>个人测评报告</p>

<div class="hero">
<p><b>测试者：</b>{safe_name}　 <b>年级：</b>{safe_grade}</p>
<div class="big">{overall:.1f} / 100</div>
<p><b>综合水平：{get_level(overall)}</b></p>
<p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
</div>

<h2>一、六维能力画像</h2>
<table>
<tr><th>能力维度</th><th>得分</th><th>水平</th></tr>
{score_rows}
</table>

<h2>二、你的主要优势</h2>
{strength_html}

<h2>三、当前需要重点提升的能力</h2>
{weak_html}

<h2>四、针对性提升建议</h2>
{advice_html}

<h2>五、结果说明</h2>
<p>本结果根据22道生成式AI情境高阶思维题的规则评分生成，用于学习能力自我诊断和项目研究。当前版本属于原型测评，不等同于经过大样本常模验证的标准化心理或教育测验。</p>
<p>如果后续完成正式试测，可进一步加入题目区分度、信度、效度分析以及基于真实样本的百分位比较。</p>

<p class="note">测评框架参考OECD PISA创造性思维、问题解决与数字化学习框架，AAC&U VALUE Rubrics，以及UNESCO学生AI能力框架，并结合大学生生成式AI使用情境进行本土化设计。</p>
</body>
</html>"""


def reset_test():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# =========================
# 6. 会话初始化
# =========================
if "shuffle_seed" not in st.session_state:
    st.session_state.shuffle_seed = random.randint(100000, 999999)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# =========================
# 7. 首页
# =========================
st.markdown(
    """
    <div class="hero">
      <h1>🧠 GenAI-HOTS 高阶思维能力测评</h1>
      <div class="muted">
        面向大学生的生成式AI情境高阶思维能力自我诊断 · 22题 · 约8–12分钟
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("📌 测评说明（建议先阅读）", expanded=False):
    st.markdown(
        """
- 本测试包含 **批判性思维、创造性思维、问题解决、元认知、计算思维、人机协同** 六个维度。
- 题目主要考察复杂情境下的判断与策略选择，不是AI知识竞赛。
- 请按照你认为**最合理的处理方式**作答，不需要搜索答案。
- 当前版本用于学习诊断和项目研究，**不是标准化心理测验或医学诊断工具**。
- 为保护隐私，本版本不要求填写姓名、手机号、身份证号等信息；昵称可不填。
        """
    )

# =========================
# 8. 测试表单
# =========================
if not st.session_state.submitted:
    st.subheader("开始测评")

    with st.form("hots_test_form"):
        c1, c2 = st.columns(2)
        with c1:
            nickname = st.text_input(
                "昵称（可不填）",
                placeholder="例如：测试者01",
                max_chars=20,
            )
        with c2:
            grade = st.selectbox(
                "年级",
                ["大一", "大二", "大三", "大四", "研究生", "其他"],
            )

        st.caption("请完成全部22题后一次提交。选项顺序会在当前测试会话中保持稳定。")
        st.divider()

        selected_texts = {}

        for i, q in enumerate(QUESTIONS, start=1):
            st.markdown(f"### {i}. {q['title']}")
            st.write(q["stem"])

            # 在每个会话中稳定随机选项顺序
            opts = q["options"].copy()
            rng = random.Random(st.session_state.shuffle_seed + q["id"] * 9973)
            rng.shuffle(opts)

            labels = [x[0] for x in opts]
            selected = st.radio(
                f"第{i}题",
                labels,
                index=None,
                key=f"q_{q['id']}",
                label_visibility="collapsed",
            )
            selected_texts[q["id"]] = selected
            st.caption(f"能力维度：{q['dimension']}")
            st.divider()

        submitted = st.form_submit_button(
            "提交并生成个人报告",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        unanswered = [qid for qid, val in selected_texts.items() if val is None]

        if unanswered:
            st.error(
                f"还有 {len(unanswered)} 题未完成："
                + "、".join(str(x) for x in unanswered)
                + "。请补充后再提交。"
            )
        else:
            answer_scores = {}
            for q in QUESTIONS:
                selected = selected_texts[q["id"]]
                score_map = {text: score for text, score in q["options"]}
                answer_scores[q["id"]] = score_map[selected]

            dimension_scores, overall = calculate_scores(answer_scores)

            st.session_state.submitted = True
            st.session_state.nickname = nickname
            st.session_state.grade = grade
            st.session_state.answer_scores = answer_scores
            st.session_state.dimension_scores = dimension_scores
            st.session_state.overall = overall
            st.rerun()

# =========================
# 9. 结果页
# =========================
else:
    name = st.session_state.nickname.strip() or "匿名测试者"
    grade = st.session_state.grade
    scores = st.session_state.dimension_scores
    overall = st.session_state.overall

    st.success("测评完成，以下是你的个人诊断结果。")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("高阶思维综合指数", f"{overall:.1f} / 100")
    with col2:
        st.metric("综合水平", get_level(overall))

    st.caption(f"测试者：{name} ｜ 年级：{grade}")

    st.subheader("六维能力画像")
    st.plotly_chart(make_radar(scores), use_container_width=True)

    metric_cols = st.columns(3)
    for idx, d in enumerate(DIMENSIONS):
        with metric_cols[idx % 3]:
            st.metric(DIMENSION_SHORT[d], f"{scores[d]:.1f}")

    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    strengths = [x[0] for x in sorted_dims[:2]]
    weaknesses = [x[0] for x in sorted_dims[-2:]]

    st.subheader("你的主要优势")
    for d in strengths:
        st.markdown(
            f"""
            <div class="result-card">
            <b>{d}｜{scores[d]:.1f}分｜{get_level(scores[d])}</b><br><br>
            {STRENGTH_TEXT[d]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("当前需要重点提升")
    for d in weaknesses:
        st.markdown(
            f"""
            <div class="result-card">
            <b>{d}｜{scores[d]:.1f}分｜{get_level(scores[d])}</b><br><br>
            {WEAK_TEXT[d]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("针对性提升建议")
    for d in weaknesses:
        st.markdown(f"**{d}**")
        for item in ADVICE[d]:
            st.markdown(f"- {item}")

    st.info(
        "当前V1.0暂不显示“超过多少百分比的大学生”。"
        "这一功能应在你们完成真实试测、建立样本分布后再加入，避免虚构常模。"
    )

    st.subheader("下载个人报告")
    report_html = make_report_html(name, grade, scores, overall)

    st.download_button(
        "⬇️ 下载HTML个人报告",
        data=report_html.encode("utf-8"),
        file_name=f"GenAI-HOTS_个人报告_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html",
        use_container_width=True,
    )

    st.caption(
        "下载后用浏览器打开即可查看，也可以在浏览器中选择“打印 → 另存为PDF”。"
    )

    st.divider()
    st.caption(
        "测评框架参考：OECD PISA Creative Thinking / Problem Solving / "
        "Learning in the Digital World；AAC&U VALUE Rubrics；UNESCO AI Competency Framework for Students。"
    )

    if st.button("🔄 重新测试", use_container_width=True):
        reset_test()
