import streamlit as st
import json
import random

# Charger les questions depuis le fichier JSON
with open("quiz_questions_50.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Descriptions et images par profil
descriptions = {
    "saucisse": "Tu es une boule d’énergie grillée, toujours prêt·e pour la fête et les barbecues 🍖🔥",
    "courgette": "Tu es naturel·le, doux·ce, toujours en phase avec la planète 🌱✨",
    "caillou": "Solide, discret·e, tu encaisses tout sans broncher 🪨💪",
    "crotte de chien": "Énigmatique et indésirable mais toujours là où on ne t’attend pas... 💩🤷‍♂️"
}

image_paths = {
    "saucisse": "saucisse.png",
    "courgette": "courgette.png",
    "caillou": "caillou.png",
    "crotte de chien": "crotte.png"
}

# Initialisation de la session
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

# UI
st.title("Quel est ton vrai toi ?")
st.markdown("Un test ultra-scientifique pour découvrir ta véritable nature.\n")

# Lancement du quiz
if not st.session_state.started:
    if st.button("🚀 Commencer le quiz"):
        st.session_state.started = True

# Quiz en cours
elif st.session_state.current < len(st.session_state.questions):
    q_index = st.session_state.current
    question = st.session_state.questions[q_index]
    st.markdown(f"### Question {q_index + 1} : {question['question']}")

    for i, (text, profil) in enumerate(question["choices"]):
        if st.button(text, key=f"{q_index}_{i}"):
            if st.session_state.last_clicked != f"{q_index}_{i}":
                st.session_state.scores[profil] += 1
                st.session_state.current += 1
                st.session_state.last_clicked = f"{q_index}_{i}"

    # Barre de progression
    st.progress((q_index + 1) / len(st.session_state.questions))

# Résultat
else:
    st.subheader("Résultat final 🎉")
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    st.success(f"Tu es surtout : **{winner.upper()}** !")

    st.info(descriptions[winner])

    # Affiche image si disponible
    if winner in image_paths:
        st.image(image_paths[winner], caption=f"Voici ton vrai toi : {winner}", use_column_width=True)

    st.markdown("### Résumé des scores :")
    for profil, score in st.session_state.scores.items():
        st.write(f" - {profil} : {score}")

    # Bouton rejouer
    if st.button("🔁 Rejouer"):
        restart_quiz()
        
