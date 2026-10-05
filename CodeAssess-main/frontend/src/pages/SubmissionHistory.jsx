import React from 'react';
import Card from '../components/Card';

export const SubmissionHistory = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Submission History</h1>
      <Card className="h-64 flex items-center justify-center text-dark-text-secondary text-sm">
        List of all submissions will be loaded in Phase 7.
      </Card>
    </div>
  );
};

export default SubmissionHistory;
