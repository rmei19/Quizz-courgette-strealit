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
    st.session_state.selected_answer = None

# Fonction pour relancer le quiz
def restart_quiz():
    st.session_state.started = False
    st.session_state.current = 0
    st.session_state.questions = random.sample(all_questions, 10)
    st.session_state.scores = {k: 0 for k in st.session_state.scores}
    st.session_state.selected_answer = None

# UI principale
st.title("Quel est ton vrai toi ?")

if not st.session_state.started:
    st.markdown("Un test ultra scientifique pour découvrir ta véritable nature en dix questions.\n\nClique sur une réponse puis sur **'Question suivante'**.")
    if st.button("Commencer le quiz"):
        st.session_state.started = True

elif st.session_state.current < len(st.session_state.questions):
    q_index = st.session_state.current
    question = st.session_state.questions[q_index]
    progress = (st.session_state.current / len(st.session_state.questions))
    
st.progress(progress)
st.markdown(f"### Question {q_index + 1} : {question['question']}")
# Afficher les choix avec un radio button
choice_texts = [text for text, _ in question["choices"]]
selected = st.radio("Fais ton choix :", choice_texts, key=f"radio_{q_index}")

# Afficher le bouton pour valider
if selected:
    if st.button("Question suivante ▶️"):
        for text, profil in question["choices"]:
            if text == selected:
                st.session_state.scores[profil] += 1
                break
        st.session_state.current += 1
        st.session_state.selected_answer = None

else:
    st.subheader("Résultat final 🎉")
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    descriptions = {
    "saucisse": "Tu es une boule d’énergie grillée, toujours prêt·e pour la fête et les barbecues 🍖🔥",
    "courgette": "Tu es naturel·le, doux·ce, toujours en phase avec la planète 🌱✨",
    "caillou": "Solide, discret·e, tu encaisses tout sans broncher 🪨💪",
    "crotte de chien": "Énigmatique et indésirable mais toujours là où on ne t’attend pas... 💩"}

    st.info(descriptions[winner])
    st.success(f"Tu es surtout : **{winner.upper()}** !")

    st.markdown("### Résumé des scores :")
    for profil, score in st.session_state.scores.items():
        st.write(f" - {profil} : {score}")

    st.markdown("---")
    st.markdown("### Partage ton résultat avec tes amis :")
    st.code(f"Moi, je suis surtout : {winner.upper()} ! #QuizCourgette", language="text")

    if st.button("Rejouer 🔁"):
        restart_quiz()
        
