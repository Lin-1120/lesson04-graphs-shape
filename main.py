import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화들의 데이터를 그래프로 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

try:
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 데이터 전처리
# --------------------------------------------------

# genre에 여러 장르가 들어 있는 경우 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("기타")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 빈 장르는 기타로 처리
df.loc[
    df["genre_first"].isin(["", "nan", "None"]),
    "genre_first"
] = "기타"


# --------------------------------------------------
# 첫 번째 그래프
# --------------------------------------------------
st.divider()

st.subheader("📊 그래프 1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

total_movies = genre_counts["영화 편수"].sum()

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    margin=dict(t=70, b=30, l=30, r=30),
    legend_title_text="장르"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# 그래프로 알 수 있는 것
# --------------------------------------------------
st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프를 통해 알 수 있는 내용을 적어 보세요."
)


# --------------------------------------------------
# 데이터 간단히 확인
# --------------------------------------------------
with st.expander("📋 사용한 데이터 확인하기"):
    st.dataframe(
        df[
            [
                "movieCd",
                "movieNm",
                "openDt",
                "genre",
                "genre_first",
                "nation",
                "first_scrn",
                "first_show",
                "first_week_audi",
                "total_audi",
                "days_in_top10"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
