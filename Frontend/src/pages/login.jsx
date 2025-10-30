import { useNavigate } from "react-router-dom";
import "./css/login.css";
import { useEffect } from "react";
import axios from "axios";


function GoogleLogin() {
 
  const login = async () => {
    window.location.href = "http://127.0.0.1:8005/auth/login";
  };

  return (
    <div>
      {" "}
      <button className="google-sign-in-button" onClick={login}>
        {" "}
        google sign in{" "}
      </button>{" "}
    </div>
  );
}

function LoginBox() {
  return (
    <div className="login-box">
      <GoogleLogin />
      <div> or </div>
      <button> Continue as Guest </button>
      
      
    </div>
  );
}

export default function Login() {
  return (
    <div className="logins">
      <LoginBox />{" "}
    </div>
  );
}
