"use client"

import { useState } from "react"
import JobDescription from "@/components/job-description"
import Resume from "@/components/resume"
import ChatInterface from "@/components/chat-interface"

export default function ResumeTailoring() {
  const [jobData, setJobData] = useState<any>(null);
  const [selectedText, setSelectedText] = useState("");
  const [page, setPage] = useState(1); // Track the current page number

  const fetchJob = async () => {
    try {
      // Fetch jobs for the current page
      const response = await fetch(`http://localhost:8000/jobs?page=${page}&limit=1`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setJobData(data.jobs[0]); // Set the fetched job data

      // Increment the page number for the next fetch
      setPage((prevPage) => prevPage + 1);
    } catch (error) {
      console.error("Error fetching job:", error);
    }
  };

  return (
    <div className="h-screen bg-background overflow-hidden">
      <div className="grid h-full grid-cols-1 gap-4 p-4 md:grid-cols-3">
        <div className="rounded-lg border bg-card shadow-sm overflow-hidden">
          <ChatInterface selectedText={selectedText} jobDescription={jobData?.description || ""} />
        </div>
        <div className="rounded-lg border bg-card shadow-sm overflow-hidden">
          <Resume onTextSelect={setSelectedText} />
        </div>
        <div className="rounded-lg border bg-card shadow-sm overflow-hidden">
          <JobDescription jobData={jobData} onFetch={fetchJob} />
        </div>
      </div>
    </div>
  )
}

