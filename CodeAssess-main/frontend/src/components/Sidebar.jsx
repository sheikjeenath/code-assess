import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Code2,
  History,
  User,
  Settings,
  ShieldCheck
} from 'lucide-react';

export const Sidebar = () => {
  const { currentUser, isAdmin } = useAuth();

  if (!currentUser) return null;

  const links = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/problems', label: 'Problems', icon: Code2 },
    { to: '/submissions', label: 'My Submissions', icon: History },
    { to: '/profile', label: 'Profile', icon: User },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  const activeClass = 'flex items-center space-x-3 px-4 py-3 rounded-lg text-primary bg-primary/10 border-l-2 border-primary font-medium transition-all duration-200';
  const inactiveClass = 'flex items-center space-x-3 px-4 py-3 rounded-lg text-dark-text-secondary hover:text-dark-text-primary hover:bg-dark-surface/50 border-l-2 border-transparent transition-all duration-200';

  return (
    <aside className="w-64 border-r border-dark-border bg-dark-surface/30 h-[calc(100vh-73px)] sticky top-[73px] flex flex-col justify-between py-6 px-4 shrink-0">
      <div className="space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => (isActive ? activeClass : inactiveClass)}
            >
              <Icon className="h-5 w-5" />
              <span>{link.label}</span>
            </NavLink>
          );
        })}

        {isAdmin && (
          <NavLink
            to="/admin"
            className={({ isActive }) => (isActive ? activeClass : inactiveClass)}
          >
            <ShieldCheck className="h-5 w-5 text-yellow-500" />
            <span className="text-yellow-500">Admin Panel</span>
          </NavLink>
        )}
      </div>

      <div className="px-4 py-3 border border-dark-border rounded-lg bg-dark-card/50">
        <p className="text-xs text-dark-text-muted font-medium">Logged in as</p>
        <p className="text-xs text-dark-text-secondary truncate mt-0.5">{currentUser.email}</p>
        {isAdmin && (
          <span className="inline-block mt-2 px-2 py-0.5 text-[10px] font-semibold text-yellow-500 bg-yellow-500/10 border border-yellow-500/20 rounded">
            Platform Admin
          </span>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
