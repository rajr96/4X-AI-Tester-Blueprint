import React from 'react';
import type { Job } from './db';
import { formatDistanceToNow } from 'date-fns';
import { ExternalLink, Edit2, Trash2, FileText } from 'lucide-react';
import { Draggable } from '@hello-pangea/dnd';

interface JobCardProps {
  job: Job;
  index: number;
  onEdit: (job: Job) => void;
  onDelete: (jobId: string) => void;
}

const statusColors: Record<string, string> = {
  'Wishlist': 'border-l-slate-400',
  'Applied': 'border-l-blue-400',
  'Follow-up': 'border-l-yellow-400',
  'Interview': 'border-l-purple-500',
  'Offer': 'border-l-green-500',
  'Rejected': 'border-l-red-500'
};

export const JobCard: React.FC<JobCardProps> = ({ job, index, onEdit, onDelete }) => {
  return (
    <Draggable draggableId={job.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`bg-white dark:bg-slate-800 p-4 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 border-l-4 ${statusColors[job.status]} mb-3 group hover:shadow-md transition-shadow`}
        >
          <div className="flex justify-between items-start mb-2">
            <div>
              <h3 className="font-semibold text-sm truncate max-w-[180px]" title={job.companyName}>{job.companyName}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 truncate max-w-[180px]">{job.title}</p>
            </div>
            <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button onClick={() => onEdit(job)} className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded"><Edit2 size={14}/></button>
              <button onClick={() => { if(confirm('Delete job?')) onDelete(job.id); }} className="p-1 hover:bg-red-50 dark:hover:bg-red-900/30 text-red-500 rounded"><Trash2 size={14}/></button>
            </div>
          </div>
          
          <div className="flex justify-between items-end mt-4">
             <div className="flex flex-col gap-1">
               {job.resumeTag && (
                  <span className="text-[10px] bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-full inline-flex items-center gap-1 text-slate-600 dark:text-slate-300 w-fit">
                    <FileText size={10} /> {job.resumeTag}
                  </span>
               )}
               <span className="text-[10px] text-slate-400">
                  {formatDistanceToNow(job.dateApplied)} ago
               </span>
             </div>
             
             {job.url && (
               <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-600 p-1">
                 <ExternalLink size={14} />
               </a>
             )}
          </div>
        </div>
      )}
    </Draggable>
  );
};