import streamlit as st
import time
import random

# ==================== 1. 配置与模拟数据 ====================
st.set_page_config(
    page_title="XinguaGen English",
    page_icon="🎓",
    layout="centered"
)

# --- CSS Hack: 隐藏菜单、页脚、工具栏 ---
hide_streamlit_style = """
<style>
    /* 1. 隐藏右上角汉堡菜单 (三个点) */
    #MainMenu {visibility: hidden;}
    
    /* 2. 隐藏底部 "Made with Streamlit" 页脚 */
    footer {visibility: hidden;}
    
    /* 3. 隐藏顶部带有 Deploy 按钮的 Header */
    header {visibility: hidden;}
    
    /* 4. 隐藏 Streamlit Cloud 的工具栏 (包含 Google 账号信息和 Manage App 按钮) */
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0px;
    }
    
    /* 5. 调整顶部空白，让内容更靠上，看起来更像原生 App */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }
    
    /* 6. 针对移动端的优化，移除顶部彩条装饰 */
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0px;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 初始化 Session State (状态管理) ---
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

# 模拟数据 (V3.1 - Human-like Academic & General News & Slang Spoken)
MOCK_DATA = {
    "spoken": {
        "short": {
            "title": "Catching Up & Weekend Vibes (Short)",
            "content": """Mike: Yo, Sarah! Long time no see. I thought you were ghosting us!
Sarah: No way! Just been swamped with that new gig. Honestly, I'm running on fumes.
Mike: That sucks. You gotta chill this weekend. We're hitting up that new burger joint tonight. You down?
Sarah: Oh, I'm totally down. I need some comfort food to save my soul.
Mike: Sweet. I'll swing by your place around 7?""",
            "vocab": [
                {"word": "ghosting", "pos": "v. (slang)", "meaning": "玩失踪/断联", "phrase": "stop ghosting me"},
                {"word": "swamped", "pos": "adj.", "meaning": "忙得不可开交", "phrase": "swamped with work"},
                {"word": "running on fumes", "pos": "idiom", "meaning": "精疲力竭 (像车没油了)", "phrase": "I'm running on fumes"}
            ],
            "analysis": [
                {"sentence": "Yo, Sarah! Long time no see.", "translation": "哟 Sarah！好久不见。", "grammar": "【语用】'Yo' 是非常非正式的打招呼方式，仅限熟人。"},
                {"sentence": "I thought you were ghosting us!", "translation": "我还以为你故意躲着我们呢！", "grammar": "【语用】'Ghosting' 原指约会中突然断联，现在广泛用于朋友间开玩笑。"}
            ]
        },
        "long": {
            "title": "Tech Talk & Weekend Plans (Extended)",
            "content": """Alex: Dude, did you see the keynote yesterday? The new AI model is insane.
Ben: Yeah, it's a total game-changer. But honestly, the price tag is a rip-off.
Alex: True, but for the features? I might bite the bullet and get it.
Ben: You're such a tech junkie. Anyway, enough shop talk. What's the plan for Saturday?
Alex: Nothing much. Just gonna kick back and maybe binge-watch that new sci-fi series.
Ben: Lame! You should come hiking with us. The weather's gonna be killer.
Alex: Hiking? You know I'm a couch potato.
Ben: Come on, don't be a flake. It’s just a light trail, easy peasy.
Alex: Alright, alright, twist my arm. I'm in. But food is on you after.""",
            "vocab": [
                {"word": "rip-off", "pos": "n. (slang)", "meaning": "抢钱/宰客 (太贵)", "phrase": "What a rip-off!"},
                {"word": "bite the bullet", "pos": "idiom", "meaning": "咬牙/硬着头皮做", "phrase": "bite the bullet"},
                {"word": "kick back", "pos": "v. phrase", "meaning": "放松/休息", "phrase": "kick back and relax"},
                {"word": "flake", "pos": "n. (slang)", "meaning": "放鸽子的人/不靠谱的人", "phrase": "Don't be a flake"}
            ],
            "analysis": [
                {"sentence": "The new AI model is insane.", "translation": "那个新 AI 模型简直疯了（太强了）。", "grammar": "【语用】'insane' 在这里是极度褒义，表示好得令人难以置信。"},
                {"sentence": "But honestly, the price tag is a rip-off.", "translation": "但说实话，这价格简直是抢钱。", "grammar": "【语用】'Rip-off' 是抱怨价格虚高最常用的俚语。"},
                {"sentence": "Alright, alright, twist my arm.", "translation": "行吧行吧，你赢了（被你强行说服了）。", "grammar": "【语用】'Twist my arm' 指'在强力劝说下同意了'，幽默的妥协。"}
            ]
        }
    },
    "news": {
        "short": {
            "title": "City Launches Green Initiative (Brief)",
            "content": """The City Council announced a comprehensive "Green City" plan today aimed at reducing urban carbon emissions by 30% over the next five years. The initiative includes expanding public transit, planting 10,000 new trees, and offering subsidies for electric vehicles. Mayor Johnson stated that this project represents a "vital step" towards a sustainable future.""",
            "vocab": [
                {"word": "comprehensive", "pos": "adj.", "meaning": "全面的", "phrase": "comprehensive plan"},
                {"word": "subsidies", "pos": "n.", "meaning": "补贴", "phrase": "government subsidies"}
            ],
            "analysis": [
                {"sentence": "The initiative includes expanding public transit...", "translation": "该倡议包括扩建公共交通...", "grammar": "【结构】使用平行结构 (expanding, planting, offering) 列举措施，新闻语体特征。"}
            ]
        },
        "long": {
            "title": "Tech Giant Unveils Revolutionary Device (Report)",
            "content": """Global tech giant Nexus Corp unveiled its latest wearable device yesterday, promising to revolutionize how users monitor their health. The device, named "PulseLink," features advanced sensors capable of tracking blood glucose levels non-invasively.
            
Industry analysts have reacted positively to the launch, noting that the stock price of Nexus Corp jumped by 5% following the announcement. "This is the breakthrough the market has been waiting for," said Sarah Chen, a senior tech analyst at FutureTrends.
            
However, privacy advocates have raised concerns regarding data security. The company has assured users that all health data will be encrypted locally on the device.""",
            "vocab": [
                {"word": "unveiled", "pos": "v.", "meaning": "揭幕/公布", "phrase": "unveiled a new product"},
                {"word": "revolutionize", "pos": "v.", "meaning": "彻底改变", "phrase": "revolutionize the industry"},
                {"word": "non-invasively", "pos": "adv.", "meaning": "无创地", "phrase": "track non-invasively"}
            ],
            "analysis": [
                {"sentence": "Global tech giant Nexus Corp unveiled its latest wearable device...", "translation": "全球科技巨头 Nexus 公司揭幕了其最新设备...", "grammar": "【选词】'Unveiled' 比 'released' 更具隆重感。"},
                {"sentence": "However, privacy advocates have raised concerns...", "translation": "然而，隐私倡导者提出了担忧...", "grammar": "【结构】新闻报道使用 'However' 引入对立观点，保持报道平衡性 (Balance)。"}
            ]
        }
    },
    "academic": {
        "short": {
            "title": "The Illusion of Understanding (Short)",
            "content": """Large Language Models (LLMs) have achieved something remarkable: they can write poetry, code, and essays that feel human. But don't be fooled. Beneath this surface fluency lies a critical gap in semantic understanding. While syntax—the structural rules of language—is mastered, true meaning often remains elusive.""",
            "vocab": [
                {"word": "remarkable", "pos": "adj.", "meaning": "非凡的", "phrase": "achieved something remarkable"},
                {"word": "elusive", "pos": "adj.", "meaning": "难以捉摸的", "phrase": "remains elusive"}
            ],
            "analysis": [
                {"sentence": "But don't be fooled.", "translation": "但别被骗了。", "grammar": "【节奏】极短的祈使句 (Punchy Sentence)，在长句后制造强烈节奏对比。"}
            ]
        },
        "long": {
            "title": "The Limits of Artificial Intuition (Essay)",
            "content": """Large Language Models (LLMs) have achieved something remarkable: they can write poetry, code, and essays that feel human. But don't be fooled. Beneath this surface fluency lies a critical gap in semantic understanding.
            
Historically, linguists treated grammar like a set of rigid rules—a puzzle to be solved. Early AI struggled with this. Today's neural networks, however, learn patterns by digesting massive datasets, effectively mimicking human intuition without actually possessing it. They are, in a sense, like parrots with an infinite memory.

This distinction matters. As we integrate these systems into education and law, we run a serious risk. We need to move beyond awe and start demanding explainability.""",
            "vocab": [
                {"word": "digest", "pos": "v.", "meaning": "消化/理解", "phrase": "digesting massive datasets"},
                {"word": "mimic", "pos": "v.", "meaning": "模仿", "phrase": "mimicking human intuition"},
                {"word": "intuition", "pos": "n.", "meaning": "直觉", "phrase": "human intuition"}
            ],
            "analysis": [
                {"sentence": "Historically, linguists treated grammar like a set of rigid rules—a puzzle to be solved.", "translation": "历史上，语言学家将语法视为一套死板的规则——就像一个待解的谜题。", "grammar": "【修辞】使用破折号引入隐喻 (puzzle)，使抽象概念具体化。"},
                {"sentence": "They are, in a sense, like parrots with an infinite memory.", "translation": "从某种意义上说，它们就像拥有无限记忆力的鹦鹉。", "grammar": "【修辞】使用类比 (Analogy) 'like parrots'，这是真人学者常用的生动表达。"}
            ]
        }
    }
}

# ==================== 2. 侧边栏设置 ====================
with st.sidebar:
    st.header("⚙️ 设置 (Settings)")
    
    topic = st.text_input("1. 场景/话题 (Topic)", "Ordering Coffee / Tech News")
    
    article_type = st.selectbox(
        "2. 文章类型 (Type)",
        options=["spoken", "news", "academic"],
        format_func=lambda x: {
            "spoken": "🗣️ 口语对话 (Slang & Idioms)",
            "news": "📰 新闻日报 (General English)",
            "academic": "🎓 学术文章 (Academic English)"
        }[x]
    )
    
    level = st.select_slider(
        "3. 词汇等级 (Level)",
        options=["Beginner", "Intermediate", "Advanced", "GRE/Academic"],
        value="Intermediate"
    )
    
    length = st.slider("4. 目标字数 (Length)", 50, 500, 150, step=10)
    
    st.markdown("---")
    st.caption("Designed for XinguaGen English")

# ==================== 3. 主界面逻辑 ====================

st.title("🎓 XinguaGen English")
st.markdown(f"**当前模式**: {article_type.capitalize()} | **目标**: {level} | **字数**: {length}")

# 生成按钮
if st.button("✨ 生成文章 (Generate)", type="primary", use_container_width=True):
    with st.spinner("AI 正在撰写中 (Using Advanced Model)..."):
        time.sleep(1.5)  # 模拟 API 延迟
        
        # 简单的逻辑判断：字数 > 200 使用长文，否则短文
        length_key = "long" if length > 200 else "short"
        st.session_state.generated_data = MOCK_DATA[article_type][length_key]
        st.rerun()

# 展示内容
data = st.session_state.generated_data

if data:
    st.markdown("---")
    
    # === Tab 1: 阅读 (Reading) ===
    tab1, tab2, tab3 = st.tabs(["📖 阅读 (Reading)", "📚 词汇 (Vocab)", "🧐 解析 (Analysis)"])
    
    with tab1:
        st.subheader(data["title"])
        
        # --- 简单的音频播放模拟 (可收起) ---
        with st.expander("🎧 朗读 (Audio Player)", expanded=False):
            st.info("点击下方播放朗读 (Demo Audio)")
            st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav", format="audio/wav")
        # ----------------------------------
        
        # 文本显示
        content_lines = data["content"].split('\n')
        for line in content_lines:
            if ":" in line and article_type == "spoken":
                # 对话格式化
                parts = line.split(":", 1)
                st.markdown(f"**{parts[0]}**: {parts[1]}")
            else:
                st.markdown(f"{line}")
                
        st.caption("💡 Tip: 切换到 '词汇' 或 '解析' 标签页查看详细讲解。")

    # === Tab 2: 词汇 (Vocab) ===
    with tab2:
        st.subheader("重点词汇 (Key Vocabulary)")
        for v in data["vocab"]:
            with st.expander(f"**{v['word']}** ({v['pos']})"):
                st.markdown(f"**含义**: {v['meaning']}")
                st.markdown(f"**搭配/例句**: *{v['phrase']}*")
                if "slang" in v["pos"] or "idiom" in v["pos"]:
                    st.badge("🔥 地道表达")

    # === Tab 3: 解析 (Analysis) ===
    with tab3:
        st.subheader("深度逐句解析 (Deep Analysis)")
        for item in data["analysis"]:
            st.markdown(f"#### {item['sentence']}")
            st.markdown(f"**翻译**: {item['translation']}")
            st.info(f"{item['grammar']}")  # 使用蓝色信息框高亮解析
            st.markdown("---")

else:
    st.info("👈 请在左侧调整设置并点击 '生成文章'。")
    st.markdown("""
    ### 功能特点：
    1. **口语对话**：包含大量 Slang (如 *ghosting*, *rip-off*)。
    2. **新闻日报**：标准的 General English，结构清晰。
    3. **学术文章**：模仿真人学者风格，包含隐喻与节奏变化。
    """)