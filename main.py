import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("KOBIS 일별 박스오피스 데이터를 활용해 영화의 시간에 따른 변화를 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
st.subheader("데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 기록 수", f"{len(df):,}개")

with col2:
    st.metric("기록된 영화 수", f"{df['영화명'].nunique():,}편")

with col3:
    st.metric(
        "데이터 기간",
        f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
        f"{df['날짜'].max().strftime('%Y-%m-%d')}"
    )


# ==================================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# ==================================================
st.divider()
st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 개봉 이후 영화의 일관객 수가 어떻게 변화하는지 알 수 있다.",
    key="graph1_comment"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================

st.divider()
st.header("그래프 2")
st.info("앞으로 추가할 그래프 영역입니다.")
# ==================================================
# 그래프 2. 일관객 합계 TOP 5 영화의 날짜별 일관객
# ==================================================
st.divider()
st.header("그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화")

# 영화별 일관객 합계를 계산하여 TOP 5 선정
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

# TOP 5 영화만 추출
top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])

# 날짜별로 영화별 일관객을 한 그래프에 표시
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 일관객 합계가 가장 큰 5편의 날짜별 관객 수 변화를 비교할 수 있다.",
    key="graph2_comment"
)
st.divider()
st.header("그래프 3")
st.info("앞으로 추가할 그래프 영역입니다.")
# ==================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ==================================================
st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 일관객 합계 계산
daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날짜 3일
top3_days = (
    daily_audience
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프
fig3 = px.area(
    daily_audience,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,"
    }
)

# 전체 날짜별 값의 마우스 오버
fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 가장 관객이 많았던 3일 표시
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"<b>{row['날짜'].strftime('%m월 %d일')}</b>"
            f"<br>{row['일관객']:,}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-55,
        font=dict(size=12)
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 날짜에 따라 박스오피스 10위권 전체의 관객 규모가 어떻게 변했는지 알 수 있다.",
    key="graph3_comment"
)
st.divider()
st.header("그래프 4")
st.info("앞으로 추가할 그래프 영역입니다.")
# ==================================================
# 그래프 4. 영화별 기간 일관객 TOP 10
# ==================================================
st.divider()
st.header("그래프 4. 영화별 기간 일관객 TOP 10")

# 영화별 일관객 합계와 10위권에 든 날수 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객=("일관객", "sum"),
        10위권_일수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계가 많은 TOP 10
top10_movies = (
    movie_summary
    .sort_values("기간_일관객", ascending=False)
    .head(10)
    .sort_values("기간_일관객", ascending=True)
)

# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="기간_일관객",
    y="영화명",
    orientation="h",
    title="영화별 기간 일관객 TOP 10",
    labels={
        "기간_일관객": "기간 일관객 합계",
        "영화명": "영화"
    },
    hover_data={
        "기간_일관객": ":,",
        "10위권_일수": True
    }
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "기간 일관객 합계: %{x:,}명<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계(명)",
    yaxis_title="영화",
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 이 기간 동안 누적된 일관객이 가장 많았던 영화와 10위권에 머문 기간을 비교할 수 있다.",
    key="graph4_comment"
)
st.divider()
st.header("그래프 5")
st.info("앞으로 추가할 그래프 영역입니다.")
# ==================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# ==================================================
st.divider()
st.header("그래프 5. 월 × 요일별 일관객 합계")

# 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(
    dict(enumerate(weekday_order))
)

# 월 × 요일별 일관객 합계
monthly_weekday = (
    heatmap_df
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)

# 피벗 테이블 생성
heatmap_pivot = monthly_weekday.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 월 순서 정렬
heatmap_pivot = heatmap_pivot.reindex(
    columns=weekday_order
)

heatmap_pivot = heatmap_pivot.sort_index()

# 히트맵
fig5 = px.imshow(
    heatmap_pivot,
    text_auto=".2s",
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    title="월 × 요일별 일관객 합계"
)

fig5.update_xaxes(
    categoryorder="array",
    categoryarray=weekday_order
)

fig5.update_yaxes(
    title="월",
    tickmode="array",
    tickvals=list(range(1, 13)),
    ticktext=[f"{i}월" for i in range(1, 13)]
)

fig5.update_layout(
    xaxis_title="요일",
    coloraxis_colorbar_title="일관객 합계"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 월과 요일에 따라 박스오피스 10위권의 일관객 합계가 어떻게 달라지는지 알 수 있다.",
    key="graph5_comment"
)
