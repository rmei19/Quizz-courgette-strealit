import streamlit as st
import json
import random

# Charger les questions depuis le fichier JSON
with open("quiz_questions_50.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Initialisation de la session
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in ["saucisse", "courgette", "caillou", "crotte de chien"]}

def restart_quiz():
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in st.session_state.scores}

if not st.session_state.started:
    st.title("Quel est ton vrai toi ?")
    st.markdown("**Saucisse**, **Courgette**, **Caillou** ou... *Crotte de chien* ? 😄")
    if st.button("Commencer le quiz"):
        st.session_state.started = True

else:
    if st.session_state.current < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current]
        st.markdown(f"### Question {st.session_state.current + 1} : {q['question']}")
        for text, profil in q["choices"]:
            if st.button(text, key=f"q{st.session_state.current}_{profil}"):
                st.session_state.scores[profil] += 1
                st.session_state.current += 1

    else:
        st.subheader("Résultat final 🧠")
        winner = max(st.session_state.scores, key=st.session_state.scores.get)
        st.success(f"Tu es surtout : **{winner.upper()}** !")

        st.markdown("### Détails :")
        for profil, score in st.session_state.scores.items():
            st.write(f" - {profil} : {score}")

        if st.button("Rejouer 🔁"):
            restart_quiz()
