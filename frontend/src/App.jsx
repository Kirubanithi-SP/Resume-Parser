// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext'; // Import AuthProvider
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';
import Spinner from './components/Spinner';

// A small component to handle initial loading state
function AppContent() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner />
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <main>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
             {/* Default protected route */}
            <Route path="/dashboard" element={<DashboardPage />} />
            {/* Add other protected routes here */}
          </Route>

          {/* Redirect root path */}
          {/* If logged in, go to dashboard, otherwise go to login */}
          <Route
              path="/"
              element={<Navigate to={localStorage.getItem('authToken') ? "/dashboard" : "/login"} replace />}
          />

          {/* Optional: Catch-all route for 404 */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}


function App() {
  return (
    <AuthProvider> {/* Wrap everything with AuthProvider */}
      <Router>
         <AppContent /> {/* Render the content based on loading state */}
      </Router>
    </AuthProvider>
  );
}

export default App;