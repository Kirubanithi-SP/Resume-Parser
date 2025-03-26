// frontend/src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/authService'; // Adjust path if needed

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('authToken'));
  const [isLoading, setIsLoading] = useState(true); // Start loading until initial check is done
  // const [user, setUser] = useState(null); // Optional: Store user details

  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        try {
          // Optional but recommended: Verify token with backend on initial load
          const userData = await authService.verifyToken();
          if (userData) {
              setToken(storedToken);
              setIsAuthenticated(true);
              // setUser(userData); // Set user if needed
          } else {
              // Token invalid or expired
              handleLogout();
          }
        } catch (error) {
          // Verification failed
          handleLogout();
        }
      } else {
        setIsAuthenticated(false);
      }
      setIsLoading(false); // Auth check finished
    };

    checkAuth();
  }, []);

  const handleLogin = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
    setIsAuthenticated(true);
    // You might want to fetch user details here too
    // setIsLoading(false); // Ensure loading is false after login
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setIsAuthenticated(false);
    // setUser(null);
  };

  const value = {
    token,
    isAuthenticated,
    isLoading,
    // user,
    login: handleLogin,
    logout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};