import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Terminal, Shield, Award, Sparkles, Brain, Code, ArrowRight } from 'lucide-react';
import Button from '../components/Button';

export const Landing = () => {
  const { currentUser } = useAuth();

  const features = [
    {
      icon: Terminal,
      title: 'Automated Grading',
      description: 'Run your code on standard, secure compilers via Judge0, verifying solutions instantly against secret test suites.',
    },
    {
      icon: Brain,
      title: 'AI Code Diagnostics',
      description: 'Unlock direct architectural feedback with quality scores across readability, error handling, design patterns, and maintainability.',
    },
    {
      icon: Sparkles,
      title: 'Mermaid Flow Diagrams',
      description: 'Understand the logical loop progression and structural paths of your algorithms visually using auto-rendered execution trees.',
    },
    {
      icon: Award,
      title: 'Interview Readiness Score',
      description: 'Receive custom interviewer feedback detailing follow-up questions, complexity justifications, and optimized code refactoring diffs.',
    },
  ];

  return (
    <div className="min-h-screen bg-dark-bg text-dark-text-primary overflow-hidden flex flex-col justify-between">
      {/* Hero section */}
      <section className="relative pt-24 pb-20 px-6 max-w-6xl mx-auto flex flex-col items-center text-center">
        {/* Glow effect backgrounds */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[120px] pointer-events-none -z-10" />
        <div className="absolute top-1/3 left-1/4 w-[300px] h-[300px] bg-purple-500/5 rounded-full blur-[90px] pointer-events-none -z-10" />

        <div className="inline-flex items-center space-x-2 bg-primary/10 border border-primary/20 rounded-full px-4 py-1.5 mb-8 animate-border-pulse">
          <Sparkles className="h-4 w-4 text-primary" />
          <span className="text-xs font-semibold text-primary uppercase tracking-wider">Next-Gen Coding Assessments</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 max-w-3xl leading-tight">
          Master Technical Interviews with{' '}
          <span className="bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">
            AI-Powered Diagnostics
          </span>
        </h1>

        <p className="text-lg md:text-xl text-dark-text-secondary max-w-2xl mb-10 leading-relaxed">
          Step beyond simple compiler output. Validate correctness against hidden test cases, get scored code quality reviews, Big-O analysis, and Mermaid.js diagrams instantly.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full">
          {currentUser ? (
            <Link to="/dashboard" className="w-full sm:w-auto">
              <Button variant="primary" className="w-full sm:w-auto py-3 px-8 text-base">
                Go to Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          ) : (
            <>
              <Link to="/register" className="w-full sm:w-auto">
                <Button variant="primary" className="w-full sm:w-auto py-3 px-8 text-base">
                  Get Started for Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link to="/login" className="w-full sm:w-auto">
                <Button variant="outline" className="w-full sm:w-auto py-3 px-8 text-base">
                  Sign In
                </Button>
              </Link>
            </>
          )}
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 border-t border-dark-border bg-dark-surface/10 relative">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Everything you need to level up</h2>
            <p className="text-dark-text-secondary max-w-lg mx-auto">
              Our assessment platform pairs Judge0 execution with cutting-edge Gemini LLM grading models.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <div
                  key={idx}
                  className="bg-dark-card border border-dark-border hover:border-primary/30 p-8 rounded-2xl transition-all duration-300 hover:shadow-xl hover:shadow-primary/5 group"
                >
                  <div className="bg-primary/10 w-12 h-12 rounded-xl flex items-center justify-center border border-primary/20 mb-6 group-hover:scale-110 transition-transform duration-300">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-lg font-bold mb-2 group-hover:text-primary transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-dark-text-secondary text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Quick stats section */}
      <section className="py-16 border-t border-dark-border bg-dark-bg/60 text-center">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 px-6">
          <div>
            <p className="text-4xl md:text-5xl font-extrabold text-primary mb-2">15+</p>
            <p className="text-xs md:text-sm text-dark-text-secondary uppercase tracking-wider font-semibold">
              Original DSA Problems
            </p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold text-primary mb-2">0ms</p>
            <p className="text-xs md:text-sm text-dark-text-secondary uppercase tracking-wider font-semibold">
              Hidden Output Exposure
            </p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold text-primary mb-2">100%</p>
            <p className="text-xs md:text-sm text-dark-text-secondary uppercase tracking-wider font-semibold">
              AI Code Walkthroughs
            </p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold text-primary mb-2">JSON</p>
            <p className="text-xs md:text-sm text-dark-text-secondary uppercase tracking-wider font-semibold">
              Structured Diagnostics
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-dark-border text-center text-sm text-dark-text-muted bg-dark-surface/20">
        <p>© {new Date().getFullYear()} CodeAssess. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Landing;
