import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="OCM Dashboard",
    layout="wide",
    page_icon="⚽"
)

# -----------------------------
# FONT AWESOME
# -----------------------------

st.markdown("""
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data(ttl=30)
def load_data():

    spreadsheet = client.open("OCM: Premier League S13")

    # LEAGUE TABLE
    table_sheet = spreadsheet.worksheet("Table-Data")
    table_data = table_sheet.get_all_records()

    # SQUADS
    squad_sheet = spreadsheet.worksheet("Squads")
    squad_data = squad_sheet.get_all_values()

    # FIXTURES
    fixtures_sheet = spreadsheet.worksheet("Fixtures-Data")
    fixtures_data = fixtures_sheet.get_all_values()

    return table_data, squad_data, fixtures_data

table_data, squad_data, fixtures_data = load_data()

# -----------------------------
# DATAFRAMES
# -----------------------------

df = pd.DataFrame(table_data)

# PRESERVE EXACT LAYOUT
squad_df = pd.DataFrame(squad_data).fillna("")

# FIXTURES
fixtures_df = pd.DataFrame(fixtures_data).fillna("")

# -----------------------------
# CLEAN LEAGUE TABLE
# -----------------------------

df = df[df["TEAM"].notna()]

df = df.sort_values(
    by=["PTS", "GD"],
    ascending=[False, False]
)

df = df.reset_index(drop=True)

columns_to_remove = [
    "+/-",
    "/-",
    "FORM",
    "P"
]

df = df.drop(
    columns=[
        col for col in df.columns
        if str(col).strip() in columns_to_remove
    ],
    errors="ignore"
)

df = df.loc[
    :,
    ~df.columns.astype(str).str.contains(r"/-", regex=True)
]

# POSITION COLUMN
df.insert(0, "POS", range(1, len(df) + 1))

# -----------------------------
# FULL TEAM NAMES
# -----------------------------

team_name_map = {
    "MNC": "Manchester City",
    "AST": "Aston Villa",
    "NFO": "Nottingham Forest",
    "EVE": "Everton",
    "WHU": "West Ham",
    "MNU": "Manchester United",
    "BAR": "Barnsley",
    "CHE": "Chelsea",
    "TOT": "Spurs",
    "FUL": "Fulham",
    "ARS": "Arsenal",
    "NOR": "Norwich City",
    "BLR": "Blackburn Rovers",
    "MID": "Middlesbrough",
    "LEE": "Leeds United",
    "PBU": "Peterborough United",
    "HUL": "Hull City",
    "WBA": "West Brom",
    "BRI": "Bristol City",
    "LIV": "Liverpool"
}

df["TEAM"] = df["TEAM"].replace(team_name_map)

# -----------------------------
# GLOBAL CSS
# -----------------------------

st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* MAIN BACKGROUND */
.stApp {

    background-color: #07090d;

    background-image:

        radial-gradient(
            circle at 15% 20%,
            rgba(0, 102, 255, 0.18) 0%,
            transparent 26%
        ),

        radial-gradient(
            circle at 85% 12%,
            rgba(255, 45, 85, 0.10) 0%,
            transparent 22%
        ),

        radial-gradient(
            circle at 50% 85%,
            rgba(0, 255, 180, 0.08) 0%,
            transparent 30%
        ),

        linear-gradient(
            180deg,
            #040506 0%,
            #0a0d12 30%,
            #10141b 60%,
            #080b10 100%
        );

    background-attachment: fixed;

    color: white;

    font-family: 'Inter', sans-serif;
}

/* CONTENT PANEL */
.block-container {

    background:
        linear-gradient(
            180deg,
            rgba(255,255,255,0.015),
            rgba(255,255,255,0.005)
        );

    border:
        1px solid rgba(255,255,255,0.04);

    border-radius: 24px;

    padding: 2rem !important;

    backdrop-filter: blur(12px);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.03);

    margin-top: 1rem;

    margin-bottom: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(12,14,18,0.96),
            rgba(8,10,14,0.96)
        );

    border-right:
        1px solid rgba(255,255,255,0.04);

    backdrop-filter: blur(18px);
}

/* TITLES */
h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2 {
    font-weight: 700 !important;
}

h1, h2, h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.title("⚽ OCM Dashboard")

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    page = option_menu(
        "OCM Navigation",
        [
            "League Table",
            "Squad Lists",
            "Fixtures",
            "Results",
            "Top Scorers"
        ],
        icons=[
            "table",
            "people",
            "calendar",
            "trophy",
            "star"
        ],
        menu_icon="cast",
        default_index=0
    )

# -----------------------------
# LEAGUE TABLE
# -----------------------------

if page == "League Table":

    st.header("League Table")

    st.table(df)

# -----------------------------
# SQUAD LISTS
# -----------------------------

elif page == "Squad Lists":

    st.header("Squad Lists")

    squad_display = squad_df.iloc[5:].reset_index(drop=True)

    team_colours = {
        "Arsenal": "#EF0107",
        "Aston Villa": "#95BFE5",
        "Barnsley": "#C8102E",
        "Chelsea": "#034694",
        "Everton": "#003399",
        "Fulham": "#FFFFFF",
        "Liverpool": "#C8102E",
        "Manchester City": "#6CABDD",
        "Manchester United": "#DA291C",
        "Nottingham Forest": "#DD0000",
        "Spurs": "#FFFFFF",
        "West Ham": "#7A263A"
    }

    row_index = 0

    while row_index < len(squad_display):

        team_name = str(
            squad_display.iloc[row_index, 1]
        ).strip()

        if (
            team_name == ""
            or team_name.lower() == "none"
        ):

            row_index += 1
            continue

        team_colour = team_colours.get(
            team_name,
            "#FFFFFF"
        )

        st.markdown(
            f"""
            <h2 style='
                color:{team_colour};
                margin-top:50px;
                margin-bottom:20px;
                font-size:32px;
                font-weight:800;
            '>
                {team_name}
            </h2>
            """,
            unsafe_allow_html=True
        )

        header_cols = st.columns([4,1,1,1,1,1,1,1,1,1])

        headers = [
            "PLAYER",
            "SA",
            "SUB",
            "G",
            "A",
            "MOTM",
            "CS",
            "YC",
            "RC",
            "G+A"
        ]

        for col, header in zip(header_cols, headers):

            col.markdown(
                f"""
                <div style='
                    color:#9aa4b2;
                    text-align:center;
                    font-weight:700;
                    margin-bottom:10px;
                    font-size:14px;
                '>
                    {header}
                </div>
                """,
                unsafe_allow_html=True
            )

        player_start = row_index + 1

        for i in range(25):

            current_row = squad_display.iloc[player_start + i]

            player_name = str(
                current_row.iloc[2]
            ).strip()

            if player_name == "":
                continue

            cols = st.columns([4,1,1,1,1,1,1,1,1,1])

            cols[0].markdown(
                f"""
                <div style='
                    background:#171717;
                    border:1px solid rgba(255,255,255,0.05);
                    padding:12px;
                    border-radius:12px;
                    color:white;
                    font-weight:600;
                    margin-bottom:8px;
                    font-size:15px;
                '>
                    {player_name}
                </div>
                """,
                unsafe_allow_html=True
            )

            stats = [
                current_row.iloc[3],
                current_row.iloc[4],
                current_row.iloc[5],
                current_row.iloc[6],
                current_row.iloc[7],
                current_row.iloc[8],
                current_row.iloc[9],
                current_row.iloc[10],
                current_row.iloc[11]
            ]

            for j in range(1, 10):

                cols[j].markdown(
                    f"""
                    <div style='
                        background:#111111;
                        border:1px solid rgba(255,255,255,0.04);
                        padding:12px 8px;
                        border-radius:12px;
                        color:white;
                        text-align:center;
                        margin-bottom:8px;
                        font-weight:600;
                        font-size:14px;
                    '>
                        {stats[j - 1]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        row_index += 28

# -----------------------------
# FIXTURES
# -----------------------------

elif page == "Fixtures":

    st.header("Fixtures")

    # LOOP THROUGH ALL GAMEWEEKS
    for gw_number in range(1, 39):

        current_gw = f"GW{gw_number}"

        # FILTER FIXTURES
        gw_fixtures = fixtures_df[
            fixtures_df.iloc[:, 1] == current_gw
        ]

        # GAMEWEEK HEADER
        st.markdown(
            f"""
            <div style="
                margin-top:30px;
                margin-bottom:10px;
                padding-left:10px;
                border-left:4px solid #005eff;
                font-size:20px;
                font-weight:800;
                color:white;
            ">
                {current_gw}
            </div>
            """,
            unsafe_allow_html=True
        )

        # FIXTURE ROWS
        for _, row in gw_fixtures.iterrows():

            # TEAM ABBREVIATIONS
            home_abbr = str(row.iloc[2]).strip()
            away_abbr = str(row.iloc[3]).strip()

            # FULL TEAM NAMES
            home = team_name_map.get(home_abbr, home_abbr)
            away = team_name_map.get(away_abbr, away_abbr)

            # ROW CONTAINER
            st.markdown(
                """
                <div style="
                    background:rgba(255,255,255,0.02);
                    border:1px solid rgba(255,255,255,0.04);
                    border-radius:10px;
                    padding:2px 6px;
                    margin-bottom:6px;
                ">
                </div>
                """,
                unsafe_allow_html=True
            )

            # STREAMLIT COLUMNS
            col1, col2, col3 = st.columns([5,1,5])

            with col1:
                st.markdown(
                    f"""
                    <div style="
                        font-size:14px;
                        font-weight:600;
                        color:white;
                        padding-top:6px;
                        padding-bottom:6px;
                    ">
                        {home}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    """
                    <div style="
                        text-align:center;
                        font-size:10px;
                        font-weight:700;
                        color:#7d8590;
                        padding-top:8px;
                    ">
                        VS
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f"""
                    <div style="
                        text-align:right;
                        font-size:14px;
                        font-weight:600;
                        color:white;
                        padding-top:6px;
                        padding-bottom:6px;
                    ">
                        {away}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# -----------------------------
# RESULTS
# -----------------------------

elif page == "Results":

    st.header("Results")
    st.write("Results coming soon")

# -----------------------------
# TOP SCORERS
# -----------------------------

elif page == "Top Scorers":

    st.header("Top Scorers")
    st.write("Top scorers coming soon")