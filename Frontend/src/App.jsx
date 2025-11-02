import { useState, useEffect } from "react";
import Home from "./pages/home"
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Navigate, useLocation } from "react-router-dom";
import axios from "axios";

function useAuth() {
  const [authStatus, setAuthStatus] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation(); 
  useEffect(() => {
    let active = true;
    const verifyAuth = async () => {
      setIsLoading(true);
      try {
        await axios.get(`${process.env.REACT_APP_BACKEND_URL}/users/`, {
          withCredentials: true,
        });
        if (active) setAuthStatus(true);
      } catch (error) {
        if (active) setAuthStatus(false);
      } finally {
        if (active) setIsLoading(false);
      }
    };
    verifyAuth();
    return () => {
      active = false;
    };
  }, [location.pathname]); 
  return { authStatus, isLoading };
}

function PrivateRoute({ children }) {
  const { authStatus, isLoading } = useAuth();
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (!authStatus) {
    return <Navigate to="/login" replace />;
  }
  return children;
}



function PublicOnlyRoute({ children }) {
  const { authStatus, isLoading } = useAuth();
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (authStatus) {
    return <Navigate to="/app" replace />;
  }
  return children;
}

  




export default function App() {
  return (
  
 <Router>
  <Routes>
      <Route
          path="/"
          element={
            <PublicOnlyRoute>
              <Dashboard />
            </PublicOnlyRoute>
          }
        />
        
        <Route
          path="/login"
          element={
            <PublicOnlyRoute>
              <Login />
            </PublicOnlyRoute>
          }
        />
        
        {/* --- Private Route --- */}
        <Route
          path="/app"
          element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          }
        />
        
      </Routes>
    </Router>
  );
}

