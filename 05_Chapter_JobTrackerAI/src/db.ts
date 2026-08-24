import { openDB, type DBSchema, type IDBPDatabase } from 'idb';

export type JobStatus = 
  | 'Wishlist'
  | 'Applied'
  | 'Follow-up'
  | 'Interview'
  | 'Offer'
  | 'Rejected';

export interface Job {
  id: string;
  companyName: string;
  title: string;
  url?: string;
  resumeTag?: string;
  dateApplied: number;
  salaryRange?: string;
  notes?: string;
  status: JobStatus;
}

interface JobTrackerDB extends DBSchema {
  jobs: {
    key: string;
    value: Job;
    indexes: { 'by-date': number };
  };
}

let dbPromise: Promise<IDBPDatabase<JobTrackerDB>>;

export function initDB() {
  if (!dbPromise) {
    dbPromise = openDB<JobTrackerDB>('job-tracker-db', 1, {
      upgrade(db) {
        const store = db.createObjectStore('jobs', { keyPath: 'id' });
        store.createIndex('by-date', 'dateApplied');
      },
    });
  }
  return dbPromise;
}

export async function getAllJobs(): Promise<Job[]> {
  const db = await initDB();
  return db.getAllFromIndex('jobs', 'by-date');
}

export async function addOrUpdateJob(job: Job): Promise<void> {
  const db = await initDB();
  await db.put('jobs', job);
}

export async function deleteJob(id: string): Promise<void> {
  const db = await initDB();
  await db.delete('jobs', id);
}

export const DEFAULT_JOBS: Job[] = [
  {
    id: 'seed-microsoft-designer',
    companyName: 'Microsoft',
    title: 'Senior Product Designer',
    url: 'https://www.microsoft.com/careers',
    resumeTag: 'Design',
    dateApplied: Date.parse('2026-08-18'),
    salaryRange: '$160k - $210k',
    notes: 'Strong fit for product design and user research roles.',
    status: 'Wishlist',
  },
  {
    id: 'seed-google-software-eng',
    companyName: 'Google',
    title: 'Software Engineer II',
    url: 'https://careers.google.com',
    resumeTag: 'Backend',
    dateApplied: Date.parse('2026-08-20'),
    salaryRange: '$180k - $220k',
    notes: 'Applied through the referral program and waiting on recruiter screening.',
    status: 'Applied',
  },
  {
    id: 'seed-atlassian-csm',
    companyName: 'Atlassian',
    title: 'Customer Success Manager',
    url: 'https://www.atlassian.com/company/careers',
    resumeTag: 'Customer Success',
    dateApplied: Date.parse('2026-08-21'),
    salaryRange: '$110k - $150k',
    notes: 'Follow up with recruiter next week after listening session.',
    status: 'Follow-up',
  },
  {
    id: 'seed-shopify-frontend',
    companyName: 'Shopify',
    title: 'Frontend Engineer',
    url: 'https://www.shopify.com/careers',
    resumeTag: 'Frontend',
    dateApplied: Date.parse('2026-08-22'),
    salaryRange: '$170k - $200k',
    notes: 'Interview loop scheduled for next Thursday with design and systems panels.',
    status: 'Interview',
  },
  {
    id: 'seed-stripe-data-analyst',
    companyName: 'Stripe',
    title: 'Data Analyst',
    url: 'https://stripe.com/jobs',
    resumeTag: 'Analytics',
    dateApplied: Date.parse('2026-08-23'),
    salaryRange: '$150k - $185k',
    notes: 'Offer discussion underway; final compensation review pending.',
    status: 'Offer',
  },
  {
    id: 'seed-ibm-qa-engineer',
    companyName: 'IBM',
    title: 'QA Automation Engineer',
    url: 'https://www.ibm.com/employment',
    resumeTag: 'QA',
    dateApplied: Date.parse('2026-08-12'),
    salaryRange: '$120k - $150k',
    notes: 'Role was paused after internal restructuring. Great learning experience.',
    status: 'Rejected',
  },
  {
    id: 'seed-salesforce-account-exec',
    companyName: 'Salesforce',
    title: 'Account Executive',
    url: 'https://www.salesforce.com/company/careers',
    resumeTag: 'Sales',
    dateApplied: Date.parse('2026-08-10'),
    salaryRange: '$130k - $170k',
    notes: 'Rejected after final round due to target profile mismatch.',
    status: 'Rejected',
  },
  {
    id: 'seed-github-platform-engineer',
    companyName: 'GitHub',
    title: 'Platform Engineer',
    url: 'https://github.com/about/careers',
    resumeTag: 'Infrastructure',
    dateApplied: Date.parse('2026-08-14'),
    salaryRange: '$150k - $190k',
    notes: 'Strong systems background; recruiter follow-up pending.',
    status: 'Applied',
  },
  {
    id: 'seed-notion-product-manager',
    companyName: 'Notion',
    title: 'Product Manager',
    url: 'https://www.notion.so/careers',
    resumeTag: 'Product',
    dateApplied: Date.parse('2026-08-16'),
    salaryRange: '$170k - $210k',
    notes: 'Submitted portfolio and case study; waiting for interview scheduling.',
    status: 'Follow-up',
  },
  {
    id: 'seed-airbnb-frontend',
    companyName: 'Airbnb',
    title: 'Frontend Engineer',
    url: 'https://careers.airbnb.com/',
    resumeTag: 'Frontend',
    dateApplied: Date.parse('2026-08-08'),
    salaryRange: '$160k - $200k',
    notes: 'Interview loop started; final review with hiring manager next week.',
    status: 'Interview',
  },
  {
    id: 'seed-linkedin-ml-engineer',
    companyName: 'LinkedIn',
    title: 'ML Engineer',
    url: 'https://www.linkedin.com/company/linkedin/jobs',
    resumeTag: 'AI',
    dateApplied: Date.parse('2026-08-05'),
    salaryRange: '$180k - $220k',
    notes: 'Role was closed internally after business reprioritization.',
    status: 'Rejected',
  },
];

export async function seedDefaultJobsIfEmpty(): Promise<void> {
  const db = await initDB();
  const existing = await db.getAll('jobs');
  const existingIds = new Set(existing.map((job) => job.id));
  const missingJobs = DEFAULT_JOBS.filter((job) => !existingIds.has(job.id));

  if (missingJobs.length === 0) return;

  for (const job of missingJobs) {
    await db.put('jobs', job);
  }
}

export async function clearAllJobs(): Promise<void> {
  const db = await initDB();
  await db.clear('jobs');
}
