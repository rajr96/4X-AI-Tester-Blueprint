import React, { useState, useEffect, useMemo } from 'react';
import { DragDropContext, Droppable, type DropResult } from '@hello-pangea/dnd';
import { Plus, Search, Moon, Sun, Download, Upload, Briefcase, TrendingUp, Clock3, CheckCircle2 } from 'lucide-react';
import { getAllJobs, addOrUpdateJob, deleteJob, clearAllJobs, seedDefaultJobsIfEmpty, type Job, type JobStatus } from './db';
import { JobCard } from './JobCard';
import { JobModal } from './JobModal';

const COLUMNS: JobStatus[] = [
  'Wishlist', 'Applied', 'Follow-up', 'Interview', 'Offer', 'Rejected'
];

const STATUS_META: Record<JobStatus, { accent: string; pill: string; short: string }> = {
  Wishlist: { accent: 'bg-sky-500/20 text-sky-200 border-sky-400/30', pill: 'bg-sky-500/10 text-sky-200', short: 'Wishlist' },
  Applied: { accent: 'bg-violet-500/20 text-violet-200 border-violet-400/30', pill: 'bg-violet-500/10 text-violet-200', short: 'Applied' },
  'Follow-up': { accent: 'bg-amber-500/20 text-amber-200 border-amber-400/30', pill: 'bg-amber-500/10 text-amber-200', short: 'Follow-up' },
  Interview: { accent: 'bg-emerald-500/20 text-emerald-200 border-emerald-400/30', pill: 'bg-emerald-500/10 text-emerald-200', short: 'Interview' },
  Offer: { accent: 'bg-cyan-500/20 text-cyan-200 border-cyan-400/30', pill: 'bg-cyan-500/10 text-cyan-200', short: 'Offer' },
  Rejected: { accent: 'bg-rose-500/20 text-rose-200 border-rose-400/30', pill: 'bg-rose-500/10 text-rose-200', short: 'Rejected' },
};

const formatRelativeDate = (date: number) => {
  const diff = Math.max(0, Date.now() - date);
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days === 0) return 'Today';
  if (days === 1) return '1 day ago';
  return `${days} days ago`;
};

export default function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingJob, setEditingJob] = useState<Job | null>(null);
  const [darkMode, setDarkMode] = useState(
    () => window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  useEffect(() => {
    const init = async () => {
      await seedDefaultJobsIfEmpty();
      await loadJobs();
    };
    init();
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const loadJobs = async () => {
    const data = await getAllJobs();
    setJobs(data.sort((a,b) => b.dateApplied - a.dateApplied));
  };

  const handleDragEnd = async (result: DropResult) => {
    if (!result.destination) return;

    const { source, destination, draggableId } = result;
    if (source.droppableId === destination.droppableId) return;

    const jobToMove = jobs.find(j => j.id === draggableId);
    if (!jobToMove) return;

    const updatedJob = { ...jobToMove, status: destination.droppableId as JobStatus };
    setJobs(prev => prev.map(j => j.id === draggableId ? updatedJob : j));
    await addOrUpdateJob(updatedJob);
  };

  const handleDelete = async (id: string) => {
    await deleteJob(id);
    setJobs(prev => prev.filter(j => j.id !== id));
  };

  const handleExport = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(jobs));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = `job-tracker-backup-[${new Date().toISOString().split('T')[0]}].json`;
    a.click();
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    try {
      const imported: Job[] = JSON.parse(text);
      if (confirm(`Import ${imported.length} jobs? This will replace current data.`)) {
        await clearAllJobs();
        for (const j of imported) await addOrUpdateJob(j);
        await loadJobs();
      }
    } catch {
      alert('Invalid JSON file');
    }
  };

  const filteredJobs = jobs.filter(j => 
    j.companyName.toLowerCase().includes(search.toLowerCase()) ||
    j.title.toLowerCase().includes(search.toLowerCase())
  );

  const metrics = useMemo(() => {
    const grouped = {
      total: jobs.length,
      wishlist: jobs.filter(j => j.status === 'Wishlist').length,
      applied: jobs.filter(j => j.status === 'Applied').length,
      followUp: jobs.filter(j => j.status === 'Follow-up').length,
      interview: jobs.filter(j => j.status === 'Interview').length,
      offer: jobs.filter(j => j.status === 'Offer').length,
      rejected: jobs.filter(j => j.status === 'Rejected').length,
    };

    const maxFunnel = Math.max(...Object.values({ applied: grouped.applied, followUp: grouped.followUp, interview: grouped.interview, offer: grouped.offer, rejected: grouped.rejected }), 1);
    const funnel = [
      { label: 'Applied', value: grouped.applied },
      { label: 'Follow-up', value: grouped.followUp },
      { label: 'Interview', value: grouped.interview },
      { label: 'Offer', value: grouped.offer },
      { label: 'Rejected', value: grouped.rejected },
    ].map(item => ({ ...item, width: (item.value / maxFunnel) * 100 }));

    return { ...grouped, funnel };
  }, [jobs]);

  const recentApplied = [...jobs.filter(j => j.status === 'Applied')].sort((a,b) => b.dateApplied - a.dateApplied).slice(0, 5);
  const followUps = [...jobs.filter(j => j.status === 'Follow-up')].sort((a,b) => a.dateApplied - b.dateApplied).slice(0, 5);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto max-w-[1700px] px-4 py-6 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-4 pb-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">CareerPulse</p>
              <h1 className="mt-2 text-4xl font-bold tracking-tight text-white">JobTracker</h1>
            </div>

            <div className="flex items-center gap-3">
              <button onClick={() => setDarkMode(!darkMode)} className="rounded-xl border border-slate-700 bg-slate-900 p-2.5 text-slate-200 transition hover:border-slate-500" title="Toggle theme">
                {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              </button>

              <button onClick={handleExport} className="rounded-xl border border-slate-700 bg-slate-900 p-2.5 text-slate-200 transition hover:border-slate-500" title="Export JSON">
                <Download size={18} />
              </button>

              <label className="cursor-pointer rounded-xl border border-slate-700 bg-slate-900 p-2.5 text-slate-200 transition hover:border-slate-500" title="Import JSON">
                <Upload size={18} />
                <input type="file" accept=".json" className="hidden" onChange={handleImport} />
              </label>

              <button
                onClick={() => { setEditingJob(null); setIsModalOpen(true); }}
                className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 font-medium text-white shadow-lg shadow-blue-700/20 transition hover:bg-blue-500"
              >
                <Plus size={18} />
                Add Job
              </button>
            </div>
          </div>

          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-lg text-slate-300">Track and manage your application pipeline locally.</p>
            </div>

            <div className="relative w-full max-w-md">
              <Search className="absolute left-3 top-3 text-slate-400" size={16} />
              <input
                type="text"
                placeholder="Search jobs..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full rounded-xl border border-slate-700 bg-slate-900/80 py-2.5 pl-10 pr-3 text-sm text-slate-100 outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500"
              />
            </div>
          </div>
        </header>

        <main className="space-y-8">
          <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/30">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Overview</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Dashboard</h2>
              </div>
              <div className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200">
                Local-first data
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
              {[
                { label: 'Available Jobs', value: metrics.total, icon: Briefcase },
                { label: 'Applied', value: metrics.applied, icon: TrendingUp },
                { label: 'Interviews', value: metrics.interview, icon: CheckCircle2 },
                { label: 'Offers', value: metrics.offer, icon: Briefcase },
                { label: 'Rejected', value: metrics.rejected, icon: Clock3 },
              ].map(({ label, value, icon: Icon }) => (
                <div key={label} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-400">{label}</span>
                    <span className="rounded-lg bg-slate-800 p-2 text-slate-200"><Icon size={16} /></span>
                  </div>
                  <div className="mt-6 text-3xl font-bold text-white">{value}</div>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
            <div className="mb-5 flex items-center justify-between">
              <h3 className="text-xl font-semibold text-white">Tracker Board</h3>
              <span className="text-sm text-slate-400">{filteredJobs.length} visible</span>
            </div>

            <DragDropContext onDragEnd={handleDragEnd}>
              <div className="grid gap-4 xl:grid-cols-6">
                {COLUMNS.map(col => {
                  const colJobs = filteredJobs.filter(j => j.status === col);

                  return (
                    <div key={col} className="min-h-[220px] rounded-2xl border border-slate-800 bg-slate-950/70 p-3">
                      <div className="mb-3 flex items-center justify-between px-1">
                        <h4 className="text-base font-medium text-white">{col}</h4>
                        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-200">{colJobs.length}</span>
                      </div>

                      <Droppable droppableId={col}>
                        {(provided) => (
                          <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-3">
                            {colJobs.length ? colJobs.map((job, index) => (
                              <JobCard
                                key={job.id}
                                job={job}
                                index={index}
                                onEdit={(j) => { setEditingJob(j); setIsModalOpen(true); }}
                                onDelete={handleDelete}
                              />
                            )) : (
                              <div className="rounded-xl border border-dashed border-slate-700 bg-slate-900/40 p-3 text-center text-sm text-slate-500">
                                No jobs
                              </div>
                            )}
                            {provided.placeholder}
                          </div>
                        )}
                      </Droppable>
                    </div>
                  );
                })}
              </div>
            </DragDropContext>
          </section>

          <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
              <h3 className="text-xl font-semibold text-white">Application Funnel</h3>
              <p className="mt-1 text-sm text-slate-400">Progression through your pipeline, calculated from local data.</p>

              <div className="mt-6 space-y-4">
                {metrics.funnel.map((item) => (
                  <div key={item.label}>
                    <div className="mb-2 flex items-center justify-between text-sm text-slate-300">
                      <span>{item.label}</span>
                      <span>{item.value}</span>
                    </div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className={`h-full rounded-full ${STATUS_META[(item.label === 'Follow-up' ? 'Follow-up' : item.label === 'Applied' ? 'Applied' : item.label === 'Interview' ? 'Interview' : item.label === 'Offer' ? 'Offer' : item.label === 'Rejected' ? 'Rejected' : 'Wishlist') as JobStatus].pill}`}
                        style={{ width: `${item.width}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white">Tracker Overview</h3>
                <span className="text-sm text-slate-400">{metrics.total} jobs</span>
              </div>

              <div className="space-y-3">
                {COLUMNS.map((column) => {
                  const count = jobs.filter(job => job.status === column).length;
                  return (
                    <div key={column} className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2">
                      <div className="flex items-center gap-2">
                        <span className={`inline-block h-2.5 w-2.5 rounded-full ${STATUS_META[column].pill.replace('bg-', 'bg-').replace('/10', '/100').replace('text-', '')}`} />
                        <span className="text-sm text-slate-200">{column}</span>
                      </div>
                      <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-200">{count}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white">Recent Applied Jobs</h3>
                <button className="text-sm text-blue-300">View all</button>
              </div>

              <div className="space-y-3">
                {recentApplied.length ? recentApplied.map(job => (
                  <div key={job.id} className="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                    <div>
                      <div className="font-medium text-white">{job.companyName}</div>
                      <div className="text-sm text-slate-400">{job.title}</div>
                    </div>
                    <div className="text-right text-sm">
                      <div className="text-slate-300">{new Date(job.dateApplied).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</div>
                      <div className="mt-1 inline-flex rounded-full bg-violet-500/15 px-2 py-0.5 text-xs text-violet-200">Applied</div>
                    </div>
                  </div>
                )) : <p className="text-sm text-slate-400">No applied jobs yet.</p>}
              </div>
            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white">Upcoming Follow-ups</h3>
                <button className="text-sm text-blue-300">View all</button>
              </div>

              <div className="space-y-3">
                {followUps.length ? followUps.map(job => (
                  <div key={job.id} className="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                    <div>
                      <div className="font-medium text-white">{job.companyName}</div>
                      <div className="text-sm text-slate-400">{job.title}</div>
                    </div>
                    <div className="text-right text-sm">
                      <div className="text-slate-300">{formatRelativeDate(job.dateApplied)}</div>
                      <button className="mt-1 rounded-full border border-amber-500/30 bg-amber-500/10 px-2 py-0.5 text-xs text-amber-200">Mark Follow-up</button>
                    </div>
                  </div>
                )) : <p className="text-sm text-slate-400">No follow-ups scheduled.</p>}
              </div>
            </div>
          </section>

        </main>
      </div>

      {isModalOpen && (
        <JobModal
          job={editingJob}
          onClose={() => setIsModalOpen(false)}
          onSave={() => { loadJobs(); setIsModalOpen(false); }}
        />
      )}
    </div>
  );
}