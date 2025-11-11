import { useNavigate } from "react-router-dom";
import "./css/login.css";
import { useEffect } from "react";
import axios from "axios";


function GoogleLogin() {
 
  const login = async () => {
    window.location.href = `${process.env.REACT_APP_BACKEND_URL}/auth/login`;
  };

  return (
    <div>
      {" "}
      <button className="sign-in-button google" onClick={login}>
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
      <button className="sign-in-button guest"> Continue as Guest </button>
      
      
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
