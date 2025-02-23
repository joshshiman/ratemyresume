interface JobDescriptionProps {
  jobData: any
  onFetch: () => void
}

export default function JobDescription({ jobData, onFetch }: JobDescriptionProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="border-b p-4 flex justify-between items-center">
        <h2 className="text-lg font-semibold">Job Description</h2>
        <button
          onClick={onFetch}
          className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
        >
          Fetch Job
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        {jobData ? (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">{jobData.title}</h3>
            <div className="space-y-2">
              <p>
                <strong>Company:</strong> {jobData.company}
              </p>
              <p>
                <strong>Location:</strong> {jobData.location}
              </p>
              <p>
                <strong>Pay:</strong> {jobData.pay}
              </p>
            </div>
            <div className="whitespace-pre-wrap">{jobData.description}</div>
          </div>
        ) : (
          <p className="text-muted-foreground">Click "Fetch Job" to load a job description</p>
        )}
      </div>
    </div>
  )
}

