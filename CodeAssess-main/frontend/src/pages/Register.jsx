import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Terminal, Lock, Mail, AlertCircle, ArrowRight } from 'lucide-react';
import Button from '../components/Button';
import GlassCard from '../components/GlassCard';

export const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register, loginWithGoogle } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password || !confirmPassword) {
      return setError('Please fill in all fields');
    }
    if (password !== confirmPassword) {
      return setError('Passwords do not match');
    }
    if (password.length < 6) {
      return setError('Password must be at least 6 characters long');
    }
    try {
      setError('');
      setLoading(true);
      await register(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to create account.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      setError('');
      setLoading(true);
      await loginWithGoogle();
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Google authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-6 py-12 bg-dark-bg relative">
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/10 rounded-full blur-[100px] pointer-events-none -z-10" />

      <GlassCard className="w-full max-w-md animate-fade-in p-8 border border-dark-border">
        {/* Brand */}
        <div className="flex flex-col items-center mb-8">
          <div className="bg-primary/20 p-2.5 rounded-lg border border-primary/40 mb-3">
            <Terminal className="h-6 w-6 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-dark-text-primary">Create an account</h2>
          <p className="text-sm text-dark-text-secondary mt-1">Get started with CodeAssess today</p>
        </div>

        {/* Errors */}
        {error && (
          <div className="mb-6 flex items-start space-x-2 bg-red-950/40 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm">
            <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Email input */}
          <div>
            <label className="block text-xs font-semibold text-dark-text-secondary uppercase tracking-wider mb-2">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3.5 h-4.5 w-4.5 text-dark-text-muted" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="glass-input w-full pl-10 pr-4 py-3 rounded-lg text-sm focus:border-primary"
              />
            </div>
          </div>

          {/* Password input */}
          <div>
            <label className="block text-xs font-semibold text-dark-text-secondary uppercase tracking-wider mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 h-4.5 w-4.5 text-dark-text-muted" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="glass-input w-full pl-10 pr-4 py-3 rounded-lg text-sm focus:border-primary"
              />
            </div>
          </div>

          {/* Confirm Password input */}
          <div>
            <label className="block text-xs font-semibold text-dark-text-secondary uppercase tracking-wider mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 h-4.5 w-4.5 text-dark-text-muted" />
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="glass-input w-full pl-10 pr-4 py-3 rounded-lg text-sm focus:border-primary"
              />
            </div>
          </div>

          <Button type="submit" loading={loading} className="w-full py-3 mt-2">
            Create Account
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </form>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-dark-border"></div>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-dark-card px-2 text-dark-text-muted">Or continue with</span>
          </div>
        </div>

        {/* Google sign-in */}
        <Button variant="outline" onClick={handleGoogleSignIn} disabled={loading} className="w-full py-3 flex justify-center items-center">
          <svg className="h-5 w-5 mr-2.5" viewBox="0 0 24 24" fill="none">
            <path
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              fill="#4285F4"
            />
            <path
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              fill="#34A853"
            />
            <path
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              fill="#FBBC05"
            />
            <path
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              fill="#EA4335"
            />
          </svg>
          Google Accounts
        </Button>

        <p className="mt-8 text-center text-sm text-dark-text-secondary">
          Already have an account?{' '}
          <Link to="/login" className="text-primary hover:text-primary-hover font-semibold">
            Sign In
          </Link>
        </p>
      </GlassCard>
    </div>
  );
};

export default Register;
