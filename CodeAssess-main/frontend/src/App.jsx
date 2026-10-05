import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import Dashboard from './pages/Dashboard';
import ProblemList from './pages/ProblemList';
import ProblemDetails from './pages/ProblemDetails';
import CodingWorkspace from './pages/CodingWorkspace';
import SubmissionHistory from './pages/SubmissionHistory';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import AdminPanel from './pages/AdminPanel';

import './App.css';

// Protected Route Wrapper
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!currentUser) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

// Admin Route Wrapper
const AdminRoute = ({ children }) => {
  const { currentUser, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Main Layout Wrapper
const Layout = () => {
  const { currentUser } = useAuth();
  const location = useLocation();

  // Pages that do not require navigation sidebar/navbar
  const cleanPages = ['/', '/login', '/register', '/forgot-password'];
  const showNavOnly = cleanPages.includes(location.pathname);

  if (showNavOnly) {
    return (
      <div className="flex flex-col min-h-screen bg-dark-bg text-dark-text-primary">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
          </Routes>
        </main>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-dark-bg text-dark-text-primary">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-h-[calc(100vh-73px)]">
          <Routes>
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/problems"
              element={
                <ProtectedRoute>
                  <ProblemList />
                </ProtectedRoute>
              }
            />
            <Route
              path="/problems/:problemId"
              element={
                <ProtectedRoute>
                  <ProblemDetails />
                </ProtectedRoute>
              }
            />
            <Route
              path="/workspace/:problemId"
              element={
                <ProtectedRoute>
                  <CodingWorkspace />
                </ProtectedRoute>
              }
            />
            <Route
              path="/submissions"
              element={
                <ProtectedRoute>
                  <SubmissionHistory />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <Settings />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <AdminPanel />
                </AdminRoute>
              }
            />
            {/* Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Layout />
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
