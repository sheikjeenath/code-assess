import React from 'react';

export const Button = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  className = '',
  disabled = false,
  loading = false,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg text-sm px-4 py-2.5 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-dark-bg disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer active:scale-97';
  
  const variants = {
    primary: 'bg-primary hover:bg-primary-hover text-white focus:ring-primary shadow-lg shadow-primary/10',
    secondary: 'bg-dark-card hover:bg-dark-border text-dark-text-primary border border-dark-border focus:ring-dark-border',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 shadow-lg shadow-red-500/10',
    outline: 'bg-transparent hover:bg-dark-surface/50 text-dark-text-primary border border-dark-border hover:border-primary/50 focus:ring-primary',
    ghost: 'bg-transparent hover:bg-dark-surface/40 text-dark-text-secondary hover:text-dark-text-primary border-none focus:ring-transparent'
  };

  const spinner = (
    <svg className="animate-spin -ml-1 mr-2 h-4.5 w-4.5 text-current" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    </svg>
  );

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {loading && spinner}
      {children}
    </button>
  );
};

export default Button;
