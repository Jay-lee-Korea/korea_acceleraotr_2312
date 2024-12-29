import streamlit as st
import pandas as pd
import altair as alt

# 데이터 파일 경로
DATA_PATH = "accelerator_23_12_1.csv"

# 데이터 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

# 메인 페이지
def main():
    st.set_page_config(layout="wide")  # Wide 레이아웃 설정

    st.title("대한민국 액셀러레이터 데이터")
    st.write("2023년 12월말 기준, 초기투자액셀러레이터협회 직원만 확인할 수 있습니다.")

    # 데이터 로드
    data = load_data()

    # 데이터 전처리
    if "거래금액" in data.columns:
        data["거래금액"] = pd.to_numeric(data["거래금액"], errors="coerce")  # 숫자로 변환
    if "거래년도" not in data.columns:
        data["거래년도"] = pd.to_datetime(data["조합ID"].str[:4], format="%Y", errors="coerce").dt.year
    if "사업자등록번호" in data.columns:
        data["사업자등록번호"] = data["사업자등록번호"].astype(str)  # 문자열로 변환

    col1, col2, col3 = st.columns([1.5, 5, 1.5])  # 좌측 대시보드, 중앙 시각화, 우측 데이터 테이블

    with col1:
        st.header("대시보드")

        # 시각화할 데이터 선택
        metric = st.radio("시각화할 데이터:", ["거래금액", "거래건수", "투자기업 수"])

        # 운용기관 선택
        selected_operator = st.selectbox(
            "운용기관명 선택:", options=["전체"] + list(data["운용기관명"].dropna().unique())
        )

        # 운용기관 지역 선택
        selected_region = st.selectbox(
            "운용기관 지역 선택:", options=["전체"] + list(data["지역(운용사)"].dropna().unique())
        )

        # 업종 선택
        selected_industry = st.selectbox(
            "운용기관이 투자한 업종:", options=["전체"] + list(data["업종대분류(VC기준)"].dropna().unique())
        )

    with col2:
        st.header("데이터 시각화")

        # 데이터 필터링
        filtered_data = data
        if selected_operator != "전체":
            filtered_data = filtered_data[filtered_data["운용기관명"] == selected_operator]
        if selected_region != "전체":
            filtered_data = filtered_data[filtered_data["지역(운용사)"] == selected_region]
        if selected_industry != "전체":
            filtered_data = filtered_data[filtered_data["업종대분류(VC기준)"] == selected_industry]

        # 연도 범위 추가 (2017년부터 2023년까지)
        all_years = pd.DataFrame({"거래년도": range(2017, 2024)})

        if metric == "거래금액":
            yearly_total = filtered_data.groupby("거래년도")["거래금액"].sum().reset_index()
            yearly_total = pd.merge(all_years, yearly_total, on="거래년도", how="left").fillna(0)
            yearly_total["거래금액"] = yearly_total["거래금액"] / 100000000  # 억 원 단위
            yearly_total["거래금액"] = yearly_total["거래금액"].round(1)

            chart = (
                alt.Chart(yearly_total)
                .mark_line(point=True)
                .encode(
                    x=alt.X("거래년도:O", title="거래년도"),
                    y=alt.Y("거래금액:Q", title="거래금액 (억 원)"),
                    tooltip=["거래년도", "거래금액"],
                )
                .properties(width=800, height=400, title="연도별 거래금액 (억 원)")
            )
            st.altair_chart(chart, use_container_width=True)

        elif metric == "거래건수":
            yearly_count = filtered_data.groupby("거래년도").size().reset_index(name="거래건수")
            yearly_count = pd.merge(all_years, yearly_count, on="거래년도", how="left").fillna(0)

            chart = (
                alt.Chart(yearly_count)
                .mark_line(point=True)
                .encode(
                    x=alt.X("거래년도:O", title="거래년도"),
                    y=alt.Y("거래건수:Q", title="거래건수"),
                    tooltip=["거래년도", "거래건수"],
                )
                .properties(width=800, height=400, title="연도별 거래건수")
            )
            st.altair_chart(chart, use_container_width=True)

        elif metric == "투자기업 수":
            yearly_unique_count = (
                filtered_data.groupby("거래년도")["사업자등록번호"].nunique().reset_index()
            )
            yearly_unique_count.rename(columns={"사업자등록번호": "투자기업 수"}, inplace=True)
            yearly_unique_count = pd.merge(all_years, yearly_unique_count, on="거래년도", how="left").fillna(0)

            chart = (
                alt.Chart(yearly_unique_count)
                .mark_line(point=True)
                .encode(
                    x=alt.X("거래년도:O", title="거래년도"),
                    y=alt.Y("투자기업 수:Q", title="투자기업 수"),
                    tooltip=["거래년도", "투자기업 수"],
                )
                .properties(width=800, height=400, title="연도별 투자기업 수")
            )
            st.altair_chart(chart, use_container_width=True)

    with col3:
        st.header("데이터 테이블")

        if metric == "거래금액":
            st.write(yearly_total)
        elif metric == "거래건수":
            st.write(yearly_count)
        elif metric == "투자기업 수":
            st.write(yearly_unique_count)


if __name__ == "__main__":
    main()





















