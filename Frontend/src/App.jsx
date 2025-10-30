import { useState, useEffect } from "react";
import Home from "./pages/home"
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
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
    if (location.pathname === "/login"|| location.pathname === '/') {
      return <Navigate to="/app" replace />;
    }
    return children;
  } else {
    // not logged in
      return <Navigate to="/login" replace />;

  }
}





export default function App() {
  return (<Router>
      <Routes>
        

        <Route
          path="/"
          element={
            <CheckAuth>
            <Dashboard />
            </CheckAuth>}
        />
        

        <Route
          path="/login"
          element={
            <CheckAuth>
            <Login />
          </CheckAuth>
          }
        />
        

        <Route
          path="/app"
          element={
            <CheckAuth>
              <Home />
            </CheckAuth>
          }
        />
        
      </Routes>
    </Router>);
}
