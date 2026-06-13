from __future__ import annotations

from datetime import date

import streamlit as st
from dotenv import load_dotenv

from shared.database.repository import get_daily_report
from shared.database.schema import init_db
from shared.tools.chat_router import ChatRouter
from shared.tools.formatters import format_daily_summary, int_value, money


load_dotenv()
init_db()


st.set_page_config(
    page_title="老板娘经营助手",
    page_icon="美",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 720px;
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    h1 {
        font-size: 1.7rem !important;
        line-height: 1.25 !important;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 12px;
    }
    .metric-card {
        border: 1px solid #e6e1d8;
        border-radius: 10px;
        padding: 0.75rem;
        background: #fffdf8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_router() -> ChatRouter:
    return ChatRouter()


router = get_router()

st.title("老板娘经营助手")
st.caption("像发微信一样记录经营、看数据、做活动文案、问经营建议。")

tabs = st.tabs(["聊天", "今日数据", "活动文案"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "你可以直接输入：今天来了8个客人收入3200新客4个老客4个",
        }
    ]

if "latest_content" not in st.session_state:
    st.session_state.latest_content = ""

with tabs[0]:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("输入今天数据、查看今天数据、帮我做七夕活动...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        result = router.handle(prompt)
        reply = result["reply"]
        if result["intent"] == "marketing":
            st.session_state.latest_content = reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

with tabs[1]:
    report = get_daily_report(date.today())
    st.subheader("今日数据")
    st.write(format_daily_summary(report))

    if report:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div class='metric-card'><b>营业额</b><br>{money(report.get('revenue'))}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("")
            st.markdown(
                f"<div class='metric-card'><b>新客数</b><br>{int_value(report.get('new_customers'))}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<div class='metric-card'><b>客户数</b><br>{int_value(report.get('customers'))}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("")
            st.markdown(
                f"<div class='metric-card'><b>老客数</b><br>{int_value(report.get('returning_customers'))}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("还没有今日数据。回到聊天页输入：今天来了8个客人收入3200。")

with tabs[2]:
    st.subheader("最近生成的活动文案")
    if st.session_state.latest_content:
        st.write(st.session_state.latest_content)
    else:
        st.info("回到聊天页输入：帮我做七夕活动。")
