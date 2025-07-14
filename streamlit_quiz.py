import streamlit as st
import json
import random

# Charger les questions
with open("quiz_questions_50.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Initialisation
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in ["saucisse", "courgette", "caillou", "crotte de chien"]}
    st.session_state.answered = False

def restart_quiz():
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in st.session_state.scores}
    st.session_state.answered = False

def handle_answer(profil):
    st.session_state.scores[profil] += 1
    st.session_state.answered = True

# Interface
if not st.session_state.started:
    st.title("Quel est ton vrai toi ?")
    st.markdown("**Saucisse**, **Courgette**, **Caillou** ou... *Crotte de chien* ? 😄")
    if st.button("Commencer le quiz"):
        st.session_state.started = True

elif st.session_state.current < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current]
    st.markdown(f"### Question {st.session_state.current + 1} : {q['question']}")

    if not st.session_state.answered:
        for text, profil in q["choices"]:
            if st.button(text, key=f"q{st.session_state.current}_{profil}"):
                handle_answer(profil)
    else:
        st.markdown("✅ Réponse enregistrée !")
        if st.button("Question suivante ▶️"):
            st.session_state.current += 1
            st.session_state.answered = False

else:
    st.subheader("Résultat final 🧠")
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    st.success(f"Tu es surtout : **{winner.upper()}** !")

    st.markdown("### Détails :")
    for profil, score in st.session_state.scores.items():
        st.write(f" - {profil} : {score}")

    if st.button("Rejouer 🔁"):
        restart_quiz()
        
