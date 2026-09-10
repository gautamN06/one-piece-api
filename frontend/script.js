const API_URL = "http://127.0.0.1:8000"

let questions = [];
let currentQuestion = 0;
let score = 0;

let allCharacters = [];

const quizSection = document.getElementById("quiz-section");
const charactersSection = document.getElementById("characters-section");

function hideSections() {
    quizSection.style.display = "none";
    charactersSection.style.display = "none";
}

function showHome() {
    hideSections();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    setActiveNav("Home");
}

function showQuiz() {
    hideSections();

    quizSection.style.display = "block";

    quizSection.scrollIntoView({
        behavior: "smooth"
    });

    setActiveNav("Quiz");

    getQuiz();
}

function showCharacters() {
    hideSections();

    charactersSection.style.display = "block";

    charactersSection.scrollIntoView({
        behavior: "smooth"
    });

    setActiveNav("Characters");

    loadCharacters();
}

function setActiveNav(pageName) {
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(link => {
        link.classList.remove("active");

        if (link.textContent.trim() === pageName) {
            link.classList.add("active");
        }
    });
}


const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(link => {

    link.addEventListener("click", function(event) {

        event.preventDefault();

        const page = link.textContent.trim();

        if (page === "Home") {
            showHome();
        }

        if (page === "Quiz") {
            showQuiz();
        }

        if (page === "Characters") {
            showCharacters();
        }

    });

});



document
    .getElementById("start-quiz-button")
    .addEventListener("click", showQuiz);


document
    .getElementById("characters-button")
    .addEventListener("click", showCharacters);


async function getQuiz() {

    try {

        const response = await fetch(`${API_URL}/quiz`);

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

        <h2>
            Question ${currentQuestion + 1}/${questions.length}
        </h2>

        <p>
            ${question.question}
        </p>

        <div class="answers">

            ${question.answers.map(answer => `
                <button class="answer-button">
                    ${answer}
                </button>
            `).join("")}

        </div>
    `;


    const answerButtons =
        document.querySelectorAll(".answer-button");


    answerButtons.forEach(button => {

        button.addEventListener("click", () => {

            checkAnswer(
                question,
                button.textContent.trim(),
                button
            );

        });

    });


    document.getElementById("next-button").style.display = "none";
}


async function checkAnswer(
    question,
    selectedAnswer,
    selectedButton
) {

    try {

        const response = await fetch(
            `${API_URL}/quiz/answer`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    character_id: question.character_id,

                    question_type: question.question_type,

                    answer: selectedAnswer

                })
            }
        );


        if (!response.ok) {
            throw new Error("Could not check answer");
        }


        const result = await response.json();



        const answerButtons =
            document.querySelectorAll(".answer-button");

        answerButtons.forEach(button => {
            button.disabled = true;
        });



        if (result.correct) {

            score++;

            selectedButton.style.background = "#22c55e";
            selectedButton.style.color = "white";
            selectedButton.style.borderColor = "#22c55e";

        }

  

        else {

            selectedButton.style.background = "#ef4444";
            selectedButton.style.color = "white";
            selectedButton.style.borderColor = "#ef4444";

        }



        const resultMessage =
            document.createElement("p");

        resultMessage.className = "result-message";

        resultMessage.textContent = result.message;


        if (!result.correct) {

            resultMessage.textContent +=
                ` Correct answer: ${result.correct_answer}`;

        }


        document
            .getElementById("quiz")
            .appendChild(resultMessage);


        // Show next button

        document.getElementById("next-button").style.display = "block";


    } catch (error) {

        console.error(error);

        alert(
            "Something went wrong checking the answer."
        );

    }

}

function nextQuestion() {

    currentQuestion++;


    if (currentQuestion < questions.length) {

        showQuestion();

    }

    else {

        showResults();

    }

}

function showResults() {

    const quizDiv =
        document.getElementById("quiz");


    quizDiv.innerHTML = `

        <div class="results">

            <h2>Quiz Complete!</h2>

            <p>
                You scored
                <strong>${score}/${questions.length}</strong>
            </p>

            <button id="play-again">
                Play Again
            </button>

        </div>

    `;


    document.getElementById("next-button").style.display =
        "none";


    document
        .getElementById("play-again")
        .addEventListener("click", getQuiz);

}



document
    .getElementById("next-button")
    .addEventListener(
        "click",
        nextQuestion
    );


hideSections();


async function loadCharacters() {

    const results =
        document.getElementById("character-results");

    results.innerHTML = `
        <p class="loading-message">
            Loading characters...
        </p>
    `;

    try {

        const response =
            await fetch(`${API_URL}/characters`);


        if (!response.ok) {
            throw new Error("Could not load characters");
        }


        allCharacters =
            await response.json();


        populateFilters(allCharacters);

        displayCharacters(allCharacters);


    } catch (error) {

        console.error(error);

        results.innerHTML = `
            <p class="no-results">
                Failed to load characters.
            </p>
        `;

    }
}

function displayCharacters(characters) {

    const results =
        document.getElementById("character-results");


    if (characters.length === 0) {

        results.innerHTML = `
            <p class="no-results">
                No characters found.
            </p>
        `;

        return;
    }


    results.innerHTML = characters.map(character => {

        const bounty = character.bounty
            ? `฿${character.bounty.toLocaleString()}`
            : "Unknown";


        return `

            <div class="character-card">

                <div class="character-image-container">

                    <img
                        src="${character.image_url || "default-character.png"}"
                        alt="${character.name}"
                        class="character-image"
                        onerror="this.onerror=null; this.src='default-character.png'"
                    >

                </div>


                <div 
                    class="character-card-content"
                    onClick="showCharacterDetails(${character.id})"
                >

                    <h3>
                        ${character.name}
                    </h3>


                    <p class="character-info">
                        <strong>Age:</strong>
                        ${character.age ?? "Unknown"}
                    </p>


                    <p class="character-info">
                        <strong>Affiliation:</strong>
                        ${character.affiliation ?? "Unknown"}
                    </p>


                    <p class="character-info">
                        <strong>Crew:</strong>
                        ${character.crew ?? "None"}
                    </p>


                    <p class="character-info">
                        <strong>Devil Fruit:</strong>
                        ${character.devil_fruit ?? "None"}
                    </p>


                    <p class="character-info bounty">
                        <strong>Bounty:</strong>
                        ${bounty}
                    </p>


                    <span class="status-badge">
                        ${character.status ?? "Unknown"}
                    </span>

                </div>

            </div>

        `;

    }).join("");

}



function searchCharacters() {

    const searchInput =
        document.getElementById("character-search");


    const searchTerm =
        searchInput.value
            .trim()
            .toLowerCase();


    if (searchTerm === "") {

        displayCharacters(allCharacters);

        return;
    }


    const filteredCharacters =
        allCharacters.filter(character =>

            character.name
                .toLowerCase()
                .includes(searchTerm)

        );


    displayCharacters(filteredCharacters);

}

function populateFilters(characters) {

    const crewFilter =
        document.getElementById("crew-filter");

    const affiliationFilter =
        document.getElementById("affiliation-filter");


    const crews = [
        ...new Set(
            characters
                .map(character => character.crew)
                .filter(Boolean)
        )
    ].sort();


    const affiliations = [
        ...new Set(
            characters
                .map(character => character.affiliation)
                .filter(Boolean)
        )
    ].sort();


    crewFilter.innerHTML =
        `<option value="">All Crews</option>` +
        crews.map(crew => `
            <option value="${crew}">
                ${crew}
            </option>
        `).join("");


    affiliationFilter.innerHTML =
        `<option value="">All Affiliations</option>` +
        affiliations.map(affiliation => `
            <option value="${affiliation}">
                ${affiliation}
            </option>
        `).join("");
}

async function filterCharacters() {

    const results =
        document.getElementById("character-results");

    results.innerHTML = `
        <p class="loading-message">
            Loading...
        </p>
    `;


    try {

        const searchTerm =
            document
                .getElementById("character-search")
                .value
                .trim()
                .toLowerCase();


        const crew =
            document.getElementById("crew-filter").value;


        const affiliation =
            document.getElementById("affiliation-filter").value;


        const params =
            new URLSearchParams();


        if (crew) {
            params.append("crew", crew);
        }


        if (affiliation) {
            params.append("affiliation", affiliation);
        }


        const queryString =
            params.toString();


        const url =
            queryString
                ? `${API_URL}/characters?${queryString}`
                : `${API_URL}/characters`;


        const response =
            await fetch(url);


        if (!response.ok) {
            throw new Error("Could not filter characters");
        }


        let characters =
            await response.json();


        /*
         * Search is currently performed
         * in the browser.
         *
         * Crew and affiliation are
         * handled by the backend.
         */

        if (searchTerm) {

            characters =
                characters.filter(character =>
                    character.name
                        .toLowerCase()
                        .includes(searchTerm)
                );

        }


        displayCharacters(characters);


    } catch (error) {

        console.error(error);

        results.innerHTML = `
            <p class="no-results">
                Failed to filter characters.
            </p>
        `;

    }
}

function showCharacterDetails(characterId) {

    const character =
        allCharacters.find(
            character => character.id === characterId
        );


    if (!character) {
        return;
    }


    const bounty =
        character.bounty
            ? `฿${character.bounty.toLocaleString()}`
            : "Unknown";


    const results =
        document.getElementById("character-results");


    results.innerHTML = `

        <div class="character-detail">

            <button
                class="back-button"
                onclick="loadCharacters()"
            >
                ← Back to Characters
            </button>


            <div class="character-detail-content">

                <div class="character-detail-image">

                    <img
                        src="${character.image_url || "default-character.png"}"
                        alt="${character.name}"
                        onerror="this.onerror=null; this.src='default-character.png';"
                    >

                </div>


                <div class="character-detail-info">

                    <p class="detail-label">
                        ONE PIECE CHARACTER
                    </p>

                    <h2>
                        ${character.name}
                    </h2>


                    <div class="detail-stat">
                        <span>Age</span>
                        <strong>
                            ${character.age ?? "Unknown"}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Affiliation</span>
                        <strong>
                            ${character.affiliation ?? "Unknown"}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Crew</span>
                        <strong>
                            ${character.crew ?? "None"}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Devil Fruit</span>
                        <strong>
                            ${character.devil_fruit ?? "None"}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Type</span>
                        <strong>
                            ${character.devil_fruit_type ?? "None"}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Bounty</span>
                        <strong>
                            ${bounty}
                        </strong>
                    </div>


                    <div class="detail-stat">
                        <span>Status</span>
                        <strong>
                            ${character.status ?? "Unknown"}
                        </strong>
                    </div>

                </div>

            </div>

        </div>

    `;
}



document
    .getElementById("search-button")
    .addEventListener(
        "click",
        filterCharacters 
    );



document
    .getElementById("character-search")
    .addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                filterCharacters();

            }

        }
    );

document
    .getElementById("crew-filter")
    .addEventListener(
        "change",
        filterCharacters
    );


document
    .getElementById("affiliation-filter")
    .addEventListener(
        "change",
        filterCharacters
    );