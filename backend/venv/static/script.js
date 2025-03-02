async function generateProblem() {
    const problemType = document.getElementById("problem-type").value;
    const response = await fetch(`/generate?type=${problemType}`);
    const data = await response.json();

    document.getElementById("problem-text").textContent = data.description;
    document.getElementById("data-container").innerHTML = data.details;

    if (problemType === "transportation") {
        document.getElementById("solution-steps").innerHTML = `<h2>Решение</h2><p>${data.solution_steps}</p>`;
    } else {
        document.getElementById("solution-steps").innerHTML = "";
    }

    document.getElementById("problem-container").style.display = "block";
}
