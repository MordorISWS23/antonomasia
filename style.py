import streamlit as st

# hide hamburger menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        #main-header {display: none};
        </style>
        """
custom_style = f"""
<style>


div[data-testid="stSidebar"] {{display: none;}}

[data-testid="stHeader"] {{
background: #25be8e;
}}

[data-baseweb="stAlert"] {{
background: #F5F5F5;
}}


[data-testid="stSelectbox"] {{
color: #F8F8FF;
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stHeader"] {{
    display: none !important;
}}

</style>
"""
css_info = f"""
<style>
    .info-box {{
        background-color: #F5F5F5; /* Replace with your desired background color */
        padding: 1rem;
        border-radius: 5px;
    }}
</style>
"""
footer = """
        <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f
                5f5f5;
                color: #666;
                text-align: right;
                padding: 10px;
                font-size: 16px;
            }
        </style>
        """


def write_footer():
    st.markdown(
        """
        <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #FFFFFF;
                color: #666;
                text-align: right;
                padding: 10px;
                font-size: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="footer"><a href="https://antonomasia.informatik.uni-bremen.de/imprint">Imprint</a> '
        '| <a href="https://www.uni-bremen.de/en/data-privacy">Privacy Policy</a></div>',
        unsafe_allow_html=True
    )
