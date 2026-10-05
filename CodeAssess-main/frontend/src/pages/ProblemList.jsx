import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { problemsApi } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { Search, Filter, ChevronRight, CheckCircle2, Clock, AlertCircle } from 'lucide-react';

const DIFFICULTY_COLORS = {
  Easy: 'text-green-400 bg-green-400/10 border-green-400/20',
  Medium: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
  Hard: 'text-red-400 bg-red-400/10 border-red-400/20',
};

const DIFFICULTY_DOT = {
  Easy: 'bg-green-400',
  Medium: 'bg-yellow-400',
  Hard: 'bg-red-400',
};

export const ProblemList = () => {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchParams, setSearchParams] = useSearchParams();

  const searchQuery = searchParams.get('q') || '';
  const difficultyFilter = searchParams.get('difficulty') || 'All';
  const tagFilter = searchParams.get('tag') || 'All';

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        setLoading(true);
        const data = await problemsApi.list();
        setProblems(data.problems || []);
      } catch (err) {
        setError(err.message || 'Failed to load problems');
      } finally {
        setLoading(false);
      }
    };
    fetchProblems();
  }, []);

  // Compute unique tags from all problems
  const allTags = ['All', ...new Set(problems.flatMap((p) => p.tags || []))];

  // Apply filters
  const filtered = problems.filter((p) => {
    const matchesSearch =
      !searchQuery ||
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.tags || []).some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesDiff = difficultyFilter === 'All' || p.difficulty === difficultyFilter;
    const matchesTag = tagFilter === 'All' || (p.tags || []).includes(tagFilter);
    return matchesSearch && matchesDiff && matchesTag;
  });

  const updateFilter = (key, value) => {
    const params = new URLSearchParams(searchParams);
    if (value === 'All' || value === '') {
      params.delete(key);
    } else {
      params.set(key, value);
    }
    setSearchParams(params);
  };

  const counts = {
    Easy: problems.filter((p) => p.difficulty === 'Easy').length,
    Medium: problems.filter((p) => p.difficulty === 'Medium').length,
    Hard: problems.filter((p) => p.difficulty === 'Hard').length,
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between pb-4 border-b border-dark-border">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Coding Challenges</h1>
          <p className="text-dark-text-secondary mt-1">
            {problems.length} problems across Easy, Medium, and Hard difficulties
          </p>
        </div>
        <div className="flex gap-3 mt-4 md:mt-0">
          {['Easy', 'Medium', 'Hard'].map((d) => (
            <div
              key={d}
              className={`px-3 py-1.5 rounded-lg border text-xs font-semibold ${DIFFICULTY_COLORS[d]}`}
            >
              {d}: {counts[d]}
            </div>
          ))}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-dark-text-muted" />
          <input
            type="text"
            placeholder="Search problems or tags..."
            value={searchQuery}
            onChange={(e) => updateFilter('q', e.target.value)}
            className="glass-input w-full pl-10 pr-4 py-2.5 rounded-lg text-sm"
          />
        </div>

        {/* Difficulty Filter */}
        <select
          value={difficultyFilter}
          onChange={(e) => updateFilter('difficulty', e.target.value)}
          className="glass-input px-3 py-2.5 rounded-lg text-sm min-w-[140px] cursor-pointer"
        >
          <option value="All">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>

        {/* Tag Filter */}
        <select
          value={tagFilter}
          onChange={(e) => updateFilter('tag', e.target.value)}
          className="glass-input px-3 py-2.5 rounded-lg text-sm min-w-[140px] cursor-pointer"
        >
          {allTags.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>

      {/* Content */}
      {loading ? (
        <LoadingSkeleton variant="table" />
      ) : error ? (
        <div className="flex items-center gap-3 bg-red-950/30 border border-red-500/30 rounded-xl p-6 text-red-400">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{error}</span>
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20 text-dark-text-muted">
          <Filter className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p className="text-lg font-medium">No problems match your filters</p>
          <p className="text-sm mt-1">Try changing your search or filter criteria</p>
        </div>
      ) : (
        <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden">
          {/* Table header */}
          <div className="grid grid-cols-12 gap-4 px-6 py-3 border-b border-dark-border text-xs font-semibold text-dark-text-muted uppercase tracking-wider">
            <div className="col-span-1">#</div>
            <div className="col-span-5">Title</div>
            <div className="col-span-2">Difficulty</div>
            <div className="col-span-3">Tags</div>
            <div className="col-span-1"></div>
          </div>

          {/* Rows */}
          {filtered.map((problem, idx) => (
            <Link
              key={problem.id}
              to={`/problems/${problem.id}`}
              className="grid grid-cols-12 gap-4 px-6 py-4 border-b border-dark-border/50 last:border-0 hover:bg-dark-surface/40 transition-colors group items-center"
            >
              <div className="col-span-1 text-dark-text-muted text-sm font-mono">{idx + 1}</div>
              <div className="col-span-5">
                <span className="font-semibold text-dark-text-primary group-hover:text-primary transition-colors">
                  {problem.title}
                </span>
              </div>
              <div className="col-span-2">
                <span
                  className={`inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-semibold border ${DIFFICULTY_COLORS[problem.difficulty]}`}
                >
                  <span className={`w-1.5 h-1.5 rounded-full ${DIFFICULTY_DOT[problem.difficulty]}`} />
                  {problem.difficulty}
                </span>
              </div>
              <div className="col-span-3 flex flex-wrap gap-1">
                {(problem.tags || []).slice(0, 3).map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-0.5 text-xs rounded bg-dark-surface border border-dark-border text-dark-text-secondary"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <div className="col-span-1 flex justify-end">
                <ChevronRight className="h-4 w-4 text-dark-text-muted group-hover:text-primary transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProblemList;
