# --------------------------------------------------
# 그래프 4. 영화별 일관객 합계 TOP 10
# --------------------------------------------------

st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

# 영화별 일관객 합계와 10위권 진입 일수를 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        진입일수=("날짜", "nunique"),
    )
    .reset_index()
)

# 일관객 합계가 가장 큰 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .sort_values("일관객합계", ascending=True)
)

fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    text="일관객합계",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "일관객합계": "일관객 합계",
        "영화명": "영화",
    },
)

# 마우스를 올렸을 때 일관객 합계와 10위권 진입 일수 표시
fig4.update_traces(
    customdata=top10_movies[["진입일수"]].values,
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>일관객 합계: %{x:,}명"
        "<br>10위권 진입 일수: %{customdata[0]}일"
        "<extra></extra>"
    ),
    texttemplate="%{x:,}명",
    textposition="outside",
)

fig4.update_layout(
    xaxis=dict(
        tickformat=",",
        title="일관객 합계(명)",
    ),
    yaxis=dict(
        title="",
        categoryorder="total ascending",
    ),
    margin=dict(
        l=180,
        r=80,
        t=80,
        b=50,
    ),
)

st.plotly_chart(
    fig4,
    use_container_width=True,
)

st.markdown(
    "### 이 그래프로 알 수 있는 것"
)

st.info(
    "이 기간 동안 누적해서 가장 많은 관객을 모은 영화 10편과 각 영화가 10위권에 머문 날수를 비교할 수 있습니다."
)
