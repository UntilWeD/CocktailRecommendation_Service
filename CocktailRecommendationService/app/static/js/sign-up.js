const signUpBtn = document.querySelector(".submit-btn");
const regex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^*])[A-Za-z\d!@#$%^*]{8,20}$/; // 정규 표현식, 영문자, 숫자, 특수문자(!@#$%^*) 포함 8~20자
const password = document.querySelector("#password");
const reEntered = document.querySelector("#verifyPassword");
const pwdFieldState = document.querySelector(".password-state");
const reEnterFieldState = document.querySelector(".reenter-state");

// 비밀번호 유효성 검사 함수
function checkPassword() {
  const passwordValue = password.value; // 현재 비밀번호 값 가져오기

  if (/\s/.test(passwordValue) || !regex.test(passwordValue)) {
    pwdFieldState.style.display = "block";
    pwdFieldState.textContent = "비밀번호가 유효하지 않습니다.";
    pwdFieldState.style.color = "tomato";
  } else {
    pwdFieldState.style.display = "block";
    pwdFieldState.textContent = "유효한 비밀번호입니다.";
    pwdFieldState.style.color = "#168c2c";
  }
  // 비밀번호가 변경되면 재입력 필드도 다시 검증
  verifyPassword();
}

// 비밀번호 재입력 확인 함수
function verifyPassword() {
  const passwordValue = password.value; // 현재 비밀번호 값 가져오기
  const reEnteredValue = reEntered.value; // 현재 재입력 값 가져오기

  if (passwordValue && reEnteredValue && passwordValue !== reEnteredValue) {
    // 모든 입력 값이 있고 비밀번호와 재입력이 다르다면
    reEnterFieldState.textContent = "비밀번호 재입력 부분을 다시 확인해주세요.";
    reEnterFieldState.style.color = "tomato";
  } else if (
    // 모든 입력 값이 있고 비밀번호와 재입력이 같다면
    passwordValue &&
    reEnteredValue &&
    passwordValue === reEnteredValue
  ) {
    reEnterFieldState.textContent = "✅";
  } else {
    reEnterFieldState.textContent = "";
  }
}

password.addEventListener("input", checkPassword);
reEntered.addEventListener("input", verifyPassword);

// 모든 입력이 유효할 때 버튼 활성화
function toggleSignUpButton() {
  const passwordValid =
    regex.test(password.value) && !/\s/.test(password.value);
  const passwordsMatch =
    password.value === reEntered.value && password.value !== "";

  if (passwordValid && passwordsMatch) {
    signUpBtn.disabled = false;
    signUpBtn.style.opacity = "1";
  } else {
    signUpBtn.disabled = true;
    signUpBtn.style.opacity = "0.5";
  }
}

password.addEventListener("input", toggleSignUpButton);
reEntered.addEventListener("input", toggleSignUpButton);

toggleSignUpButton();
