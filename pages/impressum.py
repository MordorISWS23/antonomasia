import streamlit as st

impressum = st.markdown('<p style="font-size: 12px; font-weight: bold;">Impressum</p>', unsafe_allow_html=True)
address = st.markdown('<p style="font-size: 12px;">Universität Bremen ' \
               '<br> Bibliothekstraße 1 ' \
               '<br> D-28359 Bremen </p>', unsafe_allow_html=True)
legal = st.markdown('<p style="font-size: 12px; font-weight: bold;">Rechtsform</p>', unsafe_allow_html=True)
text_legal = st.markdown('<p style="font-size: 12px;">Die Universität Bremen ist eine Körperschaft des ' \
                  'Öffentlichen Rechts. Sie wird durch die Rektorin Prof. Dr. Jutta Günther ' \
                  'gesetzlich vertreten.  ' \
                  '<br> Zuständige Aufsichtsbehörde ist die Senatorin für Wissenschaft' \
                  ' und Häfen, Katharinenstraße 37, 28195 Bremen. </p>', unsafe_allow_html=True)
responsibility_cont = st.markdown('<p style="font-size: 12px; font-weight: bold;">Inhaltliche Verantwortlichkeit ' \
                           'i. S. v. § 5 TMG und § 18 Abs. 2 MStV</p>', unsafe_allow_html=True)
text_res_cont = st.markdown('<p style="font-size: 12px;">Für die Richtigkeit und Aktualität der veröffentlichten Inhalte ' \
                     '(auch Kommentare von Leser*innen) sind die jeweiligen Ersteller*innen der einzelnen Seiten ' \
                     'verantwortlich. Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung ' \
                     'für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich ' \
                     'deren Betreiber verantwortlich.' \
                     '<br> <br> Johanna Rockstroh' \
                     '<br> Universität Bremen' \
                     '<br> Bibliothekstraße 5' \
                     '<br> D-28359 Bremen' \
                     '<br> Tel.: +49 421 218 64424' \
                     '<br> E-Mail: rockstro@uni-bremen.de  </p>', unsafe_allow_html=True)
responsibility_tech = st.markdown('<p style="font-size: 12px; font-weight: bold;">Technische Verantwortlichkeit ' \
                           'i. S. v. § 5 TMG und § 18 Abs. 2 MStV</p>', unsafe_allow_html=True)
text_res_tech = st.markdown('<p style="font-size: 12px;">' \
                     'Johanna Rockstroh' \
                     '<br> Universität Bremen' \
                     '<br> Bibliothekstraße 5' \
                     '<br> D-28359 Bremen' \
                     '<br> Tel.: +49 421 218 64424' \
                     '<br> E-Mail: rockstro@uni-bremen.de </p>', unsafe_allow_html=True)
