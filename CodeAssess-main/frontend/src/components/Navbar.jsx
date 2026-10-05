import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Terminal, User, LogOut, ShieldAlert, ChevronDown } from 'lucide-react';
import Button from './Button';

export const Navbar = () => {
  const { currentUser, isAdmin, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Failed to log out', error);
    }
  };

  return (
    <nav className="glass-panel sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-dark-border">
      {/* Brand Logo */}
      <Link to="/" className="flex items-center space-x-2 group">
        <div className="bg-primary/20 p-2 rounded-lg border border-primary/40 group-hover:border-primary transition-all duration-300">
          <Terminal className="h-6 w-6 text-primary group-hover:scale-110 transition-transform duration-300" />
        </div>
        <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-dark-text-secondary bg-clip-text text-transparent">
          Code<span className="text-primary">Assess</span>
        </span>
      </Link>

      {/* Action Navigation */}
      <div className="flex items-center space-x-4">
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2.5 rounded-lg border border-dark-border bg-dark-card hover:bg-dark-surface text-dark-text-secondary hover:text-dark-text-primary transition-colors cursor-pointer"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun className="h-4.5 w-4.5" /> : <Moon className="h-4.5 w-4.5" />}
        </button>

        {currentUser ? (
          <div className="relative">
            {/* User Dropdown Button */}
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center space-x-2 px-3 py-1.5 rounded-lg border border-dark-border bg-dark-card hover:bg-dark-surface text-dark-text-primary transition-colors cursor-pointer"
            >
              <div className="h-6 w-6 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center text-xs font-semibold text-primary">
                {currentUser.email ? currentUser.email[0].toUpperCase() : 'U'}
              </div>
              <span className="text-sm max-w-[120px] truncate hidden md:inline">
                {currentUser.displayName || currentUser.email}
              </span>
              <ChevronDown className={`h-4 w-4 text-dark-text-secondary transition-transform duration-200 ${dropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown Options */}
            {dropdownOpen && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setDropdownOpen(false)}
                />
                <div className="absolute right-0 mt-2 w-52 rounded-lg border border-dark-border bg-dark-card shadow-xl py-1 z-20 animate-fade-in">
                  <div className="px-4 py-2 border-b border-dark-border">
                    <p className="text-xs text-dark-text-muted truncate">Signed in as</p>
                    <p className="text-sm text-dark-text-primary truncate font-medium">{currentUser.email}</p>
                  </div>

                  {isAdmin && (
                    <Link
                      to="/admin"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center space-x-2 px-4 py-2 text-sm text-yellow-500 hover:bg-dark-surface transition-colors"
                    >
                      <ShieldAlert className="h-4 w-4" />
                      <span>Admin Control Panel</span>
                    </Link>
                  )}

                  <Link
                    to="/profile"
                    onClick={() => setDropdownOpen(false)}
                    className="flex items-center space-x-2 px-4 py-2 text-sm text-dark-text-secondary hover:text-dark-text-primary hover:bg-dark-surface transition-colors"
                  >
                    <User className="h-4 w-4" />
                    <span>My Profile</span>
                  </Link>

                  <button
                    onClick={() => {
                      setDropdownOpen(false);
                      handleLogout();
                    }}
                    className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-red-500 hover:bg-dark-surface transition-colors cursor-pointer text-left"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Sign Out</span>
                  </button>
                </div>
              </>
            )}
          </div>
        ) : (
          <div className="flex items-center space-x-3">
            <Link to="/login" className="text-sm text-dark-text-secondary hover:text-dark-text-primary px-3 py-2 transition-colors">
              Log In
            </Link>
            <Link to="/register">
              <Button variant="primary" className="py-2 px-4">
                Sign Up
              </Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
