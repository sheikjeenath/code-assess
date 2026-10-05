import React from 'react';

export const LoadingSkeleton = ({
  variant = 'card',
  className = '',
  count = 1
}) => {
  const items = Array.from({ length: count });

  const skeletons = {
    card: (
      <div className="bg-dark-card border border-dark-border rounded-xl p-6 animate-pulse">
        <div className="h-4 bg-dark-border rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          <div className="h-3 bg-dark-border rounded w-full"></div>
          <div className="h-3 bg-dark-border rounded w-5/6"></div>
          <div className="h-3 bg-dark-border rounded w-4/5"></div>
        </div>
      </div>
    ),
    table: (
      <div className="border border-dark-border rounded-xl p-4 bg-dark-card animate-pulse space-y-4">
        <div className="flex space-x-4 h-6 items-center">
          <div className="h-4 bg-dark-border rounded w-1/4"></div>
          <div className="h-4 bg-dark-border rounded w-1/4"></div>
          <div className="h-4 bg-dark-border rounded w-1/4"></div>
          <div className="h-4 bg-dark-border rounded w-1/4"></div>
        </div>
        <hr className="border-dark-border" />
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="flex space-x-4 h-8 items-center">
            <div className="h-3 bg-dark-border rounded w-1/4"></div>
            <div className="h-3 bg-dark-border rounded w-1/4"></div>
            <div className="h-3 bg-dark-border rounded w-1/4"></div>
            <div className="h-3 bg-dark-border rounded w-1/4"></div>
          </div>
        ))}
      </div>
    ),
    text: (
      <div className="animate-pulse space-y-2.5">
        <div className="h-3 bg-dark-border rounded w-full"></div>
        <div className="h-3 bg-dark-border rounded w-11/12"></div>
        <div className="h-3 bg-dark-border rounded w-4/5"></div>
      </div>
    ),
    editor: (
      <div className="border border-dark-border rounded-xl bg-dark-surface animate-pulse h-96 flex flex-col justify-between p-4">
        <div className="flex justify-between items-center pb-2 border-b border-dark-border">
          <div className="h-6 bg-dark-border rounded w-32"></div>
          <div className="h-6 bg-dark-border rounded w-24"></div>
        </div>
        <div className="flex-1 space-y-4 py-4">
          <div className="h-3 bg-dark-border rounded w-1/3"></div>
          <div className="h-3 bg-dark-border rounded w-1/2"></div>
          <div className="h-3 bg-dark-border rounded w-1/4"></div>
          <div className="h-3 bg-dark-border rounded w-3/4"></div>
          <div className="h-3 bg-dark-border rounded w-2/3"></div>
        </div>
        <div className="flex justify-end space-x-3 pt-2 border-t border-dark-border">
          <div className="h-9 bg-dark-border rounded w-20"></div>
          <div className="h-9 bg-dark-border rounded w-20"></div>
        </div>
      </div>
    )
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {items.map((_, i) => (
        <React.Fragment key={i}>
          {skeletons[variant]}
        </React.Fragment>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
