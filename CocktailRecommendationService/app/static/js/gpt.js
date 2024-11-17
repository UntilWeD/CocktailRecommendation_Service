// ChatGPT 연결
const responseDiv = document.querySelector(".cocktail-output");

document
  .querySelector(".cocktail-in-output")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const user_input = document.querySelector(".cocktail-input").value;
    responseDiv.textContent = "ChatGPT가 칵테일을 만들고 있습니다...";
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
          throw new Error(`HTTP error! status: ${response.status}`); // 예외를 강제로 발생
        }
        return response.json();
      })
      .then((data) => {
        // 응답 데이터를 화면에 출력
        if (data.error) {
          responseDiv.textContent = `Error: ${data.error}`;
        } else {
          const gptAnswer = data.answer;
          const replaceMarkdown = marked.parse(gptAnswer);
          const inputField = document.querySelector(".cocktail-input");
          inputField.value = "";
          console.log(replaceMarkdown);
          responseDiv.innerHTML = replaceMarkdown; // json형식으로 문자열화, null -> 특별히 수정X, 2 -> 들여쓰기 2칸
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        document.querySelector(".cocktail-output").innerHTML =
          "에러 발생, 다시 시도해주세요. ";
      });
  });
