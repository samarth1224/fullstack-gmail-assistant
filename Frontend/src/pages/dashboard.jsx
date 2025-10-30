import "./css/dashboard.css"; 
import {useNavigate} from "react-router-dom";

function BannerArea() {
  return (
    <div className="banner-area">
      <h1>
        AI Chatbot
      </h1>
      <p className="banner-subtitle">Our most intelligent AI models</p>{" "}

    </div>
  );
}

function ButtonArea() {
    const navigate = useNavigate();

  return (
    <div className="button-area">

      <button className="btn btn-primary" onClick={()=>{navigate('/app')}}>
        Chat with AI 
      </button>

      <button className="btn btn-secondary" onClick={()=>{navigate('/login')}}>
        Login
      </button>
    </div>
  ); 
}

export default function Dashboard() {
  return (
    <div className="Dashboard">
      <BannerArea />
      <ButtonArea />
    </div>
  );
}
