import copy
import random
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="DACOM",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CURRENT_USER = "혜주"
DM_CANDIDATES = ["민서", "준호", "수빈", "지우", "하린"]

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3.4rem !important;
        padding-bottom: 2.5rem;
        max-width: 1180px;
    }
    header[data-testid="stHeader"] {height: 3.2rem;}
    section.main > div {padding-top: 0.9rem;}
    .stApp {background: #f4f7fb;}

    div[data-testid="stButton"] > button {
        min-height: 46px;
        white-space: nowrap;
        border-radius: 16px;
        border: 1px solid #d7deea;
        background: #ffffff;
        color: #1f2937;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.04);
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #7aa9ff;
        color: #214fbd;
    }

    .logo-text {
        font-size: 2.05rem;
        font-weight: 800;
        color: #2563eb;
        line-height: 1.15;
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
        letter-spacing: -0.02em;
    }
    .logo-sub {
        font-size: 0.92rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    .hero-card {
        background: linear-gradient(135deg, #8fc2f5 0%, #6d7ee8 58%, #4f46e5 100%);
        color: white;
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 18px 36px rgba(79, 70, 229, 0.18);
        margin-bottom: 12px;
    }

    .scenario-box {
        background: #ffffff;
        border: 1px solid #dbe5f3;
        border-radius: 20px;
        padding: 18px;
        margin-top: 8px;
        margin-bottom: 14px;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.05);
    }

    .chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid #d6e4ff;
        background: #eef4ff;
        color: #315db8;
    }

    .status-open, .status-live, .status-accepted, .status-submitted {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .status-closed, .status-ended, .status-rejected {
        display: inline-block;
        background: #e5e7eb;
        color: #4b5563;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .status-upcoming {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .status-pending {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }

    .msg-box {
        background: #ffffff;
        border: 1px solid #dbe5f3;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 8px;
    }
    .msg-me {border-left: 4px solid #4f46e5;}
    .msg-other {border-left: 4px solid #93c5fd;}
    </style>
    """,
    unsafe_allow_html=True,
)

INITIAL_HACKATHONS = [
    {
        "slug": "emergency-handover-docs",
        "title": "긴급 인수인계 해커톤 - 문서만 남기고 사라졌다",
        "status": "진행중",
        "tags": ["AI", "협업", "문서자동화"],
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "participants": 128,
        "overview": "긴급 인수인계 문서를 더 빠르고 정확하게 만드는 협업형 해커톤입니다.",
        "summary": "예시 문서 자료를 바탕으로 바이브 코딩으로 웹서비스를 구현하고 제출하는 해커톤",
        "guide": "제출 전 서비스 플로우, 팀 협업 방식, 사용 시나리오가 분명히 드러나야 합니다. 제출 파일은 zip, pdf, csv를 지원합니다.",
        "eval": ["문제 해결력", "실현 가능성", "UI/UX 완성도", "시연 명확성"],
        "prize": ["1등 100만원", "2등 50만원", "3등 20만원"],
        "schedule": ["4/1 참가 시작", "4/7 팀빌딩 마감", "4/20 중간 점검", "4/30 최종 제출"],
    },
    {
        "slug": "campus-ai-builder",
        "title": "Campus AI Builder",
        "status": "예정",
        "tags": ["교육", "생성형AI"],
        "start_date": "2026-05-10",
        "end_date": "2026-05-25",
        "participants": 84,
        "overview": "대학생 대상 AI 서비스 기획 및 구현 해커톤입니다.",
        "summary": "대학생 대상 서비스 기획부터 MVP 구현까지 진행하는 해커톤",
        "guide": "문제 정의부터 MVP까지 명확한 사용자 경험을 제시해야 합니다.",
        "eval": ["창의성", "사용성", "기술성"],
        "prize": ["대상 150만원", "우수상 70만원"],
        "schedule": ["5/10 시작", "5/13 팀구성", "5/25 제출"],
    },
]

INITIAL_TEAMS = [
    {
        "id": "team-1",
        "hackathon_slug": "emergency-handover-docs",
        "name": "DACOM Makers",
        "intro": "해커톤 협업 경험을 구조적으로 설계하는 팀입니다.",
        "owner": CURRENT_USER,
        "members": [CURRENT_USER],
        "is_open": True,
        "looking_for": "Frontend 1명, Backend 1명",
        "contact_url": "https://open.kakao.com/",
    },
    {
        "id": "team-2",
        "hackathon_slug": "emergency-handover-docs",
        "name": "Flow Builders",
        "intro": "문서화와 사용자 흐름 설계에 강한 팀입니다.",
        "owner": "민서",
        "members": ["민서", "준호"],
        "is_open": False,
        "looking_for": "모집 마감",
        "contact_url": "https://github.com/",
    },
    {
        "id": "team-3",
        "hackathon_slug": "",
        "name": "Open Camp Crew",
        "intro": "아직 특정 해커톤은 정하지 않았지만 팀원을 미리 찾고 있습니다.",
        "owner": CURRENT_USER,
        "members": [CURRENT_USER],
        "is_open": True,
        "looking_for": "기획 1명, 디자이너 1명",
        "contact_url": "https://notion.so/",
    },
]

INITIAL_SUBMISSIONS = [
    {
        "id": "sub-1",
        "hackathon_slug": "emergency-handover-docs",
        "team_name": "DACOM Makers",
        "notes": "기본 플로우 + 팀빌딩 + 제출 시나리오 구현",
        "file_name": "dacom_prototype.pdf",
        "submitted_at": "2026-04-04 18:20",
        "status": "제출완료",
        "score": 98,
    }
]

INITIAL_LEADERBOARDS = {
    "emergency-handover-docs": [
        {"rank": 1, "team_name": "DACOM Makers", "points": 98, "status": "제출완료"},
        {"rank": 2, "team_name": "Flow Builders", "points": 92, "status": "제출완료"},
        {"rank": 3, "team_name": "Proto Crew", "points": 71, "status": "미제출"},
    ],
    "campus-ai-builder": [
        {"rank": 1, "team_name": "Starter Pack", "points": 0, "status": "미제출"},
    ],
    "global": [
        {"rank": 1, "nickname": CURRENT_USER, "points": 420},
        {"rank": 2, "nickname": "민서", "points": 380},
        {"rank": 3, "nickname": "준호", "points": 350},
        {"rank": 4, "nickname": "수빈", "points": 280},
    ],
}

INITIAL_APPLICATIONS = [
    {"id": "app-1", "team_name": "DACOM Makers", "user": "지우", "status": "pending"},
    {"id": "app-2", "team_name": "Flow Builders", "user": CURRENT_USER, "status": "pending"},
]

INITIAL_INVITATIONS = [
    {"id": "inv-1", "team_name": "DACOM Makers", "user": "민서", "status": "pending"},
    {"id": "inv-2", "team_name": "Open Camp Crew", "user": "수빈", "status": "pending"},
]

INITIAL_MESSAGES = {
    "DACOM Makers": [
        {"sender": CURRENT_USER, "text": "오늘까지 기본 플로우 점검하고 제출 화면 연결할게요.", "time": "2026-04-05 10:20"},
        {"sender": "지우", "text": "좋아요. 저는 팀 모집 UX랑 카드 구성 정리해볼게요.", "time": "2026-04-05 10:22"},
    ],
    "Open Camp Crew": [
        {"sender": CURRENT_USER, "text": "관심 있는 분은 역할이랑 가능 기간 같이 남겨주세요.", "time": "2026-04-05 09:10"},
    ],
}

INITIAL_TODOS = {
    "DACOM Makers": [
        {"task": "해커톤 상세 페이지 QA", "done": False},
        {"task": "제출 폼 연결 확인", "done": True},
    ],
    "Open Camp Crew": [
        {"task": "모집 포지션 정리", "done": False},
    ],
}

INITIAL_ACTIVITY_LOGS = {
    "DACOM Makers": [
        {"time": "2026-04-05 10:15", "text": "혜주가 팀 공지 초안을 정리했습니다."},
        {"time": "2026-04-05 10:32", "text": "지우가 팀 지원 요청을 보냈습니다."},
    ],
    "Open Camp Crew": [
        {"time": "2026-04-05 09:05", "text": "혜주가 모집글을 생성했습니다."},
    ],
}

INITIAL_DMS = {
    "민서": [
        {"sender": "민서", "text": "Flow Builders 일정 공유 가능할까요?", "time": "2026-04-05 11:00"},
        {"sender": CURRENT_USER, "text": "네, 오후에 정리해서 보낼게요.", "time": "2026-04-05 11:05"},
    ],
    "수빈": [
        {"sender": "수빈", "text": "Open Camp Crew 포지션 아직 열려 있나요?", "time": "2026-04-05 09:40"},
    ],
}

INITIAL_USER_PROFILES = [
    {
        "name": CURRENT_USER,
        "headline": "해커톤 협업 경험을 설계하는 PM · AI 기획형 빌더",
        "bio": "해커톤에서 팀빌딩, 협업 흐름, 제출 경험까지 연결되는 서비스를 만드는 데 관심이 있습니다.",
        "role": "PM",
        "skills": ["기획", "문서화", "UI Flow", "발표"],
        "available": "주 4회 가능",
        "portfolio": "DACOM 협업 플랫폼 기획 및 프로토타입 제작",
        "trust_score": 0.92,
        "points": 420,
        "view_count": 16,
        "is_public": True,
        "is_discoverable": True,
    },
    {
        "name": "민서",
        "headline": "프론트엔드와 UI 설계에 강한 빌더",
        "bio": "서비스 화면 구현과 인터랙션 설계 경험이 있습니다.",
        "role": "Frontend",
        "skills": ["React", "UI/UX"],
        "available": "주 4회 가능",
        "portfolio": "해커톤 웹 대시보드 2회 구현",
        "trust_score": 0.88,
        "points": 380,
        "view_count": 23,
        "is_public": True,
        "is_discoverable": True,
    },
    {
        "name": "준호",
        "headline": "API와 데이터 구조 설계 중심의 백엔드 개발자",
        "bio": "백엔드 API와 DB 구조를 안정적으로 설계합니다.",
        "role": "Backend",
        "skills": ["FastAPI", "DB"],
        "available": "주 5회 가능",
        "portfolio": "실시간 제출/랭킹 API 서버 제작",
        "trust_score": 0.86,
        "points": 350,
        "view_count": 19,
        "is_public": True,
        "is_discoverable": True,
    },
    {
        "name": "수빈",
        "headline": "LLM 응용과 프롬프트 설계 중심의 AI 빌더",
        "bio": "LLM 기반 기능 구현과 프롬프트 최적화 경험이 있습니다.",
        "role": "AI",
        "skills": ["LLM", "Prompt"],
        "available": "주 3회 가능",
        "portfolio": "AI 해커톤 3회 참여",
        "trust_score": 0.84,
        "points": 280,
        "view_count": 14,
        "is_public": True,
        "is_discoverable": True,
    },
    {
        "name": "지우",
        "headline": "브랜딩과 화면 완성도에 강한 디자이너",
        "bio": "서비스 브랜딩과 시각 구조를 정리하는 역할을 맡습니다.",
        "role": "Design",
        "skills": ["Figma", "Brand"],
        "available": "주 4회 가능",
        "portfolio": "브랜딩 시안 및 랜딩페이지 제작",
        "trust_score": 0.83,
        "points": 240,
        "view_count": 11,
        "is_public": True,
        "is_discoverable": True,
    },
    {
        "name": "하린",
        "headline": "발표 구조와 일정 관리 중심의 PM",
        "bio": "기획서와 발표 스토리라인 정리에 강합니다.",
        "role": "PM",
        "skills": ["기획", "문서화"],
        "available": "주 3회 가능",
        "portfolio": "발표 자료 구조화 및 프로젝트 관리",
        "trust_score": 0.80,
        "points": 220,
        "view_count": 9,
        "is_public": True,
        "is_discoverable": True,
    },
]

PAGE_SCENARIOS = {
    "home": [
        "사용자가 메인에서 해커톤 보기, 팀 찾기, 나의 팀, 메시지 중 하나를 선택합니다.",
        "심사위원은 상단 로고와 메뉴 이동이 실제 서비스처럼 동작하는지 확인할 수 있습니다.",
    ],
    "hackathons": [
        "사용자가 상태와 태그 기준으로 해커톤을 필터링합니다.",
        "각 카드의 상세보기 버튼을 눌러 해커톤 상세 화면으로 이동합니다.",
    ],
    "detail": [
        "사용자가 개요, 팀 빌딩, 협업, 평가, 상금, 안내, 일정, 제출, 리더보드를 한 흐름 안에서 탐색합니다.",
        "팀 초대/메시지/제출/리더보드까지 연결된 실제 시연 흐름을 보여줄 수 있습니다.",
    ],
    "camp": [
        "사용자가 팀 모집글을 확인하고 팀별로 메시지를 바로 보내거나 지원할 수 있습니다.",
        "새 팀 모집글 생성도 같은 페이지에서 가능해 탐색과 생성 흐름을 함께 보여줍니다.",
    ],
    "messages": [
        "사용자가 받은 요청, 보낸 요청, 상태 확인, 1:1 메시지를 확인합니다.",
        "팀 리스트에서 메시지 보내기를 누르면 바로 이 페이지로 이동해 대화를 시작할 수 있습니다.",
    ],
    "my_team": [
        "사용자가 내가 속한 팀의 정보, 팀원, 협업, 할 일, 활동 로그, 제출 연결을 확인합니다.",
        "오른쪽 영역에서 필요한 역할의 팀원을 필터링하고 바로 초대 요청을 보낼 수 있습니다.",
    ],
    "profile": [
        "사용자가 프로필 정보와 포트폴리오를 확인하고 공개 범위를 설정합니다.",
        "팀원 탐색 노출 여부를 끄면 다른 사용자의 초대 목록에서 실제로 숨겨집니다.",
    ],
}

def init_state() -> None:
    defaults = {
        "page": "home",
        "selected_slug": "emergency-handover-docs",
        "selected_team": "DACOM Makers",
        "selected_dm_target": "민서",
        "hackathons": copy.deepcopy(INITIAL_HACKATHONS),
        "teams": copy.deepcopy(INITIAL_TEAMS),
        "submissions": copy.deepcopy(INITIAL_SUBMISSIONS),
        "leaderboards": copy.deepcopy(INITIAL_LEADERBOARDS),
        "applications": copy.deepcopy(INITIAL_APPLICATIONS),
        "invitations": copy.deepcopy(INITIAL_INVITATIONS),
        "messages": copy.deepcopy(INITIAL_MESSAGES),
        "todos": copy.deepcopy(INITIAL_TODOS),
        "activity_logs": copy.deepcopy(INITIAL_ACTIVITY_LOGS),
        "dms": copy.deepcopy(INITIAL_DMS),
        "user_profiles": copy.deepcopy(INITIAL_USER_PROFILES),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def go_page(page_name: str, slug: str | None = None, team_name: str | None = None, dm_target: str | None = None) -> None:
    st.session_state.page = page_name
    if slug is not None:
        st.session_state.selected_slug = slug
    if team_name is not None:
        st.session_state.selected_team = team_name
    if dm_target is not None:
        st.session_state.selected_dm_target = dm_target

def get_selected_hackathon():
    for hackathon in st.session_state.hackathons:
        if hackathon["slug"] == st.session_state.selected_slug:
            return hackathon
    return None

def get_related_teams(slug: str):
    return [team for team in st.session_state.teams if team["hackathon_slug"] == slug]

def get_related_submissions(slug: str):
    return [submission for submission in st.session_state.submissions if submission["hackathon_slug"] == slug]

def get_team_invitations(team_name: str):
    return [inv for inv in st.session_state.invitations if inv["team_name"] == team_name]

def get_my_invitations():
    return [inv for inv in st.session_state.invitations if inv["user"] == CURRENT_USER]

def get_team_messages(team_name: str):
    return st.session_state.messages.get(team_name, [])

def get_team_todos(team_name: str):
    return st.session_state.todos.get(team_name, [])

def get_team_logs(team_name: str):
    return st.session_state.activity_logs.get(team_name, [])

def get_dm_messages(user_name: str):
    return st.session_state.dms.get(user_name, [])

def get_my_teams():
    return [team for team in st.session_state.teams if CURRENT_USER in team["members"] or team["owner"] == CURRENT_USER]

def get_profile(name: str):
    for profile in st.session_state.user_profiles:
        if profile["name"] == name:
            return profile
    return None

def get_discoverable_profiles(exclude_names=None):
    exclude_names = exclude_names or []
    results = []
    for profile in st.session_state.user_profiles:
        if profile["name"] in exclude_names:
            continue
        if not profile.get("is_discoverable", True):
            continue
        results.append(profile)
    return results

def update_my_profile(bio: str, is_public: bool, is_discoverable: bool) -> None:
    profile = get_profile(CURRENT_USER)
    if profile:
        profile["bio"] = bio
        profile["is_public"] = is_public
        profile["is_discoverable"] = is_discoverable

def status_html(status: str) -> str:
    if status == "진행중":
        return '<span class="status-live">진행중</span>'
    if status == "예정":
        return '<span class="status-upcoming">예정</span>'
    return '<span class="status-ended">종료</span>'

def recruitment_html(is_open: bool) -> str:
    return '<span class="status-open">모집중</span>' if is_open else '<span class="status-closed">모집마감</span>'

def flow_status_html(status: str) -> str:
    if status == "pending":
        return '<span class="status-pending">대기중</span>'
    if status == "accepted":
        return '<span class="status-accepted">수락됨</span>'
    if status == "rejected":
        return '<span class="status-rejected">거절됨</span>'
    if status == "제출완료":
        return '<span class="status-submitted">제출완료</span>'
    return f'<span class="status-closed">{status}</span>'

def add_team(team_data: dict) -> None:
    st.session_state.teams.insert(0, team_data)
    st.session_state.messages.setdefault(team_data["name"], [])
    st.session_state.todos.setdefault(team_data["name"], [])
    st.session_state.activity_logs.setdefault(team_data["name"], [])

def add_log(team_name: str, text: str) -> None:
    st.session_state.activity_logs.setdefault(team_name, []).insert(
        0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": text}
    )

def apply_to_team(team_name: str, user: str = CURRENT_USER) -> bool:
    for app in st.session_state.applications:
        if app["team_name"] == team_name and app["user"] == user:
            return False
    st.session_state.applications.insert(
        0,
        {
            "id": f"app-{len(st.session_state.applications) + 1}",
            "team_name": team_name,
            "user": user,
            "status": "pending",
        },
    )
    add_log(team_name, f"{user}가 팀 지원 요청을 보냈습니다.")
    return True

def invite_user_to_team(team_name: str, user: str) -> bool:
    for inv in st.session_state.invitations:
        if inv["team_name"] == team_name and inv["user"] == user:
            return False
    for team in st.session_state.teams:
        if team["name"] == team_name and user in team["members"]:
            return False
    st.session_state.invitations.insert(
        0,
        {
            "id": f"inv-{len(st.session_state.invitations) + 1}",
            "team_name": team_name,
            "user": user,
            "status": "pending",
        },
    )
    add_log(team_name, f"{user}에게 팀 초대를 보냈습니다.")
    return True

def update_invitation(team_name: str, user: str, status: str) -> None:
    for inv in st.session_state.invitations:
        if inv["team_name"] == team_name and inv["user"] == user:
            inv["status"] = status
            if status == "accepted":
                for team in st.session_state.teams:
                    if team["name"] == team_name and user not in team["members"]:
                        team["members"].append(user)
                add_log(team_name, f"{user}가 팀 초대를 수락했습니다.")
            elif status == "rejected":
                add_log(team_name, f"{user}가 팀 초대를 거절했습니다.")
            return

def add_submission(submission_data: dict) -> None:
    st.session_state.submissions.insert(0, submission_data)
    slug = submission_data["hackathon_slug"]
    team_name = submission_data["team_name"]
    score = random.randint(80, 99)

    if slug not in st.session_state.leaderboards:
        st.session_state.leaderboards[slug] = []

    rows = st.session_state.leaderboards[slug]
    found = False
    for row in rows:
        if row.get("team_name") == team_name:
            row["points"] = max(row["points"], score)
            row["status"] = "제출완료"
            found = True
            break

    if not found:
        rows.append(
            {
                "rank": len(rows) + 1,
                "team_name": team_name,
                "points": score,
                "status": "제출완료",
            }
        )

    rows.sort(key=lambda x: x["points"], reverse=True)
    for idx, row in enumerate(rows, start=1):
        row["rank"] = idx

    add_log(team_name, f"{team_name} 팀이 제출을 완료했습니다.")

def add_team_message(team_name: str, sender: str, text: str) -> None:
    st.session_state.messages.setdefault(team_name, []).append(
        {
            "sender": sender,
            "text": text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    add_log(team_name, f"{sender}가 팀 채팅 메시지를 남겼습니다.")

def add_todo(team_name: str, task: str) -> None:
    st.session_state.todos.setdefault(team_name, []).append({"task": task, "done": False})
    add_log(team_name, f"새 할 일 '{task}'가 추가되었습니다.")

def toggle_todo(team_name: str, index: int) -> None:
    todos = st.session_state.todos.get(team_name, [])
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
        state_text = "완료" if todos[index]["done"] else "진행중"
        add_log(team_name, f"할 일 '{todos[index]['task']}' 상태가 {state_text}로 변경되었습니다.")

def add_dm_message(target_user: str, sender: str, text: str) -> None:
    st.session_state.dms.setdefault(target_user, []).append(
        {
            "sender": sender,
            "text": text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )

def render_message_list(messages):
    if not messages:
        st.info("대화 기록이 없습니다.")
        return
    for msg in messages:
        klass = "msg-me" if msg["sender"] == CURRENT_USER else "msg-other"
        st.markdown(
            f"<div class='msg-box {klass}'><b>{msg['sender']}</b> · {msg['time']}<br><div style='margin-top:8px'>{msg['text']}</div></div>",
            unsafe_allow_html=True,
        )

def scenario_box(page_key: str) -> None:
    st.markdown('<div class="scenario-box">', unsafe_allow_html=True)
    st.markdown("### 🎬 이 페이지 시연 포인트")
    for idx, text in enumerate(PAGE_SCENARIOS.get(page_key, []), start=1):
        st.write(f"**{idx}.** {text}")
    st.markdown("</div>", unsafe_allow_html=True)

def top_nav() -> None:
    st.markdown('<div class="logo-text">DACOM</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Hackathon collaboration platform</div>', unsafe_allow_html=True)
    nav_cols = st.columns([1, 1, 1, 1, 1, 1, 0.9])
    labels = ["홈", "해커톤", "팀 탐색", "랭킹", "나의 팀", "메시지"]
    pages = ["home", "hackathons", "camp", "rankings", "my_team", "messages"]

    for idx, label in enumerate(labels):
        with nav_cols[idx]:
            if st.button(label, key=f"top_nav_{idx}", use_container_width=True):
                go_page(pages[idx])

    with nav_cols[6]:
        if st.button("프로필", key="top_nav_profile", use_container_width=True):
            go_page("profile")

    st.divider()

def render_home() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div style="font-size:0.95rem; opacity:0.85; margin-bottom:8px;">DACOM · Hackathon Collaboration Platform</div>
            <div style="font-size:2rem; font-weight:800; line-height:1.35;">
                해커톤 탐색부터 팀 구성, 협업, 제출, 리더보드 확인까지<br>
                한 번에 보여주는 협업형 프로토타입
            </div>
            <div style="margin-top:14px; color:#e2e8f0; line-height:1.7; font-size:0.98rem;">
                팀 생성, 지원, 초대, 팀 채팅, 할 일 관리, 제출, 메시지까지 이어지는 흐름을 시연할 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("해커톤 수", len(st.session_state.hackathons))
    c2.metric("팀 수", len(st.session_state.teams))
    c3.metric("제출 수", len(st.session_state.submissions))
    c4.metric("지원/초대 수", len(st.session_state.applications) + len(st.session_state.invitations))

    scenario_box("home")

def render_hackathons() -> None:
    st.title("해커톤 목록")
    st.caption("카드를 클릭하면 해커톤 상세 화면으로 이동합니다.")
    scenario_box("hackathons")

    all_tags = sorted({tag for h in st.session_state.hackathons for tag in h["tags"]})
    c1, c2 = st.columns(2)
    with c1:
        status_filter = st.selectbox("상태 필터", ["전체", "진행중", "예정", "종료"])
    with c2:
        tag_filter = st.selectbox("태그 필터", ["전체"] + list(all_tags))

    filtered = []
    for h in st.session_state.hackathons:
        if status_filter != "전체" and h["status"] != status_filter:
            continue
        if tag_filter != "전체" and tag_filter not in h["tags"]:
            continue
        filtered.append(h)

    if not filtered:
        st.info("조건에 맞는 해커톤이 없습니다.")
        return

    for h in filtered:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3.5, 1.1, 1.2, 1.2])
            with c1:
                st.subheader(h["title"])
                st.write(h["overview"])
                st.markdown("".join(f'<span class="chip">#{tag}</span>' for tag in h["tags"]), unsafe_allow_html=True)
            with c2:
                st.markdown("**상태**")
                st.markdown(status_html(h["status"]), unsafe_allow_html=True)
            with c3:
                st.markdown("**기간**")
                st.write(f"{h['start_date']} ~ {h['end_date']}")
            with c4:
                st.markdown("**참가자**")
                st.write(f"{h['participants']}명")
                if st.button("상세보기", key=f"open_{h['slug']}", use_container_width=True):
                    go_page("detail", slug=h["slug"])

def render_detail() -> None:
    h = get_selected_hackathon()
    if not h:
        st.warning("선택된 해커톤 정보가 없습니다.")
        return

    st.markdown(
        f"""
        <div class="hero-card">
            <div style="font-size:0.95rem; opacity:0.9;">{h['status']}</div>
            <div style="font-size:2.2rem; font-weight:800; margin-top:10px; line-height:1.3;">{h['title']}</div>
            <div style="margin-top:10px; opacity:0.9; font-size:1rem;">{h['summary']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    scenario_box("detail")
    tabs = st.tabs(["개요", "팀 빌딩", "협업", "평가", "상금", "안내", "일정", "제출", "리더보드"])

    with tabs[0]:
        st.write(h["overview"])
        c1, c2, c3 = st.columns(3)
        c1.info(f"시작일\n\n{h['start_date']}")
        c2.info(f"종료일\n\n{h['end_date']}")
        c3.info(f"참가자 수\n\n{h['participants']}명")

    with tabs[1]:
        related_teams = get_related_teams(h["slug"])
        left, right = st.columns([1.05, 0.95])

        with left:
            st.subheader("이 해커톤 팀 리스트")
            if not related_teams:
                st.info("아직 연결된 팀이 없습니다.")
            else:
                for team in related_teams:
                    with st.container(border=True):
                        a1, a2 = st.columns([4, 1])
                        with a1:
                            st.write(f"**팀명:** {team['name']}")
                            st.write(f"**소개:** {team['intro']}")
                            st.write(f"**팀장:** {team['owner']}")
                            st.write(f"**팀원:** {', '.join(team['members'])}")
                            st.write(f"**모집 포지션:** {team['looking_for']}")
                        with a2:
                            st.markdown(recruitment_html(team["is_open"]), unsafe_allow_html=True)

                        is_not_owner = team["owner"] != CURRENT_USER
                        is_not_member = CURRENT_USER not in team["members"]

                        b1, b2 = st.columns(2)
                        if is_not_owner and is_not_member and team["is_open"]:
                            if b1.button("지원하기", key=f"detail_apply_{team['id']}", use_container_width=True):
                                if apply_to_team(team["name"]):
                                    st.success("지원이 완료되었습니다.")
                                    st.rerun()
                                else:
                                    st.warning("이미 지원한 팀입니다.")

                        if b2.button("메시지 보내기", key=f"detail_dm_{team['id']}", use_container_width=True):
                            go_page("messages", dm_target=team["owner"])

                        if st.button("나의 팀으로 보기", key=f"detail_team_go_{team['id']}", use_container_width=True):
                            go_page("my_team", team_name=team["name"])

        with right:
            st.subheader("이 해커톤 팀 생성")
            with st.form("detail_team_create"):
                team_name = st.text_input("팀명(필수)")
                team_intro = st.text_area("소개(필수)")
                team_open = st.checkbox("모집중", value=True)
                team_looking_for = st.text_input("모집 포지션")
                team_contact = st.text_input("연락 링크")
                submit_team = st.form_submit_button("팀 생성", use_container_width=True)

                if submit_team:
                    if not team_name.strip() or not team_intro.strip():
                        st.error("팀명과 소개는 필수입니다.")
                    else:
                        new_team_name = team_name.strip()
                        add_team(
                            {
                                "id": f"team-{len(st.session_state.teams) + 1}",
                                "hackathon_slug": h["slug"],
                                "name": new_team_name,
                                "intro": team_intro.strip(),
                                "owner": CURRENT_USER,
                                "members": [CURRENT_USER],
                                "is_open": team_open,
                                "looking_for": team_looking_for.strip() if team_looking_for.strip() else "미정",
                                "contact_url": team_contact.strip() if team_contact.strip() else "추후 공유",
                            }
                        )
                        add_log(new_team_name, f"{CURRENT_USER}가 팀을 생성했습니다.")
                        st.success("팀이 생성되었습니다.")
                        st.rerun()

            st.subheader("내 팀 초대 관리")
            my_owned = [team for team in related_teams if team["owner"] == CURRENT_USER]
            if not my_owned:
                st.info("내가 관리하는 팀이 없습니다.")
            else:
                for my_team in my_owned:
                    with st.expander(f"{my_team['name']} 초대 상태 보기"):
                        invites = get_team_invitations(my_team["name"])
                        if not invites:
                            st.write("보낸 초대가 없습니다.")
                        else:
                            for inv in invites:
                                st.write(f"- {inv['user']} / {inv['status']}")

    with tabs[2]:
        st.subheader("협업 공간")
        joined_teams = [team for team in get_related_teams(h["slug"]) if CURRENT_USER in team["members"] or team["owner"] == CURRENT_USER]
        if not joined_teams:
            st.info("협업 공간은 내가 속한 팀에서만 사용할 수 있습니다.")
        else:
            team_names = [team["name"] for team in joined_teams]
            selected_chat_team = st.selectbox("협업할 팀 선택", team_names, key=f"collab_team_select_{h['slug']}")
            collab_tabs = st.tabs(["팀 채팅", "게시판/공지", "To-do List", "활동 로그"])

            with collab_tabs[0]:
                render_message_list(get_team_messages(selected_chat_team))
                with st.form(f"chat_form_{h['slug']}"):
                    chat_text = st.text_area("메시지 입력", placeholder="진행 상황, 요청 사항, 일정 등을 입력하세요.")
                    chat_submit = st.form_submit_button("메시지 보내기", use_container_width=True)
                    if chat_submit:
                        if not chat_text.strip():
                            st.error("메시지를 입력해주세요.")
                        else:
                            add_team_message(selected_chat_team, CURRENT_USER, chat_text.strip())
                            st.success("메시지를 보냈습니다.")
                            st.rerun()

            with collab_tabs[1]:
                logs = get_team_logs(selected_chat_team)
                if logs:
                    for log in logs[:5]:
                        with st.container(border=True):
                            st.write(f"**{log['time']}**")
                            st.write(log["text"])
                else:
                    st.info("공지/게시판 성격의 기록이 없습니다.")

            with collab_tabs[2]:
                todos = get_team_todos(selected_chat_team)
                if not todos:
                    st.info("등록된 할 일이 없습니다.")
                for idx, todo in enumerate(todos):
                    a1, a2 = st.columns([5, 1])
                    a1.checkbox(
                        todo["task"],
                        value=todo["done"],
                        key=f"todo_{selected_chat_team}_{idx}",
                        on_change=toggle_todo,
                        args=(selected_chat_team, idx),
                    )
                    a2.markdown(flow_status_html("accepted" if todo["done"] else "pending"), unsafe_allow_html=True)

                with st.form(f"todo_form_{selected_chat_team}"):
                    todo_text = st.text_input("새 할 일 추가")
                    todo_submit = st.form_submit_button("할 일 추가", use_container_width=True)
                    if todo_submit:
                        if not todo_text.strip():
                            st.error("할 일을 입력해주세요.")
                        else:
                            add_todo(selected_chat_team, todo_text.strip())
                            st.success("할 일이 추가되었습니다.")
                            st.rerun()

            with collab_tabs[3]:
                logs = get_team_logs(selected_chat_team)
                if not logs:
                    st.info("활동 로그가 없습니다.")
                else:
                    for log in logs:
                        with st.container(border=True):
                            st.write(f"**{log['time']}**")
                            st.write(log["text"])

    with tabs[3]:
        for item in h["eval"]:
            st.markdown(f"- {item}")

    with tabs[4]:
        for item in h["prize"]:
            st.markdown(f"- {item}")

    with tabs[5]:
        st.write(h["guide"])
        st.caption("공개 금지 정보: 내부 유저 정보, 비공개 데이터, 다른 팀 내부 정보는 노출하지 않는 구조를 기본 원칙으로 둡니다.")

    with tabs[6]:
        for item in h["schedule"]:
            st.markdown(f"- {item}")

    with tabs[7]:
        related_teams = get_related_teams(h["slug"])
        owned_or_joined = [team for team in related_teams if CURRENT_USER in team["members"] or team["owner"] == CURRENT_USER]
        team_options = [team["name"] for team in owned_or_joined]

        if not team_options:
            st.warning("먼저 팀을 생성하거나 팀에 합류해야 제출할 수 있습니다.")
        else:
            with st.form("submit_form"):
                selected_team = st.selectbox("제출 팀 선택", team_options)
                notes = st.text_area("메모(notes, optional)")
                uploaded_file = st.file_uploader("파일 업로드(zip / pdf / csv)", type=["zip", "pdf", "csv"])
                submit_btn = st.form_submit_button("저장 / 제출", use_container_width=True)

                if submit_btn:
                    if uploaded_file is None:
                        st.error("파일 업로드는 필수입니다.")
                    else:
                        add_submission(
                            {
                                "id": f"sub-{len(st.session_state.submissions) + 1}",
                                "hackathon_slug": h["slug"],
                                "team_name": selected_team,
                                "notes": notes,
                                "file_name": uploaded_file.name,
                                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "제출완료",
                                "score": random.randint(80, 99),
                            }
                        )
                        st.success("제출이 완료되었고 리더보드가 업데이트되었습니다.")
                        st.rerun()

        st.subheader("최근 제출 내역")
        related_subs = get_related_submissions(h["slug"])
        if not related_subs:
            st.info("아직 제출 내역이 없습니다.")
        else:
            for sub in related_subs:
                with st.container(border=True):
                    st.write(f"**팀명:** {sub['team_name']}")
                    st.write(f"**파일명:** {sub['file_name']}")
                    st.write(f"**메모:** {sub['notes'] if sub['notes'] else '-'}")
                    st.write(f"**제출 시각:** {sub['submitted_at']}")
                    st.markdown(flow_status_html(sub["status"]), unsafe_allow_html=True)

    with tabs[8]:
        rows = st.session_state.leaderboards.get(h["slug"], [])
        if not rows:
            st.info("리더보드 데이터가 없습니다.")
        else:
            head = st.columns([1, 3, 2, 2])
            head[0].markdown("**순위**")
            head[1].markdown("**팀명**")
            head[2].markdown("**점수**")
            head[3].markdown("**상태**")
            for row in rows:
                cols = st.columns([1, 3, 2, 2])
                cols[0].write(f"#{row['rank']}")
                cols[1].write(row["team_name"])
                cols[2].write(f"{row['points']}점")
                cols[3].write(row["status"])

def render_camp() -> None:
    st.title("팀 탐색")
    st.caption("해커톤 연결 여부를 선택해 팀 모집글을 만들고, 기존 팀에 지원하거나 메시지를 보낼 수 있습니다.")
    scenario_box("camp")

    hackathon_options = ["전체"] + [h["title"] for h in st.session_state.hackathons]
    selected_title = st.selectbox("해커톤 기준 필터", hackathon_options)
    title_to_slug = {h["title"]: h["slug"] for h in st.session_state.hackathons}

    filtered_teams = st.session_state.teams
    if selected_title != "전체":
        selected_slug = title_to_slug[selected_title]
        filtered_teams = [team for team in filtered_teams if team["hackathon_slug"] == selected_slug]

    left, right = st.columns([1.08, 0.92])

    with left:
        st.subheader("팀 리스트")
        if not filtered_teams:
            st.info("표시할 팀이 없습니다.")
        else:
            for team in filtered_teams:
                with st.container(border=True):
                    a1, a2 = st.columns([4, 1])
                    with a1:
                        st.write(f"**팀명:** {team['name']}")
                        st.write(f"**소개:** {team['intro']}")
                        st.write(f"**팀장:** {team['owner']}")
                        st.write(f"**팀원:** {', '.join(team['members'])}")
                        st.write(f"**모집 포지션:** {team['looking_for']}")
                        st.write(f"**연결 해커톤:** {team['hackathon_slug'] if team['hackathon_slug'] else '없음'}")
                    with a2:
                        st.markdown(recruitment_html(team["is_open"]), unsafe_allow_html=True)

                    can_apply = team["owner"] != CURRENT_USER and CURRENT_USER not in team["members"] and team["is_open"]
                    b1, b2 = st.columns(2)

                    if can_apply:
                        if b1.button("지원하기", key=f"camp_apply_{team['id']}", use_container_width=True):
                            if apply_to_team(team["name"]):
                                st.success("지원이 완료되었습니다.")
                                st.rerun()
                            else:
                                st.warning("이미 지원한 팀입니다.")

                    if b2.button("메시지 보내기", key=f"camp_dm_{team['id']}", use_container_width=True):
                        go_page("messages", dm_target=team["owner"])

    with right:
        st.subheader("팀 모집글 생성")
        with st.form("camp_form"):
            team_name = st.text_input("팀명(필수)")
            team_intro = st.text_area("소개(필수)")
            link_hackathon = st.selectbox("연결할 해커톤", ["연결 없음"] + [h["title"] for h in st.session_state.hackathons])
            is_open = st.checkbox("모집중", value=True)
            looking_for = st.text_input("모집 포지션")
            contact_url = st.text_input("연락 링크")
            submitted = st.form_submit_button("팀 모집글 생성", use_container_width=True)

            if submitted:
                if not team_name.strip() or not team_intro.strip():
                    st.error("팀명과 소개는 필수입니다.")
                else:
                    slug = "" if link_hackathon == "연결 없음" else title_to_slug[link_hackathon]
                    new_team_name = team_name.strip()
                    add_team(
                        {
                            "id": f"team-{len(st.session_state.teams) + 1}",
                            "hackathon_slug": slug,
                            "name": new_team_name,
                            "intro": team_intro.strip(),
                            "owner": CURRENT_USER,
                            "members": [CURRENT_USER],
                            "is_open": is_open,
                            "looking_for": looking_for.strip() if looking_for.strip() else "미정",
                            "contact_url": contact_url.strip() if contact_url.strip() else "추후 공유",
                        }
                    )
                    add_log(new_team_name, f"{CURRENT_USER}가 팀 모집글을 생성했습니다.")
                    st.success("팀 모집글이 생성되었습니다.")
                    st.rerun()

def render_rankings() -> None:
    st.title("랭킹")
    st.caption("글로벌 랭킹 테이블을 보여주는 페이지입니다.")
    scenario_box("rankings")

    rank_filter = st.selectbox("기간 필터(옵션)", ["전체", "최근", "30일"], index=0)
    st.caption(f"현재 선택된 필터: {rank_filter}")

    rows = st.session_state.leaderboards["global"]
    head = st.columns([1, 3, 2])
    head[0].markdown("**순위**")
    head[1].markdown("**닉네임**")
    head[2].markdown("**Points**")
    for row in rows:
        cols = st.columns([1, 3, 2])
        cols[0].write(f"#{row['rank']}")
        cols[1].write(row["nickname"])
        cols[2].write(f"{row['points']}점")

def render_my_team() -> None:
    st.title("나의 팀")
    st.caption("내가 속한 팀의 정보, 팀원, 협업, 할 일, 활동 로그, 제출 연결을 확인하는 페이지입니다.")
    scenario_box("my_team")

    my_teams = get_my_teams()
    if not my_teams:
        st.info("아직 속한 팀이 없습니다.")
        return

    team_names = [team["name"] for team in my_teams]
    default_index = team_names.index(st.session_state.selected_team) if st.session_state.selected_team in team_names else 0
    selected_team_name = st.selectbox("확인할 팀 선택", team_names, index=default_index)
    team = next((t for t in my_teams if t["name"] == selected_team_name), None)
    if not team:
        st.warning("팀 정보를 찾을 수 없습니다.")
        return

    st.session_state.selected_team = selected_team_name

    left_col, right_col = st.columns([1.15, 0.85])

    with left_col:
        with st.container(border=True):
            st.subheader(team["name"])
            st.write(team["intro"])
            st.write(f"**팀장:** {team['owner']}")
            st.write(f"**팀원:** {', '.join(team['members'])}")
            st.write(f"**모집 포지션:** {team['looking_for']}")
            st.markdown(recruitment_html(team["is_open"]), unsafe_allow_html=True)
            if team["hackathon_slug"]:
                related = [h for h in st.session_state.hackathons if h["slug"] == team["hackathon_slug"]]
                if related:
                    st.write(f"**연결 해커톤:** {related[0]['title']}")
                    if st.button("연결된 해커톤 상세 보기", key=f"myteam_go_detail_{team['id']}", use_container_width=True):
                        go_page("detail", slug=team["hackathon_slug"])

        team_tabs = st.tabs(["팀 채팅 / 게시판", "To-do List", "활동 로그"])

        with team_tabs[0]:
            render_message_list(get_team_messages(team["name"]))
            with st.form(f"myteam_chat_{team['id']}"):
                text = st.text_area("메시지 입력", placeholder="팀 공지, 진행 상황, 질문 등을 남겨보세요.")
                send = st.form_submit_button("메시지 보내기", use_container_width=True)
                if send:
                    if not text.strip():
                        st.error("메시지를 입력해주세요.")
                    else:
                        add_team_message(team["name"], CURRENT_USER, text.strip())
                        st.success("메시지를 보냈습니다.")
                        st.rerun()

        with team_tabs[1]:
            todos = get_team_todos(team["name"])
            if not todos:
                st.info("등록된 할 일이 없습니다.")
            for idx, todo in enumerate(todos):
                c1, c2 = st.columns([5, 1])
                c1.checkbox(
                    todo["task"],
                    value=todo["done"],
                    key=f"myteam_todo_{team['id']}_{idx}",
                    on_change=toggle_todo,
                    args=(team["name"], idx),
                )
                c2.markdown(flow_status_html("accepted" if todo["done"] else "pending"), unsafe_allow_html=True)

            with st.form(f"myteam_todo_add_{team['id']}"):
                todo_text = st.text_input("새 할 일")
                add_btn = st.form_submit_button("할 일 추가", use_container_width=True)
                if add_btn:
                    if not todo_text.strip():
                        st.error("할 일을 입력해주세요.")
                    else:
                        add_todo(team["name"], todo_text.strip())
                        st.success("할 일이 추가되었습니다.")
                        st.rerun()

        with team_tabs[2]:
            logs = get_team_logs(team["name"])
            if not logs:
                st.info("활동 로그가 없습니다.")
            else:
                for log in logs:
                    with st.container(border=True):
                        st.write(f"**{log['time']}**")
                        st.write(log["text"])

    with right_col:
        with st.container(border=True):
            st.subheader("제출 연결")
            related_subs = [sub for sub in st.session_state.submissions if sub["team_name"] == team["name"]]
            if not related_subs:
                st.info("아직 제출 내역이 없습니다.")
            else:
                latest = related_subs[0]
                st.write(f"**최근 제출 파일:** {latest['file_name']}")
                st.write(f"**제출 시각:** {latest['submitted_at']}")
                st.markdown(flow_status_html(latest["status"]), unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("팀원 리스트 / 초대")
            role_filter = st.selectbox("필요 역할 필터", ["전체", "Frontend", "Backend", "AI", "Design", "PM"], key=f"member_role_filter_{team['id']}")
            skill_query = st.text_input("기술/키워드 검색", key=f"member_skill_query_{team['id']}")

            filtered_members = []
            existing_members = set(team["members"])
            for profile in get_discoverable_profiles(exclude_names=list(existing_members)):
                if role_filter != "전체" and profile["role"] != role_filter:
                    continue
                if skill_query.strip():
                    haystack = " ".join(profile["skills"]) + " " + profile["bio"] + " " + profile["role"]
                    if skill_query.strip().lower() not in haystack.lower():
                        continue
                filtered_members.append(profile)

            if not filtered_members:
                st.info("조건에 맞는 팀원이 없습니다.")
            else:
                for profile in filtered_members:
                    with st.container(border=True):
                        st.write(f"**이름:** {profile['name']}")
                        st.write(f"**역할:** {profile['role']}")
                        st.write(f"**기술:** {', '.join(profile['skills'])}")
                        st.write(f"**소개:** {profile['bio']}")
                        st.write(f"**가능 일정:** {profile['available']}")
                        if st.button("바로 초대 요청하기", key=f"invite_member_{team['id']}_{profile['name']}", use_container_width=True):
                            if invite_user_to_team(team["name"], profile["name"]):
                                st.success(f"{profile['name']}님에게 초대 요청을 보냈습니다.")
                                st.rerun()
                            else:
                                st.warning("이미 초대했거나 이미 팀원입니다.")

def render_messages() -> None:
    st.title("메시지")
    st.caption("받은 요청, 보낸 요청, 상태 확인, 1:1 메시지를 확인하는 페이지입니다.")
    scenario_box("messages")

    tabs = st.tabs(["받은 요청", "보낸 요청", "상태 확인", "1:1 메시지"])

    with tabs[0]:
        my_invitations = get_my_invitations()
        if not my_invitations:
            st.info("받은 요청이 없습니다.")
        else:
            for inv in my_invitations:
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                    c1.write(f"**초대 팀:** {inv['team_name']}")
                    c2.markdown(flow_status_html(inv["status"]), unsafe_allow_html=True)
                    if inv["status"] == "pending":
                        if c3.button("수락", key=f"messages_inv_acc_{inv['id']}"):
                            update_invitation(inv["team_name"], inv["user"], "accepted")
                            st.rerun()
                        if c4.button("거절", key=f"messages_inv_rej_{inv['id']}"):
                            update_invitation(inv["team_name"], inv["user"], "rejected")
                            st.rerun()

    with tabs[1]:
        my_teams = [team for team in st.session_state.teams if team["owner"] == CURRENT_USER]
        sent = []
        for team in my_teams:
            sent.extend(get_team_invitations(team["name"]))
        if not sent:
            st.info("보낸 요청이 없습니다.")
        else:
            for inv in sent:
                with st.container(border=True):
                    st.write(f"**팀:** {inv['team_name']}")
                    st.write(f"**대상:** {inv['user']}")
                    st.markdown(flow_status_html(inv["status"]), unsafe_allow_html=True)

    with tabs[2]:
        my_apps = [app for app in st.session_state.applications if app["user"] == CURRENT_USER]
        if not my_apps and not get_my_invitations():
            st.info("확인할 상태가 없습니다.")
        else:
            st.markdown("#### 지원 상태")
            for app in my_apps:
                with st.container(border=True):
                    st.write(f"**지원 팀:** {app['team_name']}")
                    st.markdown(flow_status_html(app["status"]), unsafe_allow_html=True)

            st.markdown("#### 초대 상태")
            for inv in get_my_invitations():
                with st.container(border=True):
                    st.write(f"**초대 팀:** {inv['team_name']}")
                    st.markdown(flow_status_html(inv["status"]), unsafe_allow_html=True)

    with tabs[3]:
        target_names = DM_CANDIDATES
        default_idx = target_names.index(st.session_state.selected_dm_target) if st.session_state.selected_dm_target in target_names else 0
        dm_target = st.selectbox("대화 상대 선택", target_names, index=default_idx, key="dm_target_select")
        st.session_state.selected_dm_target = dm_target

        render_message_list(get_dm_messages(dm_target))

        with st.form("dm_form"):
            dm_text = st.text_area("메시지 입력", placeholder="팀 지원 전 간단한 문의를 남겨보세요.")
            dm_submit = st.form_submit_button("메시지 보내기", use_container_width=True)
            if dm_submit:
                if not dm_text.strip():
                    st.error("메시지를 입력해주세요.")
                else:
                    add_dm_message(dm_target, CURRENT_USER, dm_text.strip())
                    st.success("메시지를 보냈습니다.")
                    st.rerun()

def render_profile() -> None:
    profile = get_profile(CURRENT_USER)
    if not profile:
        st.error("프로필 정보를 찾을 수 없습니다.")
        return

    st.title("프로필")
    st.caption("메인 우측 상단 버튼으로 이동하는 독립 프로필 페이지입니다.")
    scenario_box("profile")

    left, right = st.columns([0.95, 2.05])

    with left:
        with st.container(border=True):
            st.subheader("프로필 메뉴")
            st.markdown("- 프로필 정보")
            st.markdown("- 소개 & 포트폴리오")
            st.markdown("- 역량 & 스킬")
            st.markdown("- 쇼케이스")
            st.markdown("- 참여 활동")
            st.markdown("- 포인트")
            st.markdown("- 랭킹")
            st.markdown("- 공개 설정")

    with right:
        st.markdown(
            f"""
            <div class="hero-card" style="padding-bottom:22px;">
                <div style="font-size:0.95rem; opacity:0.88;">DACOM Profile</div>
                <div style="font-size:2.1rem; font-weight:800; margin-top:8px;">{profile['name']}</div>
                <div style="margin-top:8px; font-size:1rem; opacity:0.92;">{profile['headline']}</div>
                <div style="margin-top:18px; display:flex; gap:18px; font-size:0.98rem; flex-wrap:wrap;">
                    <div>👀 조회수 {profile['view_count']}</div>
                    <div>신뢰 점수 {profile['trust_score']:.2f} / 1.0</div>
                    <div>포인트 {profile['points']}P</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1.15, 0.85])

        with c1:
            with st.container(border=True):
                st.subheader("소개")
                if profile.get("is_public", True):
                    st.write(profile["bio"])
                    st.write(f"**포트폴리오:** {profile['portfolio']}")
                    st.write(f"**주 역할:** {profile['role']}")
                    st.write(f"**기술:** {', '.join(profile['skills'])}")
                    st.write(f"**가능 일정:** {profile['available']}")
                else:
                    st.warning("현재 개인정보 공개가 꺼져 있어, 다른 사용자에게는 상세 프로필 정보가 숨겨집니다.")

        with c2:
            with st.container(border=True):
                st.subheader("공개 설정")
                st.caption("이 설정에 따라 다른 사용자에게 프로필이 보일지 결정됩니다.")
                new_public = st.toggle("개인정보 공개", value=profile.get("is_public", True), key="profile_public_toggle")
                new_discoverable = st.toggle("팀원 탐색 노출", value=profile.get("is_discoverable", True), key="profile_discoverable_toggle")
                st.caption("팀원 탐색 노출을 끄면 다른 사용자의 팀원 탐색/초대 목록에서 숨겨집니다.")

                if st.button("설정 저장", key="save_profile_settings", use_container_width=True):
                    update_my_profile(profile["bio"], new_public, new_discoverable)
                    st.success("프로필 설정이 저장되었습니다.")
                    st.rerun()

        with st.container(border=True):
            st.subheader("프로필 수정")
            with st.form("profile_edit_form"):
                bio_text = st.text_area("소개 수정", value=profile["bio"], height=140)
                submit_profile = st.form_submit_button("프로필 업데이트", use_container_width=True)
                if submit_profile:
                    update_my_profile(
                        bio_text,
                        st.session_state.get("profile_public_toggle", profile.get("is_public", True)),
                        st.session_state.get("profile_discoverable_toggle", profile.get("is_discoverable", True)),
                    )
                    st.success("프로필이 업데이트되었습니다.")
                    st.rerun()

        with st.container(border=True):
            st.subheader("팀원 탐색 노출 미리보기")
            if profile.get("is_discoverable", True):
                st.success("현재 프로필은 팀원 탐색에 노출됩니다.")
            else:
                st.warning("현재 프로필은 팀원 탐색에 노출되지 않습니다.")

top_nav()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "hackathons":
    render_hackathons()
elif st.session_state.page == "detail":
    render_detail()
elif st.session_state.page == "camp":
    render_camp()
elif st.session_state.page == "rankings":
    render_rankings()
elif st.session_state.page == "my_team":
    render_my_team()
elif st.session_state.page == "messages":
    render_messages()
elif st.session_state.page == "profile":
    render_profile()