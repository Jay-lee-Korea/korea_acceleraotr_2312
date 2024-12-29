import streamlit as st
import pandas as pd
import altair as alt

# 데이터 파일 경로
DATA_PATH = "accelerator_23_12_1.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

st.set_page_config(page_title="페이지 2", layout="wide")

st.title("운용기관별 업종 투자 분포 - 페이지 2")
st.write("운용기관이 투자한 업종의 분포를 확인할 수 있습니다.")

data = load_data()

if "업종대분류(VC기준)" not in data.columns:
    st.error("데이터에 '업종대분류(VC기준)' 열이 없습니다.")
else:
    selected_operator = st.selectbox("운용기관명 선택:", ["전체"] + list(data["운용기관명"].dropna().unique()))
    filtered_data = data[data["운용기관명"] == selected_operator] if selected_operator != "전체" else data

    industry_counts = filtered_data["업종대분류(VC기준)"].value_counts().reset_index()
    industry_counts.columns = ["업종대분류", "건수"]

    if industry_counts.empty:
        st.warning("선택한 운용기관에 대한 업종 데이터가 없습니다.")
    else:
        st.subheader("업종별 투자 비중 (막대 그래프)")
        bar_chart = (
            alt.Chart(industry_counts)
            .mark_bar()
            .encode(
                x=alt.X("건수:Q", title="투자 건수"),
                y=alt.Y("업종대분류:N", title="업종대분류", sort="-x"),
                color=alt.Color("업종대분류:N", legend=None),
                tooltip=["업종대분류", "건수"],
            )
            .properties(width=800, height=400, title="업종별 투자 건수 분포")
        )
        st.altair_chart(bar_chart, use_container_width=True)





















