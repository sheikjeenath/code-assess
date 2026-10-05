import React from 'react';

export const GlassCard = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`glass-card rounded-xl p-6 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default GlassCard;
