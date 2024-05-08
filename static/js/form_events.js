const constructToast = (message, type) => {
  var toastBody = document.createElement("div");
  toastBody.setAttribute("class", "toast-body");
  toastBody.textContent = message;

  var toastButton = document.createElement("button");
  toastButton.setAttribute("type", "button");
  toastButton.setAttribute("class", "btn-close me-2 m-auto");
  toastButton.setAttribute("data-bs-dismiss", "toast");
  toastButton.setAttribute("aria-label", "Close");

  var toastFlex = document.createElement("div");
  toastFlex.setAttribute("class", "d-flex");
  toastFlex.append(toastBody);
  toastFlex.append(toastButton);

  var toast = document.createElement("div");
  toast.setAttribute("class", `toast bg-${type} text-white`);
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");
  toast.append(toastFlex);

  return toast;
};

const showToast = (message, type) => {
  var toast = constructToast(message, type);
  const toastWrapper = document.getElementById("toast-wrapper");
  toastWrapper.append(toast);
  var toastEl = new bootstrap.Toast(toast);
  toastEl.show();
};

const login = () => {
  let username = document.getElementById("floatingInput").value;
  let password = document.getElementById("floatingPassword").value;

  if (!username || !password) {
    showToast("Please fill in all fields", "danger");
    return;
  }

  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((res) => {
      if (res.status === 200) {
        res.json().then((data) => {
          document.cookie = `token=${data["token"]};`;
          showToast("Logged in successfully.", "success");
        });
      } else {
        res.json().then((data) => {
          showToast(data["error"], "danger");
        });
      }
    })
    .catch((err) => {
      if (err) {
        console.log(err);
      }
    });
};

const register = () => {
  let username = document.getElementById("floatingInput").value;
  let password = document.getElementById("floatingPassword").value;

  if (!username || !password) {
    showToast("Please fill in all fields", "danger");
    return;
  }

  fetch("/api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((res) => {
      if (res.status === 201) {
        showToast("User created successfully.", "success");
      } else {
        res.json().then((data) => {
          showToast(data["error"], "danger");
        });
      }
    })
    .catch((err) => {
      if (err) {
        console.log(err);
      }
    });
};
