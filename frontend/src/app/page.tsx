"use client"

import { useState } from "react"
import JobDescription from "./components/job-description"
import Resume from "./components/resume"
import ChatInterface from "./components/chat-interface"

export default function ResumeTailoring() {
  const [jobData, setJobData] = useState<any>(null)
  const [selectedText, setSelectedText] = useState("")

  const fetchJob = async () => {
    try {
      const response = await fetch("http://34.130.198.88:8001/jobs?limit=1")
      const data = await response.json()
      setJobData(data.jobs[0])
    } catch (error) {
      console.error("Error fetching job:", error)
    }
  }

  return (
    <div className="h-screen bg-background">
      <div className="grid h-full grid-cols-1 gap-4 p-4 md:grid-cols-3">
        <div className="rounded-lg border bg-card shadow-sm">
          <JobDescription jobData={jobData} onFetch={fetchJob} />
        </div>
        <div className="rounded-lg border bg-card shadow-sm">
          <Resume onTextSelect={setSelectedText} />
        </div>
        <div className="rounded-lg border bg-card shadow-sm">
          <ChatInterface selectedText={selectedText} jobDescription={jobData?.description || ""} />
        </div>
      </div>
    </div>
  )
}

