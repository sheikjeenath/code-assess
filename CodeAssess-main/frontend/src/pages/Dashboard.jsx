import React from 'react';
import Card from '../components/Card';

export const Dashboard = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-dark-text-secondary mt-1">Review your coding statistics, progress, and AI quality scores.</p>
        </div>
      </div>
      
      <div className="grid md:grid-cols-4 gap-6">
        <Card>
          <h3 className="text-sm font-semibold text-dark-text-secondary uppercase">Problems Solved</h3>
          <p className="text-4xl font-extrabold text-primary mt-2">0</p>
        </Card>
        <Card>
          <h3 className="text-sm font-semibold text-dark-text-secondary uppercase">Success Rate</h3>
          <p className="text-4xl font-extrabold text-green-500 mt-2">0%</p>
        </Card>
        <Card>
          <h3 className="text-sm font-semibold text-dark-text-secondary uppercase">Avg AI Quality Score</h3>
          <p className="text-4xl font-extrabold text-blue-400 mt-2">0</p>
        </Card>
        <Card>
          <h3 className="text-sm font-semibold text-dark-text-secondary uppercase">Submissions</h3>
          <p className="text-4xl font-extrabold text-yellow-500 mt-2">0</p>
        </Card>
      </div>

      <Card className="h-64 flex items-center justify-center text-dark-text-secondary text-sm">
        No submission history recorded yet. Open the Problems tab to start practicing!
      </Card>
    </div>
  );
};

export default Dashboard;
