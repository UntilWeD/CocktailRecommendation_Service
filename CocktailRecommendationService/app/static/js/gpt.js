document
  .querySelector(".cocktail-in-output")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const user_input = document.querySelector(".cocktail-input").value;

    fetch("/gpt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: user_input,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        // 응답 데이터를 화면에 출력
        const responseDiv = document.querySelector(".cocktail-output");
        if (data.error) {
          responseDiv.textContent = `Error: ${data.error}`;
        } else {
          const gptAnswer = data.answer;
          const replaceMarkdown = gptAnswer
            .replace(/\n/g, "<br>")
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
          responseDiv.innerHTML = JSON.stringify(replaceMarkdown, null, 2);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        document.querySelector(".cocktail-output").innerHTML =
          "An error occurred. Please try again.";
      });
  });
