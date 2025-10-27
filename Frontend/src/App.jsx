import { useState, useEffect } from "react";
import InterfaceArea from "./component/interfacearea";
import Login from "./pages/login";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Navigate, useLocation } from "react-router-dom";
import axios from "axios";

function CheckAuth({ children }) {
  const location = useLocation();
  const [authStatus, setAuthStatus] = useState(false);

  useEffect(() => {
    let active = true;
    const verifyAuth = async () => {
      try {
        await axios.get("http://127.0.0.1:8005/users/", {
          withCredentials: true,
        });
        if (active) setAuthStatus(true);
      } catch (error) {
        if (active) setAuthStatus(false);
      }
    };
    verifyAuth();
    return () => {
      active = false;
    };
  }, [location.pathname]);

  

  if (authStatus) {
    // logged in
    if (location.pathname === "/login") {
      return <Navigate to="/app" replace />;
    }
    return children;
  } else {
    // not logged in
    if (location.pathname !== "/login") {
      return <Navigate to="/login" replace />;
    }
    return children;
  }
}

function Main() {
  return (
    <div className="Main">
      <InterfaceArea />
    </div>
  );
}

function home() {
  return <div> Home </div>;
}

export default function App() {
  return (
    <Router>
      <nav>
        <Link to="/login">Login</Link> | <Link to="/app">app</Link>
      </nav>
      <Routes>
        <Route
          path="/login"
          element={
            <CheckAuth>
              {" "}
              <Login />{" "}
            </CheckAuth>
          }
        />
        <Route
          path="/app"
          element={
           <CheckAuth>
            <Main />
        </CheckAuth>

          }
        />
      </Routes>
    </Router>
  );
}
