import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { problemsApi } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { Code2, ChevronRight, AlertCircle, BookOpen, Cpu, Tag } from 'lucide-react';

const DIFFICULTY_COLORS = {
  Easy: 'text-green-400 bg-green-400/10 border-green-400/20',
  Medium: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
  Hard: 'text-red-400 bg-red-400/10 border-red-400/20',
};

export const ProblemDetails = () => {
  const { problemId } = useParams();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProblem = async () => {
      try {
        setLoading(true);
        const data = await problemsApi.get(problemId);
        setProblem(data);
      } catch (err) {
        setError(err.message || 'Failed to load problem');
      } finally {
        setLoading(false);
      }
    };
    fetchProblem();
  }, [problemId]);

  if (loading) return <LoadingSkeleton variant="card" count={3} />;

  if (error) {
    return (
      <div className="flex items-center gap-3 bg-red-950/30 border border-red-500/30 rounded-xl p-6 text-red-400">
        <AlertCircle className="h-5 w-5 shrink-0" />
        <span>{error}</span>
      </div>
    );
  }

  if (!problem) return null;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Breadcrumb */}
      <nav className="flex items-center text-sm text-dark-text-muted space-x-2">
        <Link to="/problems" className="hover:text-primary transition-colors">Problems</Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-dark-text-primary">{problem.title}</span>
      </nav>

      {/* Problem Header */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-2xl font-bold text-dark-text-primary">{problem.title}</h1>
            <div className="flex items-center flex-wrap gap-3 mt-3">
              <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-semibold border ${DIFFICULTY_COLORS[problem.difficulty]}`}>
                {problem.difficulty}
              </span>
              {(problem.tags || []).map((tag) => (
                <span key={tag} className="flex items-center gap-1 px-2.5 py-1 text-xs rounded bg-dark-surface border border-dark-border text-dark-text-secondary">
                  <Tag className="h-3 w-3" />
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <Link
            to={`/workspace/${problemId}`}
            className="inline-flex items-center gap-2 bg-primary hover:bg-primary-hover text-white font-medium px-5 py-2.5 rounded-lg transition-all duration-200 text-sm shadow-lg shadow-primary/20"
          >
            <Code2 className="h-4 w-4" />
            Solve Challenge
          </Link>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Description */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-dark-card border border-dark-border rounded-xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <BookOpen className="h-5 w-5 text-primary" />
              <h2 className="font-semibold text-dark-text-primary">Problem Description</h2>
            </div>
            <div className="prose prose-invert max-w-none text-dark-text-secondary text-sm leading-relaxed whitespace-pre-wrap">
              {problem.description}
            </div>
          </div>

          {/* Sample Cases */}
          {(problem.sampleCases || []).length > 0 && (
            <div className="bg-dark-card border border-dark-border rounded-xl p-6">
              <h2 className="font-semibold text-dark-text-primary mb-4">Examples</h2>
              <div className="space-y-4">
                {problem.sampleCases.map((tc, idx) => (
                  <div key={idx} className="bg-dark-surface rounded-lg border border-dark-border p-4">
                    <p className="text-xs font-semibold text-dark-text-muted uppercase mb-2">Example {idx + 1}</p>
                    <div className="space-y-2 text-sm font-mono">
                      <div>
                        <span className="text-dark-text-muted">Input: </span>
                        <span className="text-dark-text-primary whitespace-pre-wrap">{tc.input}</span>
                      </div>
                      <div>
                        <span className="text-dark-text-muted">Output: </span>
                        <span className="text-green-400 whitespace-pre-wrap">{tc.output}</span>
                      </div>
                      {tc.explanation && (
                        <div className="mt-2 pt-2 border-t border-dark-border text-dark-text-secondary font-sans text-xs">
                          <span className="font-semibold">Explanation: </span>{tc.explanation}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Constraints */}
          {(problem.constraints || []).length > 0 && (
            <div className="bg-dark-card border border-dark-border rounded-xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Cpu className="h-5 w-5 text-primary" />
                <h2 className="font-semibold text-dark-text-primary">Constraints</h2>
              </div>
              <ul className="space-y-2">
                {problem.constraints.map((c, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-dark-text-secondary font-mono">
                    <span className="text-primary mt-0.5 shrink-0">•</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Languages */}
          <div className="bg-dark-card border border-dark-border rounded-xl p-6">
            <h2 className="font-semibold text-dark-text-primary mb-4">Supported Languages</h2>
            <div className="grid grid-cols-2 gap-2">
              {Object.keys(problem.starterTemplates || { python: '', cpp: '', java: '', javascript: '' }).map((lang) => (
                <div key={lang} className="px-3 py-2 bg-dark-surface border border-dark-border rounded-lg text-xs text-dark-text-secondary text-center capitalize">
                  {lang === 'cpp' ? 'C++' : lang === 'javascript' ? 'JavaScript' : lang.charAt(0).toUpperCase() + lang.slice(1)}
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <Link
            to={`/workspace/${problemId}`}
            className="flex items-center justify-center gap-2 bg-primary hover:bg-primary-hover text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 shadow-lg shadow-primary/20 w-full"
          >
            <Code2 className="h-5 w-5" />
            Open Coding Workspace
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ProblemDetails;
