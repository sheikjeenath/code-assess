import React from "react";

const SubmissionReport = ({ submission }) => {
  if (!submission) return null;

  return (
    <div className="p-4 space-y-6 text-white">
      {/* Overall Score */}
      <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
        <h2 className="text-xl font-bold">Overall Score</h2>

        <p className="text-5xl font-bold text-green-400 mt-2">
          {submission.overallScore ?? "--"}
        </p>

        <p className="mt-2 text-sm text-gray-400">
          Verdict :
          <span className="ml-2 font-semibold text-green-400">
            {submission.status}
          </span>
        </p>
      </div>

      {/* AI Report */}
      {submission.aiReport && (
        <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
          <h2 className="text-lg font-semibold mb-3">
            AI Code Review
          </h2>

          <pre className="whitespace-pre-wrap text-sm">
            {JSON.stringify(submission.aiReport, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default SubmissionReport;