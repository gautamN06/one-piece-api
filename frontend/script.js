let questions = [];
let currentQuestion = 0;
let score = 0;


async function getQuiz() {
    try {
        const response = await fetch("http://127.0.0.1:8000/quiz");

        if (!response.ok) {
            throw new Error("Could not load quiz");
        }

        const data = await response.json();

        questions = data.questions;
        currentQuestion = 0;
        score = 0;

        showQuestion();

    } catch (error) {
        console.error(error);

        document.getElementById("quiz").innerHTML = `
            <p>Failed to load quiz.</p>
        `;
    }
}


function showQuestion() {

    const question = questions[currentQuestion];

    const quizDiv = document.getElementById("quiz");

    quizDiv.innerHTML = `
        <h2>Question ${currentQuestion + 1}/${questions.length}</h2>

        <p>${question.question}</p>

        <div class="answers">
            ${question.answers.map(answer => `
                <button class="answer-button">
                    ${answer}
                </button>
            `).join("")}
        </div>
    `;

    
    const answerButtons = document.querySelectorAll(".answer-button");

    
    answerButtons.forEach(button => {

        button.addEventListener("click", () => {

            checkAnswer(
                question,
                button.textContent.trim()
            );

        });

    });

    
    document.getElementById("next-button").style.display = "none";
}



async function checkAnswer(question, selectedAnswer) {

    try {

        const response = await fetch("http://127.0.0.1:8000/quiz/answer", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                character_id: question.character_id,
                question_type: question.question_type,
                answer: selectedAnswer
            })

        });

        if (!response.ok) {
            throw new Error("Could not check answer");
        }

        const result = await response.json();

        // Disable all answer buttons
        const answerButtons =
            document.querySelectorAll(".answer-button");

        answerButtons.forEach(button => {
            button.disabled = true;
        });


        
        if (result.correct) {

            score++;

            document.querySelectorAll(".answer-button").forEach(button => {

                if (button.textContent.trim() === selectedAnswer) {
                    button.style.backgroundColor = "green";
                    button.style.color = "white";
                }

            });

        } else {

            document.querySelectorAll(".answer-button").forEach(button => {

                if (button.textContent.trim() === selectedAnswer) {
                    button.style.backgroundColor = "red";
                    button.style.color = "white";
                }

            });

        }


        
        const resultMessage = document.createElement("p");

        resultMessage.textContent = result.message;

        document.getElementById("quiz").appendChild(resultMessage);


        // Show Next button
        document.getElementById("next-button").style.display = "block";

    } catch (error) {

        console.error(error);

        alert("Something went wrong checking the answer.");

    }
}



function nextQuestion() {

    currentQuestion++;

    if (currentQuestion < questions.length) {

        showQuestion();

    } else {

        showResults();

    }
}



function showResults() {

    const quizDiv = document.getElementById("quiz");

    quizDiv.innerHTML = `
        <h2>Quiz Complete!</h2>

        <p>You scored ${score}/${questions.length}</p>

        <button id="play-again">Play Again</button>
    `;

    document.getElementById("next-button").style.display = "none";

    document
        .getElementById("play-again")
        .addEventListener("click", getQuiz);
}

document
    .getElementById("next-button")
    .addEventListener("click", nextQuestion);

getQuiz();

