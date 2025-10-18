import { useState } from "react";
import "./css/infoarea.css";

export default function InfoArea() {
  const [logIn, setLogIn] = useState(false);

  return (
    <div className="info-area">
      <div className="model">Model=Gemini 2.5 flash</div>
      <div className="login"></div>
    </div>
  );
}
