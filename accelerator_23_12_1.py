import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import os

# NanumGothic-Regular 폰트를 동적으로 다운로드 및 설정
@st.cache_resource
def get_font_path():
    font_url = "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic-Regular.ttf?raw=true"
    font_path = "./NanumGothic-Regular.ttf"
    if not os.path.exists(font_path):
        # 폰트 다운로드
        import urllib.request
        urllib.request.urlretrieve(font_url, font_path)
    return font_path

# 폰트 설정
font_path = get_font_path()
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
matplotlib.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

# 데이터 파일 경로
DATA_PATH = "accelerator_23_12_1.csv"

# Streamlit 앱 구성
def main():
    st.set_page_config(layout="wide")  # 페이지 레이아웃 설정

    st.title("대한민국 액셀러레이터 데이터")
    st.write("2023년 12월말 기준, 초기투자액셀러레이터협회 직원만 확인할 수 있습니다.")

    # 데이터 업로드
    uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # 거래년도 열 생성
        if "거래금액" in data.columns:
            data["거래금액"] = pd.to_numeric(data["거래금액"], errors="coerce")  # 숫자로 변환
        if "거래년도" not in data.columns:
            data["거래년도"] = pd.to_datetime(data["조합ID"].str[:4], format="%Y", errors="coerce").dt.year

        # 거래건수 및 투자기업 수 계산 (사업자등록번호 기준)
        if "사업자등록번호" in data.columns:
            data["사업자등록번호"] = data["사업자등록번호"].astype(str)  # 문자열로 변환

        st.header("샘플 데이터")
        st.write(data.head())  # 데이터 확인

        # 간단한 예시 그래프
        if "거래년도" in data.columns and "거래금액" in data.columns:
            yearly_data = data.groupby("거래년도")["거래금액"].sum().reset_index()
            plt.figure(figsize=(10, 6))
            plt.plot(yearly_data["거래년도"], yearly_data["거래금액"], marker="o")
            plt.title("연도별 거래금액")
            plt.xlabel("거래년도")
            plt.ylabel("거래금액")
            plt.grid(True)
            st.pyplot(plt)

    else:
        st.write("데이터 파일을 업로드해주세요.")

if __name__ == "__main__":
    main()
















