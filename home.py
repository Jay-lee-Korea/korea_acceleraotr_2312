import streamlit as st

st.set_page_config(page_title="멀티페이지 앱", layout="wide")

st.title("멀티페이지 Streamlit 앱")
st.write("왼쪽 사이드바를 통해 페이지를 선택하세요.")

import streamlit as st
import pandas as pd
import altair as alt

# 데이터 파일 경로
DATA_PATH = "accelerator_23_12_1.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

st.set_page_config(page_title="페이지 1", layout="wide")

st.title("대한민국 액셀러레이터 데이터 - 페이지 1")
st.write("2023년 12월말 기준, 초기투자액셀러레이터협회 직원만 확인할 수 있습니다.")

data = load_data()

# 거래년도 열 생성
if "거래금액" in data.columns:
    data["거래금액"] = pd.to_numeric(data["거래금액"], errors="coerce")  # 숫자로 변환
if "거래년도" not in data.columns:
    data["거래년도"] = pd.to_datetime(data["조합ID"].str[:4], format="%Y", errors="coerce").dt.year

# 거래건수 및 투자기업 수 계산
if "사업자등록번호" in data.columns:
    data["사업자등록번호"] = data["사업자등록번호"].astype(str)

col1, col2, col3 = st.columns([1.5, 5, 1.5])

with col1:
    st.header("대시보드")
    metric = st.radio("시각화할 데이터:", ["거래금액", "거래건수", "투자기업 수"])
    selected_operator = st.selectbox("운용기관명 선택:", ["전체"] + list(data["운용기관명"].dropna().unique()))
    selected_region = st.selectbox("운용기관 지역 선택:", ["전체"] + list(data["지역(운용사)"].dropna().unique()))

with col2:
    st.header("데이터 시각화")
    st.write("선택된 데이터 시각화를 구현하세요.")

with col3:
    st.header("데이터 테이블")
    st.write("선택된 데이터 테이블을 보여줍니다.")

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


















