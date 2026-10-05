import React from 'react';

export const Card = ({
  children,
  className = '',
  hoverEffect = false,
  ...props
}) => {
  return (
    <div
      className={`bg-dark-card border border-dark-border rounded-xl p-6 transition-all duration-300 ${
        hoverEffect ? 'hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-0.5' : ''
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
