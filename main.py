import streamlit as st
import re

# ======================
# 페이지 설정
# ======================
st.set_page_config(page_title="생활기록부 자가 점검 & 바이트 계산기", layout="centered")
st.title("📘 생기부 self 점검 & 바이트 계산기")

st.markdown("""
한 번의 입력으로  
- 🧠맥락 기반 자동 분류+📏글자 수 & 바이트 수 계산🖍️생활기록부 구조 점검
""")

# ======================
# 바이트 기준 선택
# ======================
MAX_BYTES = st.selectbox(
    "📌 생활기록부 바이트 기준 선택",
    [500, 1000, 1500, 2000],
    index=2
)

# ======================
# 입력 (단 한 번)
# ======================
text = st.text_area(
    "✏️ 생활기록부 줄글 입력 (태그·줄바꿈 없어도 자동 분류)",
    height=260,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "교과서 p.132, 추가 자료를 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 바이트 계산 함수 (NEIS 기준)
# ======================
def calc_bytes(text):
    total = 0
    for ch in text:
        if ord(ch) <= 127:
            total += 1
        else:
            total += 3
    return total

# ======================
# 문장 분해 + 의미 기반 분류
# ======================
def classify_sentences(text):
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    result = {
        "행동": [],
        "동기": [],
        "결론": [],
        "참고": [],
        "느낀점": []
    }

    for s in sentences:
        if any(k in s for k in [
            "수업","설명","풀이","활동","발표","수행","보고서",
            "토론","시연","참여","제시","분석","적용"
        ]):
            result["행동"].append(s)

        elif any(k in s for k in [
            "때문","이유","어려워","필요","위해","위해서","문제"
        ]):
            result["동기"].append(s)

        elif any(k in s for k in [
            "향상","성장","능력","도출","결과","효과","결론","신장"
        ]):
            result["결론"].append(s)

        elif any(k in s for k in [
            "교과서","자료","논문","p.","페이지","도서"
        ]):
            result["참고"].append(s)

        else:
            result["느낀점"].append(s)

    return result

# ======================
# 실행 (입력 1번 → 결과 전체)
# ======================
if text.strip():
    st.divider()

    classified = classify_sentences(text)
    total_bytes = calc_bytes(text)
    total_chars = len(text)

    # ---------- 전체 요약 ----------
    st.subheader("📊 전체 요약")

    col1, col2, col3 = st.columns(3)
    col1.metric("글자 수", f"{total_chars} 자")
    col2.metric("바이트 수", f"{total_bytes} byte")
    col3.metric("기준", f"{MAX_BYTES} byte")

    st.progress(min(total_bytes / MAX_BYTES, 1.0))

    if total_bytes < MAX_BYTES:
        st.success(f"✅ {MAX_BYTES - total_bytes} byte 남았습니다.")
    elif total_bytes == MAX_BYTES:
        st.warning("⚠️ 기준 바이트에 정확히 도달했습니다.")
    else:
        st.error(f"❌ {total_bytes - MAX_BYTES} byte 초과했습니다.")

    st.divider()

    # ---------- 분류 결과 ----------
    st.subheader("🧠 맥락 기반 자동 분류")

    icons = {
        "행동": "🔵 [행동]",
        "동기": "🔴 [동기]",
        "결론": "🟢 [결론]",
        "참고": "🟣 [참고]",
        "느낀점": "🟠 [느낀점]"
    }

    for key in ["행동", "동기", "결론", "참고", "느낀점"]:
        if classified[key]:
            content = ". ".join(classified[key]) + "."
            st.markdown(f"**{icons[key]}** {content}")
            st.caption(f"➡️ 글자 수: {len(content)}자 | 바이트 수: {calc_bytes(content)} byte")

    st.divider()

    # ---------- 최종 하이라이트 문장 ----------
    st.subheader("🖍️ 분류 후 전체 문장")

    for key in ["행동", "동기", "결론", "참고", "느낀점"]:
        if classified[key]:
            st.write(f"{icons[key]} " + " ".join(classified[key]))




st.markdown(
    "<hr style='margin-top:40px'>"
    "<p style='text-align:center; color:gray; font-size:14px;'>"
    "🛠️ made by 서재원"
    "</p>",
    unsafe_allow_html=True
)

