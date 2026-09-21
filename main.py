# --------------------------------------------------
# 그래프 2 - 일관객 합계 상위 5편의 날짜별 변화
# --------------------------------------------------
st.header("2. 일관객 합계 상위 5편의 날짜별 변화")

st.write(
    "전체 기간의 일관객 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

# 상위 5편의 영화명만 추출
top5_movie_names = top5_movies["영화명"].tolist()

# 상위 5편의 날짜별 데이터만 추출
top5_df = (
    df[df["영화명"].isin(top5_movie_names)]
    .sort_values(["영화명", "날짜"])
    .copy()
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,",
    },
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
    yaxis_title="일관객 수 (명)",
    legend_title="영화",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.info(
    "이 그래프로 알 수 있는 것: 전체 기간의 일관객 합계가 큰 영화 5편이 "
    "날짜에 따라 어떤 관객 추이를 보였는지 비교할 수 있습니다."
)


# --------------------------------------------------
# 그래프 3
# --------------------------------------------------
st.header("3. 다음 그래프")

st.caption("앞으로 새로운 그래프를 추가할 수 있는 영역입니다.")

# 여기에 세 번째 그래프를 추가하세요.
