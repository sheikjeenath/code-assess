import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { problemsApi, submissionsApi } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import SubmissionReport from '../components/SubmissionReport';
import {
  Play, Send, RotateCcw, Upload, Download, Copy, ChevronLeft,
  Terminal, CheckCircle2, XCircle, AlertTriangle, Clock, Cpu,
  ChevronDown, ChevronRight
} from 'lucide-react';

const LANGUAGE_OPTIONS = [
  { id: 'python', label: 'Python' },
  { id: 'cpp', label: 'C++' },
  { id: 'java', label: 'Java' },
  { id: 'javascript', label: 'JavaScript' },
];

const VERDICT_STYLES = {
  'Accepted': { color: 'text-green-400', bg: 'bg-green-400/10 border-green-400/30', icon: CheckCircle2 },
  'Wrong Answer': { color: 'text-red-400', bg: 'bg-red-400/10 border-red-400/30', icon: XCircle },
  'Compilation Error': { color: 'text-orange-400', bg: 'bg-orange-400/10 border-orange-400/30', icon: AlertTriangle },
  'Runtime Error': { color: 'text-orange-400', bg: 'bg-orange-400/10 border-orange-400/30', icon: AlertTriangle },
  'Time Limit Exceeded': { color: 'text-yellow-400', bg: 'bg-yellow-400/10 border-yellow-400/30', icon: Clock },
};

export const CodingWorkspace = () => {
  const { problemId } = useParams();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [customInput, setCustomInput] = useState('');
  const [runResult, setRunResult] = useState(null);
  const [runLoading, setRunLoading] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submission, setSubmission] = useState(null);
  const [activeTab, setActiveTab] = useState('console'); // 'console' | 'report'
  const [consolePanelOpen, setConsolePanelOpen] = useState(true);
  const [copied, setCopied] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const fetchProblem = async () => {
      try {
        setLoading(true);
        const data = await problemsApi.get(problemId);
        setProblem(data);
        const template = data.starterTemplates?.[language] || '';
        setCode(template);
        // Pre-fill custom input with first sample case
        if (data.sampleCases?.[0]) {
          setCustomInput(data.sampleCases[0].input);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProblem();
  }, [problemId]);

  // Update starter code when language changes
  useEffect(() => {
    if (problem) {
      const template = problem.starterTemplates?.[language] || '';
      setCode(template);
    }
  }, [language, problem]);

  const handleRun = async () => {
    if (!code.trim()) return;
    try {
      setRunLoading(true);
      setRunResult(null);
      setActiveTab('console');
      const result = await submissionsApi.run({
        code,
        language,
        problemId,
        stdin: customInput,
      });
      setRunResult(result);
    } catch (err) {
      setRunResult({ error: err.message });
    } finally {
      setRunLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!code.trim()) return;
    try {
      setSubmitLoading(true);
      setSubmission(null);
      setActiveTab('report');
      const result = await submissionsApi.submit({
        code,
        language,
        problemId,
      });
      setSubmission(result);
    } catch (err) {
      setSubmission({ error: err.message });
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleReset = () => {
    if (problem) {
      setCode(problem.starterTemplates?.[language] || '');
      setRunResult(null);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleDownload = () => {
    const ext = { python: 'py', cpp: 'cpp', java: 'java', javascript: 'js' }[language];
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `solution.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => setCode(ev.target.result);
    reader.readAsText(file);
    e.target.value = '';
  };

  const monacoLanguage = { python: 'python', cpp: 'cpp', java: 'java', javascript: 'javascript' }[language];

  if (loading) return <LoadingSkeleton variant="editor" />;

  return (
    <div className="flex flex-col h-[calc(100vh-73px)] -m-6 md:-m-8 overflow-hidden">
      {/* Top toolbar */}
      <div className="glass-panel border-b border-dark-border flex items-center justify-between px-4 py-2.5 shrink-0">
        <div className="flex items-center gap-3">
          <Link
            to={`/problems/${problemId}`}
            className="flex items-center gap-1.5 text-sm text-dark-text-secondary hover:text-primary transition-colors"
          >
            <ChevronLeft className="h-4 w-4" />
            <span className="hidden sm:inline">{problem?.title || 'Problem'}</span>
          </Link>
          <div className="w-px h-5 bg-dark-border" />
          {/* Language Selector */}
          <div className="relative">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="glass-input px-3 py-1.5 rounded-lg text-sm pr-8 cursor-pointer appearance-none"
            >
              {LANGUAGE_OPTIONS.map((l) => (
                <option key={l.id} value={l.id}>{l.label}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-dark-text-muted pointer-events-none" />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button onClick={handleReset} title="Reset to starter code" className="p-1.5 text-dark-text-muted hover:text-dark-text-primary hover:bg-dark-surface rounded cursor-pointer transition-colors">
            <RotateCcw className="h-4 w-4" />
          </button>
          <button onClick={() => fileInputRef.current?.click()} title="Upload file" className="p-1.5 text-dark-text-muted hover:text-dark-text-primary hover:bg-dark-surface rounded cursor-pointer transition-colors">
            <Upload className="h-4 w-4" />
          </button>
          <input ref={fileInputRef} type="file" accept=".py,.js,.java,.cpp,.c,.txt" onChange={handleUpload} className="hidden" />
          <button onClick={handleDownload} title="Download code" className="p-1.5 text-dark-text-muted hover:text-dark-text-primary hover:bg-dark-surface rounded cursor-pointer transition-colors">
            <Download className="h-4 w-4" />
          </button>
          <button onClick={handleCopy} title="Copy code" className="p-1.5 text-dark-text-muted hover:text-dark-text-primary hover:bg-dark-surface rounded cursor-pointer transition-colors">
            {copied ? <CheckCircle2 className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
          </button>

          <div className="w-px h-5 bg-dark-border mx-1" />

          {/* Run Button */}
          <button
            onClick={handleRun}
            disabled={runLoading || submitLoading}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg bg-dark-card border border-dark-border hover:border-primary/50 text-dark-text-primary transition-all disabled:opacity-50 cursor-pointer"
          >
            {runLoading ? (
              <span className="animate-spin h-4 w-4 border-2 border-dark-text-muted border-t-primary rounded-full" />
            ) : (
              <Play className="h-4 w-4 text-green-400" />
            )}
            Run
          </button>

          {/* Submit Button */}
          <button
            onClick={handleSubmit}
            disabled={runLoading || submitLoading}
            className="flex items-center gap-1.5 px-4 py-1.5 text-sm font-semibold rounded-lg bg-primary hover:bg-primary-hover text-white transition-all shadow-lg shadow-primary/20 disabled:opacity-50 cursor-pointer"
          >
            {submitLoading ? (
              <span className="animate-spin h-4 w-4 border-2 border-white/30 border-t-white rounded-full" />
            ) : (
              <Send className="h-4 w-4" />
            )}
            Submit
          </button>
        </div>
      </div>

      {/* Main Editor Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Monaco Editor */}
        <div className="flex-1 overflow-hidden">
          <Editor
            height="100%"
            language={monacoLanguage}
            value={code}
            onChange={(val) => setCode(val || '')}
            theme="vs-dark"
            options={{
              fontSize: 14,
              fontFamily: 'JetBrains Mono, Fira Code, monospace',
              fontLigatures: true,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              tabSize: 4,
              wordWrap: 'on',
              padding: { top: 16, bottom: 16 },
              lineNumbers: 'on',
              renderLineHighlight: 'all',
              cursorSmoothCaretAnimation: 'on',
              smoothScrolling: true,
            }}
          />
        </div>

        {/* Right Panel: Console / Report */}
        <div className="w-[420px] border-l border-dark-border flex flex-col shrink-0 overflow-hidden">
          {/* Panel tabs */}
          <div className="flex border-b border-dark-border shrink-0">
            <button
              onClick={() => setActiveTab('console')}
              className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer ${
                activeTab === 'console'
                  ? 'text-primary border-b-2 border-primary'
                  : 'text-dark-text-secondary hover:text-dark-text-primary'
              }`}
            >
              <Terminal className="h-4 w-4" />
              Console
            </button>
            <button
              onClick={() => setActiveTab('report')}
              className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer ${
                activeTab === 'report'
                  ? 'text-primary border-b-2 border-primary'
                  : 'text-dark-text-secondary hover:text-dark-text-primary'
              }`}
            >
              <Cpu className="h-4 w-4" />
              AI Report
              {submission && !submission.error && (
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              )}
            </button>
          </div>

          {/* Panel content */}
          <div className="flex-1 overflow-y-auto">
            {activeTab === 'console' ? (
              <ConsolePanel
                runResult={runResult}
                runLoading={runLoading}
                customInput={customInput}
                setCustomInput={setCustomInput}
                sampleCases={problem?.sampleCases || []}
              />
            ) : (
              <ReportPanel submission={submission} loading={submitLoading} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// ─── Console Panel ─────────────────────────────────────────────────────────────

const ConsolePanel = ({ runResult, runLoading, customInput, setCustomInput, sampleCases }) => {
  return (
    <div className="p-4 space-y-4">
      {/* Custom Input */}
      <div>
        <label className="block text-xs font-semibold text-dark-text-muted uppercase tracking-wider mb-2">
          Standard Input (stdin)
        </label>
        <textarea
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
          placeholder="Enter custom input here..."
          rows={4}
          className="glass-input w-full px-3 py-2 rounded-lg text-sm font-mono resize-none"
        />
        {/* Quick-fill from sample cases */}
        {sampleCases.length > 0 && (
          <div className="flex gap-2 mt-2 flex-wrap">
            {sampleCases.map((tc, i) => (
              <button
                key={i}
                onClick={() => setCustomInput(tc.input)}
                className="text-xs px-2 py-1 rounded border border-dark-border text-dark-text-muted hover:border-primary/50 hover:text-primary transition-colors cursor-pointer"
              >
                Use Example {i + 1}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Output */}
      <div>
        <label className="block text-xs font-semibold text-dark-text-muted uppercase tracking-wider mb-2">
          Output
        </label>
        {runLoading ? (
          <div className="bg-dark-surface rounded-lg border border-dark-border p-4 h-28 flex items-center justify-center">
            <div className="flex items-center gap-3 text-dark-text-muted text-sm">
              <span className="animate-spin h-4 w-4 border-2 border-dark-border border-t-primary rounded-full" />
              Executing...
            </div>
          </div>
        ) : runResult ? (
          <div className="bg-dark-surface rounded-lg border border-dark-border p-4 space-y-3">
            {runResult.error ? (
              <p className="text-red-400 text-sm">{runResult.error}</p>
            ) : (
              <>
                {/* Status */}
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-dark-text-muted">Status:</span>
                  <span className={`font-semibold ${runResult.status === 'Accepted' ? 'text-green-400' : 'text-orange-400'}`}>
                    {runResult.status}
                  </span>
                </div>
                {/* Runtime & Memory */}
                {runResult.runtime && (
                  <div className="flex gap-4 text-xs text-dark-text-muted">
                    <span>Runtime: <span className="text-dark-text-primary">{runResult.runtime}s</span></span>
                    {runResult.memory && <span>Memory: <span className="text-dark-text-primary">{(runResult.memory / 1024).toFixed(1)}MB</span></span>}
                  </div>
                )}
                {/* stdout */}
                {runResult.stdout && (
                  <div>
                    <p className="text-xs text-dark-text-muted mb-1">stdout:</p>
                    <pre className="text-green-400 text-xs whitespace-pre-wrap font-mono bg-dark-bg/50 p-2 rounded">{runResult.stdout}</pre>
                  </div>
                )}
                {/* stderr */}
                {runResult.stderr && (
                  <div>
                    <p className="text-xs text-dark-text-muted mb-1">stderr:</p>
                    <pre className="text-red-400 text-xs whitespace-pre-wrap font-mono bg-dark-bg/50 p-2 rounded">{runResult.stderr}</pre>
                  </div>
                )}
                {/* compile output */}
                {runResult.compile_output && (
                  <div>
                    <p className="text-xs text-dark-text-muted mb-1">Compiler output:</p>
                    <pre className="text-orange-400 text-xs whitespace-pre-wrap font-mono bg-dark-bg/50 p-2 rounded">{runResult.compile_output}</pre>
                  </div>
                )}
              </>
            )}
          </div>
        ) : (
          <div className="bg-dark-surface rounded-lg border border-dark-border p-4 h-28 flex items-center justify-center text-dark-text-muted text-sm">
            Press Run to execute your code
          </div>
        )}
      </div>
    </div>
  );
};

// ─── Report Panel ──────────────────────────────────────────────────────────────

const ReportPanel = ({ submission, loading }) => {
  if (loading) {
    return (
      <div className="p-4 space-y-3">
        <div className="flex items-center gap-3 text-dark-text-muted text-sm mb-4">
          <span className="animate-spin h-4 w-4 border-2 border-dark-border border-t-primary rounded-full" />
          Grading and generating AI analysis...
        </div>
        <LoadingSkeleton variant="card" count={3} />
      </div>
    );
  }

  if (!submission) {
    return (
      <div className="p-4 h-full flex flex-col items-center justify-center text-center">
        <Send className="h-10 w-10 text-dark-text-muted/30 mb-3" />
        <p className="text-dark-text-muted text-sm">Submit your code to see the AI analysis report</p>
      </div>
    );
  }

  if (submission.error) {
    return (
      <div className="p-4">
        <div className="flex items-center gap-2 bg-red-950/30 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
          <XCircle className="h-4 w-4 shrink-0" />
          <span>{submission.error}</span>
        </div>
      </div>
    );
  }

  return <SubmissionReport submission={submission} />;
};

export default CodingWorkspace;
