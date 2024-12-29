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




















