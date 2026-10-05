import React from 'react';
import Card from '../components/Card';

export const Settings = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Platform Settings</h1>
      <Card className="h-64 flex items-center justify-center text-dark-text-secondary text-sm">
        Platform preferences will be configured in Phase 7.
      </Card>
    </div>
  );
};

export default Settings;
