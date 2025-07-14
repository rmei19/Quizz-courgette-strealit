import streamlit as st
import json
import random

# Charger les questions
with open("quiz_questions_50.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Initialiser la session
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in ["saucisse", "courgette", "caillou", "crotte de chien"]}
    st.session_state.answers = []

def restart_quiz():
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in st.session_state.scores}
    st.session_state.answers = []

# Interface
st.title("Quel est ton vrai toi ?")

if not st.session_state.started:
    st.markdown("**Saucisse**, **Courgette**, **Caillou** ou... *Crotte de chien* ? 😄")
    if st.button("Commencer le quiz"):
        st.session_state.started = True

elif st.session_state.current < len(st.session_state.questions):
    q_index = st.session_state.current
    question = st.session_state.questions[q_index]

    st.markdown(f"### Question {q_index + 1} : {question['question']}")

    with st.form(key=f"form_{q_index}"):
        choice = st.radio("Fais ton choix :", [c[0] for c in question["choices"]], index=None)
        submitted = st.form_submit_button("Valider")

        if submitted and choice:
            # Chercher le profil associé à la réponse choisie
            for text, profil in question["choices"]:
                if text == choice:
                    st.session_state.scores[profil] += 1
                    break
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
        
