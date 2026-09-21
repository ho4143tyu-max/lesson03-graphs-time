import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)

df = pd.read_csv(DATA_URL)

# 날짜: 하이픈 없는 8자리 숫자 → 실제 날짜형
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d",
)

# 숫자형 열 변환
numeric_columns = [
    "순위",
    "영화코드",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )


# --------------------------------------------------
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# --------------------------------------------------

st.header("1. 영화별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
    title=f"「{selected_movie}」의 날짜별 일관객 변화",
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d",
    ),
    yaxis=dict(
        tickformat=",",
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "선택한 영화의 일별 관객 수가 시간에 따라 어떻게 증가하거나 감소했는지 확인할 수 있습니다."
)


# --------------------------------------------------
# 그래프 2. 기간 전체 일관객 합계 TOP 5
# --------------------------------------------------

st.divider()

st.header("2. 일관객 합계가 가장 큰 영화 5편")

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

# 상위 5편의 영화명만 추출
top5_movie_names = top5_movies["영화명"].tolist()

# 상위 5편의 날짜별 데이터
top5_df = (
    df[df["영화명"].isin(top5_movie_names)]
    .sort_values(["날짜", "영화명"])
    .copy()
)

fig_top5 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
    title="이 기간 일관객 합계 TOP 5 영화의 날짜별 일관객",
)

fig_top5.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig_top5.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d",
    ),
    yaxis=dict(
        tickformat=",",
    ),
    legend=dict(
        title="영화",
    ),
)

st.plotly_chart(
    fig_top5,
    use_container_width=True,
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "전체 기간 동안 일관객 합계가 가장 큰 5편의 흥행 추이를 날짜별로 비교할 수 있습니다."
)


# --------------------------------------------------
# 앞으로 추가할 그래프 영역
# --------------------------------------------------

st.divider()

st.header("3. 다음 그래프")

st.info(
    "앞으로 추가할 그래프를 이 구역에 넣습니다."
)


st.divider()

st.header("4. 다음 그래프")

st.info(
    "앞으로 추가할 그래프를 이 구역에 넣습니다."
)


st.divider()

st.header("5. 다음 그래프")

st.info(
    "앞으로 추가할 그래프를 이 구역에 넣습니다."
)
