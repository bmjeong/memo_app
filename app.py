# from datetime import datetime

# import streamlit as st
# from supabase import create_client


# st.set_page_config(
#     page_title="내 메모장",
#     page_icon="📝",
#     layout="centered",
# )


# @st.cache_resource
# def get_supabase_client():
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)


# supabase = get_supabase_client()


# def add_note(title, content):
#     supabase.table("notes").insert(
#         {
#             "title": title,
#             "content": content,
#         }
#     ).execute()


# def get_notes():
#     result = (
#         supabase.table("notes")
#         .select("id, title, content, created_at")
#         .order("created_at", desc=True)
#         .execute()
#     )
#     return result.data


# def delete_note(note_id):
#     supabase.table("notes").delete().eq("id", note_id).execute()

# def check_password():
#     if "password_ok" not in st.session_state:
#         st.session_state.password_ok = False

#     if st.session_state.password_ok:
#         return True

#     password = st.text_input("비밀번호", type="password")

#     if st.button("로그인"):
#         if password == st.secrets["APP_PASSWORD"]:
#             st.session_state.password_ok = True
#             st.rerun()
#         else:
#             st.error("비밀번호가 틀렸습니다.")

#     return False


# if not check_password():
#     st.stop()

# st.title("📝 내 메모장")

# st.subheader("새 메모 작성")

# title = st.text_input("제목")
# content = st.text_area("내용", height=180)

# if st.button("저장"):
#     clean_title = title.strip()
#     clean_content = content.strip()

#     if not clean_title and not clean_content:
#         st.warning("제목이나 내용을 입력해 주세요.")
#     else:
#         add_note(
#             clean_title or "제목 없음",
#             clean_content,
#         )
#         st.success("메모가 저장되었습니다.")
#         st.rerun()

# st.divider()

# st.subheader("저장된 메모")

# try:
#     notes = get_notes()

#     if not notes:
#         st.info("아직 저장된 메모가 없습니다.")
#     else:
#         for note in notes:
#             note_id = note["id"]
#             note_title = note["title"]
#             note_content = note["content"]
#             created_at = note["created_at"]

#             with st.container(border=True):
#                 st.markdown(f"### {note_title}")
#                 st.caption(created_at)
#                 st.write(note_content)

#                 if st.button("삭제", key=f"delete_{note_id}"):
#                     delete_note(note_id)
#                     st.success("메모가 삭제되었습니다.")
#                     st.rerun()

# except Exception as e:
#     st.error("Supabase에서 메모를 불러오지 못했습니다.")
#     st.exception(e)

import streamlit as st
from datetime import date
from supabase import create_client
import base64
from pathlib import Path

import base64
import random

import pandas as pd
from datetime import date

OTTER_MESSAGES = [
    "수고했어! 👏",
    "정말 잘했어! 🌟",
    "멋져! 👍",
    "하나 더 해냈네! 😊",
    "최고야! 🥳",
    "오늘도 열심히 했구나! 💛",
]


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def show_otter_header(message: str = "오늘 할 일을 시작해 볼까?"):
    otter_base64 = image_to_base64("assets/otter_face.png")

    st.markdown(
        f"""
        <style>
        .otter-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 18px;
            margin: 5px 0 25px 0;
        }}

        .otter-image {{
            width: 115px;
            height: 115px;
            object-fit: contain;
        }}

        .speech-bubble {{
            position: relative;
            background: #ffffff;
            border: 4px solid #222222;
            border-radius: 24px;
            padding: 14px 22px;
            min-width: 150px;
            max-width: 280px;
            text-align: center;
            font-size: 21px;
            font-weight: 700;
            color: #333333;
            box-shadow: 4px 5px 0 rgba(0, 0, 0, 0.12);
            animation: bubble-pop 0.25s ease-out;
        }}

        .speech-bubble::before {{
            content: "";
            position: absolute;
            left: -20px;
            top: 46px;
            border-width: 12px 20px 12px 0;
            border-style: solid;
            border-color: transparent #222222 transparent transparent;
        }}

        .speech-bubble::after {{
            content: "";
            position: absolute;
            left: -13px;
            top: 49px;
            border-width: 9px 16px 9px 0;
            border-style: solid;
            border-color: transparent #ffffff transparent transparent;
        }}

        @keyframes bubble-pop {{
            0% {{
                transform: scale(0.85);
                opacity: 0;
            }}
            100% {{
                transform: scale(1);
                opacity: 1;
            }}
        }}

        @media (max-width: 600px) {{
            .otter-header {{
                gap: 10px;
            }}

            .otter-image {{
                width: 85px;
                height: 85px;
            }}

            .speech-bubble {{
                font-size: 17px;
                padding: 11px 15px;
                max-width: 210px;
            }}

            .speech-bubble::before {{
                top: 32px;
            }}

            .speech-bubble::after {{
                top: 35px;
            }}
        }}
        </style>

        <div class="otter-header">
            <img
                class="otter-image"
                src="data:image/png;base64,{otter_base64}"
            >
            <div class="speech-bubble">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def add_otter_background():
    otter_path = Path("images/otter.png")

    if not otter_path.exists():
        st.warning("수달 이미지 파일을 찾을 수 없습니다: images/otter.png")
        return

    encoded = base64.b64encode(otter_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        .otter-bg {{
            position: fixed;
            left: -160px;
            bottom: 40px;
            width: 130px;
            height: 130px;
            background-image: url("data:image/png;base64,{encoded}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.22;
            z-index: 0;
            pointer-events: none;
            animation: otter-walk 18s linear infinite;
        }}

        @keyframes otter-walk {{
            0% {{
                transform: translateX(-160px) scaleX(1);
            }}
            45% {{
                transform: translateX(calc(100vw + 160px)) scaleX(1);
            }}
            50% {{
                transform: translateX(calc(100vw + 160px)) scaleX(-1);
            }}
            95% {{
                transform: translateX(-160px) scaleX(-1);
            }}
            100% {{
                transform: translateX(-160px) scaleX(1);
            }}
        }}

        .block-container {{
            position: relative;
            z-index: 2;
        }}
        </style>

        <div class="otter-bg"></div>
        """,
        unsafe_allow_html=True,
    )

def load_checklist_templates():
    """
    자주 사용하는 체크리스트 항목을 불러옵니다.
    """
    try:
        response = (
            supabase.table("checklist_templates")
            .select("*")
            .order("category", desc=False)
            .order("description", desc=False)
            .execute()
        )

        return response.data or []

    except Exception as e:
        st.error(f"자주 쓰는 항목을 불러오지 못했습니다: {e}")
        return []

# =========================
# Supabase 연결
# =========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# 앱 비밀번호 확인
# =========================
def password_gate():
    if "password_ok" not in st.session_state:
        st.session_state["password_ok"] = False

    if st.session_state["password_ok"]:
        return True

    st.title("체크리스트 앱")

    password = st.text_input("앱 비밀번호", type="password")

    if st.button("입장"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state["password_ok"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")

    return False

# =========================
# 역할 선택 화면
# =========================
def role_select_screen():
    st.title("누가 사용할까요?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("관리자", use_container_width=True):
            st.session_state["role"] = "admin"
            st.rerun()

    with col2:
        if st.button("율하", use_container_width=True):
            st.session_state["role"] = "율하"
            st.rerun()

    with col3:
        if st.button("서하", use_container_width=True):
            st.session_state["role"] = "서하"
            st.rerun()

def back_to_role_select():
    if st.button("처음 화면으로"):
        if "role" in st.session_state:
            del st.session_state["role"]
        st.rerun()


# =========================
# 관리자 화면
# =========================
def admin_screen():
    st.title("관리자 화면")
    back_to_role_select()

    st.divider()

    categories = ["공부", "독서", "생활", "운동", "집안일", "기타"]

    # --------------------------------------------------
    # 1. 자주 쓰는 항목 관리
    # --------------------------------------------------
    st.subheader("자주 쓰는 항목 관리")

    try:
        templates = (
            supabase.table("checklist_templates")
            .select("*")
            .order("category", desc=False)
            .order("description", desc=False)
            .execute()
            .data
        ) or []

    except Exception as e:
        st.error(f"자주 쓰는 항목 조회 오류: {e}")
        templates = []

    with st.expander("자주 쓰는 항목 등록", expanded=False):
        template_category = st.selectbox(
            "분류",
            categories,
            key="template_category"
        )

        template_description = st.text_input(
            "설명",
            key="template_description",
            placeholder="예: 수학 문제집 2쪽 풀기"
        )

        template_point = st.number_input(
            "점수",
            min_value=0,
            max_value=100,
            value=1,
            step=1,
            key="template_point"
        )

        if st.button(
            "자주 쓰는 항목 등록",
            key="add_template",
            use_container_width=True
        ):
            if not template_description.strip():
                st.warning("설명을 입력하세요.")

            else:
                try:
                    supabase.table("checklist_templates").insert({
                        "category": template_category,
                        "description": template_description.strip(),
                        "point": int(template_point),
                    }).execute()

                    st.success("자주 쓰는 항목으로 등록되었습니다.")
                    st.rerun()

                except Exception as e:
                    if "duplicate" in str(e).lower():
                        st.warning("이미 등록된 항목입니다.")
                    else:
                        st.error(f"등록 오류: {e}")

        if templates:
            st.divider()
            st.caption("등록된 자주 쓰는 항목")

            for template in templates:
                col1, col2 = st.columns([6, 1])

                with col1:
                    st.write(
                        f"**[{template['category']}] "
                        f"{template['description']} "
                        f"({template['point']}점)**"
                    )

                with col2:
                    if st.button(
                        "삭제",
                        key=f"delete_template_{template['id']}",
                        use_container_width=True
                    ):
                        try:
                            (
                                supabase.table("checklist_templates")
                                .delete()
                                .eq("id", template["id"])
                                .execute()
                            )

                            st.rerun()

                        except Exception as e:
                            st.error(f"삭제 오류: {e}")

        else:
            st.info("등록된 자주 쓰는 항목이 없습니다.")

    st.divider()

    # --------------------------------------------------
    # 2. 체크리스트 만들기
    # --------------------------------------------------
    st.subheader("체크리스트 만들기")

    target_date = st.date_input(
        "체크리스트 날짜",
        value=date.today(),
        key="admin_target_date"
    )

    child_name = st.selectbox(
        "누구의 체크리스트인가요?",
        ["율하", "서하"],
        key="admin_child_name"
    )

    # 드롭다운 표시용 항목 구성
    template_labels = ["직접 입력"]
    template_map = {}

    for template in templates:
        label = (
            f"[{template['category']}] "
            f"{template['description']} "
            f"({template['point']}점)"
        )

        template_labels.append(label)
        template_map[label] = template

    selected_template_label = st.selectbox(
        "자주 쓰는 항목 선택",
        template_labels,
        key="admin_selected_template"
    )

    selected_template = template_map.get(selected_template_label)

    # 선택된 템플릿에 따라 위젯 key 변경
    # key가 바뀌면 선택 항목의 기본값이 즉시 적용됨
    if selected_template:
        template_key = str(selected_template["id"])
        default_category = selected_template["category"]
        default_description = selected_template["description"]
        default_point = int(selected_template["point"])
    else:
        template_key = "direct"
        default_category = "공부"
        default_description = ""
        default_point = 1

    if default_category not in categories:
        default_category = "기타"

    category = st.selectbox(
        "분류",
        categories,
        index=categories.index(default_category),
        key=f"checklist_category_{template_key}"
    )

    description = st.text_input(
        "설명",
        value=default_description,
        key=f"checklist_description_{template_key}",
        placeholder="체크리스트 설명을 입력하세요."
    )

    point = st.number_input(
        "점수",
        min_value=0,
        max_value=100,
        value=default_point,
        step=1,
        key=f"checklist_point_{template_key}"
    )

    if st.button(
        "추가하기",
        type="primary",
        use_container_width=True,
        key="add_checklist_item"
    ):
        if not description.strip():
            st.warning("설명을 입력하세요.")

        else:
            try:
                supabase.table("checklist_items").insert({
                    "child_name": child_name,
                    "category": category,
                    "description": description.strip(),
                    "point": int(point),
                    "target_date": str(target_date),
                    "is_active": True,
                }).execute()

                st.success("체크리스트가 추가되었습니다.")
                st.rerun()

            except Exception as e:
                st.error(f"체크리스트 추가 오류: {e}")

    st.divider()

    # --------------------------------------------------
    # 3. 등록된 체크리스트
    # --------------------------------------------------
    st.subheader("등록된 체크리스트")

    list_date = st.date_input(
        "조회 날짜",
        value=target_date,
        key="admin_list_date"
    )

    list_child = st.selectbox(
        "조회할 아이",
        ["전체", "율하", "서하"],
        key="admin_list_child"
    )

    try:
        query = (
            supabase.table("checklist_items")
            .select("*")
            .eq("target_date", str(list_date))
        )

        if list_child != "전체":
            query = query.eq("child_name", list_child)

        items = (
            query
            .order("child_name", desc=False)
            .order("category", desc=False)
            .order("created_at", desc=False)
            .execute()
            .data
        ) or []

    except Exception as e:
        st.error(f"체크리스트 조회 오류: {e}")
        items = []

    if not items:
        st.info(f"{list_date}에 등록된 체크리스트가 없습니다.")

    for item in items:
        with st.container(border=True):
            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                status = "사용 중" if item["is_active"] else "숨김"

                st.write(
                    f"**{item['child_name']} / "
                    f"{item['category']} / "
                    f"{item['point']}점**"
                )

                st.caption(
                    f"{item['description']} / {status}"
                )

            with col2:
                if item["is_active"]:
                    if st.button(
                        "숨김",
                        key=f"hide_{item['id']}",
                        use_container_width=True
                    ):
                        (
                            supabase.table("checklist_items")
                            .update({"is_active": False})
                            .eq("id", item["id"])
                            .execute()
                        )

                        st.rerun()

                else:
                    if st.button(
                        "복구",
                        key=f"show_{item['id']}",
                        use_container_width=True
                    ):
                        (
                            supabase.table("checklist_items")
                            .update({"is_active": True})
                            .eq("id", item["id"])
                            .execute()
                        )

                        st.rerun()

            with col3:
                if st.button(
                    "삭제",
                    key=f"delete_{item['id']}",
                    use_container_width=True
                ):
                    try:
                        (
                            supabase.table("checklist_items")
                            .delete()
                            .eq("id", item["id"])
                            .execute()
                        )

                        st.rerun()

                    except Exception as e:
                        st.error(f"삭제 오류: {e}")

    st.divider()

    # --------------------------------------------------
    # 4. 점수 현황
    # --------------------------------------------------
    st.subheader("점수 현황")

    score_col1, score_col2 = st.columns(2)

    with score_col1:
        total = calculate_total_score("율하")
        st.metric("율하", f"{total}점")

    with score_col2:
        total = calculate_total_score("서하")
        st.metric("서하", f"{total}점")

# =========================
# 아이 화면
# =========================
def child_screen(child_name):
    if child_name == "율하":
        show_otter_header()

    st.title(f"{child_name} 체크리스트")
    back_to_role_select()

    selected_date = st.date_input(
        "날짜",
        value=date.today(),
        key=f"selected_date_{child_name}"
    )

    st.divider()

    # -----------------------------------------
    # 1. 선택 날짜의 체크리스트만 조회
    # -----------------------------------------
    try:
        items = (
            supabase.table("checklist_items")
            .select("*")
            .eq("is_active", True)
            .eq("child_name", child_name)
            .eq("target_date", str(selected_date))
            .order("category", desc=False)
            .order("created_at", desc=False)
            .execute()
            .data
        )

    except Exception as e:
        st.error(f"체크리스트 조회 중 오류가 발생했습니다: {e}")
        return

    if not items:
        st.info(
            f"{selected_date}에 등록된 "
            f"{child_name} 체크리스트가 없습니다."
        )
        return

    # -----------------------------------------
    # 2. 선택 날짜의 기록을 한 번에 조회
    # -----------------------------------------
    item_ids = [item["id"] for item in items]

    try:
        records = (
            supabase.table("checklist_records")
            .select("*")
            .eq("child_name", child_name)
            .eq("record_date", str(selected_date))
            .in_("item_id", item_ids)
            .execute()
            .data
        )

    except Exception as e:
        st.error(f"기록 조회 중 오류가 발생했습니다: {e}")
        return

    # item_id를 key로 사용하는 사전
    record_map = {
        record["item_id"]: record
        for record in records
    }

    # -----------------------------------------
    # 3. 표에 표시할 데이터 생성
    # -----------------------------------------
    table_rows = []

    for item in items:
        record = record_map.get(item["id"])

        table_rows.append({
            "item_id": item["id"],
            "분류": item["category"],
            "설명": item["description"],
            "점수": int(item["point"]),
            "완료": bool(record["is_done"]) if record else False,
            "메모": (record.get("memo") or "") if record else "",
        })

    checklist_df = pd.DataFrame(table_rows)

    st.caption(
        "완료 여부와 메모를 작성한 뒤 "
        "아래의 전체 저장 버튼을 눌러 주세요."
    )

    # -----------------------------------------
    # 4. 모바일에서도 한 표로 유지되는 편집기
    # -----------------------------------------
    edited_df = st.data_editor(
        checklist_df,
        key=f"checklist_editor_{child_name}_{selected_date}",
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        disabled=[
            "item_id",
            "분류",
            "설명",
            "점수",
        ],
        column_config={
            "item_id": None,

            "분류": st.column_config.TextColumn(
                "분류",
                width="small"
            ),

            "설명": st.column_config.TextColumn(
                "설명",
                width="large"
            ),

            "점수": st.column_config.NumberColumn(
                "점수",
                width="small",
                format="%d점"
            ),

            "완료": st.column_config.CheckboxColumn(
                "체크",
                width="small",
                default=False
            ),

            "메모": st.column_config.TextColumn(
                "메모",
                width="large"
            ),
        }
    )

    # -----------------------------------------
    # 5. 편집된 표 기준 오늘 점수 계산
    # -----------------------------------------
    today_score = int(
        edited_df.loc[
            edited_df["완료"] == True,
            "점수"
        ].sum()
    )

    st.metric(
        f"{selected_date} 점수",
        f"{today_score}점"
    )

    # -----------------------------------------
    # 6. 모든 행을 한 번에 저장
    # -----------------------------------------
    if st.button(
        "전체 저장",
        type="primary",
        use_container_width=True
    ):
        save_rows = []

        for _, row in edited_df.iterrows():
            memo_value = row["메모"]

            if pd.isna(memo_value):
                memo_value = ""

            save_rows.append({
                "child_name": child_name,
                "item_id": row["item_id"],
                "record_date": str(selected_date),
                "is_done": bool(row["완료"]),
                "memo": str(memo_value).strip(),
            })

        try:
            # unique 제약조건:
            # child_name, item_id, record_date
            supabase.table("checklist_records").upsert(
                save_rows,
                on_conflict="child_name,item_id,record_date"
            ).execute()

            if child_name == "율하" and today_score > 0:
                st.session_state.otter_message = (
                    "오늘도 정말 잘했어!"
                )

            st.success("체크리스트가 저장되었습니다.")
            st.rerun()

        except Exception as e:
            st.error(f"저장 중 오류가 발생했습니다: {e}")

    st.divider()

    total_score = calculate_total_score(child_name)

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "선택 날짜 점수",
            f"{today_score}점"
        )

    with metric_col2:
        st.metric(
            "누적 점수",
            f"{total_score}점"
        )

# =========================
# 점수 계산
# =========================
def calculate_total_score(child_name):
    records = (
        supabase.table("checklist_records")
        .select("is_done, checklist_items(point)")
        .eq("child_name", child_name)
        .eq("is_done", True)
        .execute()
        .data
    )

    total = 0

    for record in records:
        item = record.get("checklist_items")
        if item:
            total += item.get("point", 0)

    return total


# =========================
# 메인
# =========================
def main():
    st.set_page_config(
        page_title="체크리스트 앱",
        page_icon="✅",
        layout="centered"
    )

    if not password_gate():
        return

    if "role" not in st.session_state:
        role_select_screen()
        return

    role = st.session_state["role"]

    if role == "admin":
        admin_screen()
    elif role in ["율하", "서하"]:
        child_screen(role)
    else:
        st.error("잘못된 사용자입니다.")
        del st.session_state["role"]
        st.rerun()


if __name__ == "__main__":
    main()