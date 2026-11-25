import streamlit as st

cost = []
welfare = ["노인복지", "청년지원", "청소년지원"]


def allocate_budget(total_budget, score_list):
    allocated_list = []
    total_score = 0

    for score in score_list:
        total_score = total_score + score

    for score in score_list:
        if total_score > 0:
            ratio = score / total_score
            budget_amount = int(total_budget * ratio)
        else:
            budget_amount = 0
        allocated_list.append(budget_amount)

    return allocated_list


st.title("🏛️ 지역사회 복지 예산 분배 시스템")
st.write("총 예산을 입력하고 각 복지 분야의 필요도를 평가하여 예산을 배분합니다.")

if "saved_scores" not in st.session_state:
    st.session_state.saved_scores = [0, 0, 0]
if "is_completed" not in st.session_state:
    st.session_state.is_completed = [False, False, False]

input_budget = st.number_input(
    "1. 현재 총 복지 예산을 입력하세요 (원):",
    min_value=0,
    value=10000000,
    step=100000
)
cost.append(input_budget)

st.divider()

selected_field = st.selectbox("2. 평가할 복지 분야를 선택하세요:", welfare)
field_index = welfare.index(selected_field)

urgency_score = st.slider(
    f"3. '{selected_field}' 분야의 필요도를 선택하세요 (1~5점):",
    min_value=1,
    max_value=5,
    value=3
)

if st.button("비율로 계산하기"):
    st.session_state.saved_scores[field_index] = urgency_score
    st.session_state.is_completed[field_index] = True

    all_done = True
    for status in st.session_state.is_completed:
        if status == False:
            all_done = False

    if all_done:
        st.success("✅ 모든 복지 분야의 평가가 완료되었습니다!")

        final_budgets = allocate_budget(cost[0], st.session_state.saved_scores)

        result_message = (
            f"**{welfare[0]}**은(는) **{final_budgets[0]:,}원**, "
            f"**{welfare[1]}**은(는) **{final_budgets[1]:,}원**, "
            f"**{welfare[2]}**은(는) **{final_budgets[2]:,}원**이 필요합니다."
        )
        st.info(result_message)

        st.subheader("📊 분야별 필요 예산 목록")
        table_data = []
        for i in range(len(welfare)):
            row = {
                "복지분야": welfare[i],
                "필요도(1~5점)": f"{st.session_state.saved_scores[i]}점",
                "필요한 예산": f"{final_budgets[i]:,}원"
            }
            table_data.append(row)

        st.table(table_data)

    else:
        remaining_fields = []
        for i in range(len(welfare)):
            if st.session_state.is_completed[i] == False:
                remaining_fields.append(welfare[i])

        st.warning(
            f"'{selected_field}' 분야 점수가 저장되었습니다! "
            f"아직 입력하지 않은 분야({', '.join(remaining_fields)})를 위에서 다시 선택해 주세요."
        )

if st.button("입력 초기화"):
    st.session_state.saved_scores = [0, 0, 0]
    st.session_state.is_completed = [False, False, False]
    st.rerun()
