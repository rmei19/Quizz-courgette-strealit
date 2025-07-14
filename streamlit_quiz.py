import streamlit as st
import json
import random

# Charger les questions depuis le fichier JSON
with open("quiz_questions_50.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Initialisation des variables de session
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in ["saucisse", "courgette", "caillou", "crotte de chien"]}
    st.session_state.last_clicked = None

# Fonction pour relancer le quiz
def restart_quiz():
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in st.session_state.scores}
    st.session_state.last_clicked = None

# UI principale
st.title("Quel est ton vrai toi ?")

if not st.session_state.started:
    st.markdown("**Saucisse**, **Courgette**, **Caillou** ou... *Crotte de chien* ? 🧠\n\nUn test ultra scientifique pour découvrir ta véritable essence.")
    if st.button("Commencer le quiz"):
        st.session_state.started = True

elif st.session_state.current < len(st.session_state.questions):
    q_index = st.session_state.current
    question = st.session_state.questions[q_index]
    st.markdown(f"### Question {q_index + 1} : {question['question']}")

    for i, (text, profil) in enumerate(question["choices"]):
        if st.button(text, key=f"{q_index}_{i}"):
            if st.session_state.last_clicked != f"{q_index}_{i}":  # éviter double enregistrement
                st.session_state.scores[profil] += 1
                st.session_state.current += 1
                st.session_state.last_clicked = f"{q_index}_{i}"

else:
    st.subheader("Résultat final 🎉")
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    st.success(f"Tu es surtout : **{winner.upper()}** !")

    st.markdown("### Résumé des scores :")
    for profil, score in st.session_state.scores.items():
        st.write(f" - {profil} : {score}")

    if st.button("Rejouer 🔁"):
        restart_quiz()
        
