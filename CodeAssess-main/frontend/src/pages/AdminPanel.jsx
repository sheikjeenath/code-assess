import React from 'react';
import Card from '../components/Card';

export const AdminPanel = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Admin Console</h1>
      <Card className="h-64 flex items-center justify-center text-dark-text-secondary text-sm">
        Admin dashboard, user controls, prompts and test cases CRUD will be enabled in Phase 7.
      </Card>
    </div>
  );
};

export default AdminPanel;
