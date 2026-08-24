import React, { useState } from 'react';
import { addOrUpdateJob, type Job, type JobStatus } from './db';
import { v4 as uuidv4 } from 'uuid';
import { X } from 'lucide-react';

interface JobModalProps {
  job: Job | null;
  onClose: () => void;
  onSave: (job: Job) => void;
}

const statusOptions: JobStatus[] = [
  'Wishlist', 'Applied', 'Follow-up', 'Interview', 'Offer', 'Rejected'
];

export const JobModal: React.FC<JobModalProps> = ({ job, onClose, onSave }) => {
  const [formData, setFormData] = useState<Partial<Job>>(
    job || {
      status: 'Wishlist',
      companyName: '',
      title: '',
      dateApplied: Date.now()
    }
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.companyName || !formData.title) return;

    const jobToSave: Job = {
      id: formData.id || uuidv4(),
      companyName: formData.companyName,
      title: formData.title,
      url: formData.url,
      resumeTag: formData.resumeTag,
      dateApplied: formData.dateApplied || Date.now(),
      salaryRange: formData.salaryRange,
      notes: formData.notes,
      status: formData.status as JobStatus,
    };

    await addOrUpdateJob(jobToSave);
    onSave(jobToSave);
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex justify-end">
      <div className="bg-white dark:bg-slate-900 w-full max-w-md h-full shadow-2xl p-6 overflow-y-auto slide-in-right">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">{job ? 'Edit Job' : 'Add New Job'}</h2>
          <button onClick={onClose} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Company Name *</label>
            <input 
              required
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.companyName || ''}
              onChange={e => setFormData({ ...formData, companyName: e.target.value })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Role / Title *</label>
            <input 
              required
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.title || ''}
              onChange={e => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.status}
              onChange={e => setFormData({ ...formData, status: e.target.value as JobStatus })}
            >
              {statusOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">LinkedIn / Job URL</label>
            <input 
              type="url"
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent text-blue-500"
              value={formData.url || ''}
              onChange={e => setFormData({ ...formData, url: e.target.value })}
              placeholder="https://..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Resume Used</label>
            <input 
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.resumeTag || ''}
              onChange={e => setFormData({ ...formData, resumeTag: e.target.value })}
              placeholder="e.g. QA_Lead_v2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Salary Range</label>
            <input 
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.salaryRange || ''}
              onChange={e => setFormData({ ...formData, salaryRange: e.target.value })}
              placeholder="$120k - $150k"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Notes</label>
            <textarea 
              rows={4}
              className="w-full border dark:border-slate-700 rounded-md p-2 bg-transparent"
              value={formData.notes || ''}
              onChange={e => setFormData({ ...formData, notes: e.target.value })}
            />
          </div>

          <div className="pt-4 flex justify-end space-x-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium rounded-md hover:bg-slate-100 dark:hover:bg-slate-800">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700">
              Save Job
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};