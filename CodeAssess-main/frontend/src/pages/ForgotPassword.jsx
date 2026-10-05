import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Terminal, Mail, AlertCircle, CheckCircle, ArrowLeft } from 'lucide-react';
import Button from '../components/Button';
import GlassCard from '../components/GlassCard';

export const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const { resetPassword } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      return setError('Please enter your email address');
    }
    try {
      setMessage('');
      setError('');
      setLoading(true);
      await resetPassword(email);
      setMessage('A password reset link has been sent to your email.');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to send password reset email. Please try again.');
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
          <h2 className="text-2xl font-bold text-dark-text-primary">Reset password</h2>
          <p className="text-sm text-dark-text-secondary mt-1">We will send a recovery link to your inbox</p>
        </div>

        {/* Errors */}
        {error && (
          <div className="mb-6 flex items-start space-x-2 bg-red-950/40 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm">
            <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Success message */}
        {message && (
          <div className="mb-6 flex items-start space-x-2 bg-green-950/40 border border-green-500/30 text-green-400 p-3 rounded-lg text-sm">
            <CheckCircle className="h-5 w-5 shrink-0 mt-0.5" />
            <span>{message}</span>
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

          <Button type="submit" loading={loading} className="w-full py-3 mt-2">
            Send Reset Link
          </Button>
        </form>

        <p className="mt-8 text-center text-sm text-dark-text-secondary flex justify-center items-center">
          <Link to="/login" className="text-primary hover:text-primary-hover font-semibold flex items-center">
            <ArrowLeft className="h-4 w-4 mr-1.5" />
            Back to Sign In
          </Link>
        </p>
      </GlassCard>
    </div>
  );
};

export default ForgotPassword;
