interface ResumeProps {
  onTextSelect: (text: string) => void
}

export default function Resume({ onTextSelect }: ResumeProps) {
  const handleTextSelection = () => {
    const selection = window.getSelection()
    if (selection && selection.toString()) {
      onTextSelect(selection.toString())
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b p-4">
        <h2 className="text-lg font-semibold">Resume</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4" onMouseUp={handleTextSelection}>
        <div className="space-y-6">
          <h1 className="text-2xl font-bold">John Smith</h1>

          <p className="text-muted-foreground">
            Passionate Software Engineer with 10+ years of experience in developing web applications and backend
            systems. Skilled at writing clear, concise code that is easy to maintain and troubleshoot.
          </p>

          <section>
            <h2 className="text-xl font-semibold">Experience</h2>
            <div className="mt-4 space-y-4">
              <div>
                <h3 className="font-medium">Senior Software Engineer - TechCorp</h3>
                <p className="text-sm text-muted-foreground">2020 - Present</p>
                <ul className="mt-2 list-disc pl-5 text-sm">
                  <li>Led development of microservices architecture serving 1M+ users</li>
                  <li>Implemented CI/CD pipeline reducing deployment time by 60%</li>
                  <li>Mentored junior developers and conducted code reviews</li>
                  <li>
                    Scripted unique test plans, test scripts and processes to remove previously know redundancy by 40%
                    and ensured predictable outcomes
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-medium">Software Engineer - Innovate Solutions</h3>
                <p className="text-sm text-muted-foreground">2018 - 2020</p>
                <ul className="mt-2 list-disc pl-5 text-sm">
                  <li>Developed full-stack features for SaaS product using React and Node.js</li>
                  <li>Designed REST APIs handling 500+ requests/minute with 99.9% uptime</li>
                  <li>Optimized PostgreSQL queries reducing page load times by 30%</li>
                  <li>Collaborated with product teams to implement user-facing features</li>
                  <li>Improved application performance through caching strategies</li>
                </ul>
              </div>
              {/* New Technical PM Experience */}
              <div>
                <h3 className="font-medium">Technical Project Manager - TechFlow Systems</h3>
                <p className="text-sm text-muted-foreground">2016 - 2018</p>
                <ul className="mt-2 list-disc pl-5 text-sm">
                  <li>Led cross-functional teams in delivering 15+ tech projects on time and under budget</li>
                  <li>Managed Agile Scrum processes using Jira and Confluence for team of 12 developers</li>
                  <li>Coordinated between engineering, design, and stakeholders to define product roadmaps</li>
                  <li>Conducted risk analysis that reduced project delays by 25% through proactive mitigation</li>
                  <li>Oversaw $500k+ cloud migration project improving system reliability by 40%</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-xl font-semibold">Education</h2>
            <div className="mt-4">
              <h3 className="font-medium">BS in Computer Science</h3>
              <p className="text-sm text-muted-foreground">Hack Canada University, 2025</p>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}