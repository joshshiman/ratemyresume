"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

interface ChatInterfaceProps {
  selectedText: string
  jobDescription: string
}

interface Message {
  text: string
  type: "input" | "response"
}

export default function ChatInterface({ selectedText, jobDescription }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState("")

  const handleSubmit = async () => {
    if (!inputText) return

    const newMessage: Message = { text: inputText, type: "input" }
    setMessages((prev) => [...prev, newMessage])

    try {
      const response = await fetch("http://34.130.198.88:8000/tailor-resume", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_description: jobDescription,
          resume_bullet: inputText,
        }),
      })

      const data = await response.json()
      const responseMessage: Message = {
        text: data.tailored_bullet,
        type: "response",
      }

      setMessages((prev) => [...prev, responseMessage])
    } catch (error) {
      console.error("Error:", error)
    }

    setInputText("")
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b p-4">
        <h2 className="text-lg font-semibold">Resume Tailor</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`rounded-lg p-3 ${
                message.type === "input" ? "bg-muted text-muted-foreground" : "bg-primary text-primary-foreground"
              }`}
            >
              {message.text}
            </div>
          ))}
        </div>
      </div>
      <div className="border-t p-4">
        <div className="space-y-4">
          <Textarea
            value={inputText || selectedText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Paste your resume bullet point here..."
            className="min-h-[100px]"
          />
          <Button onClick={handleSubmit} className="w-full">
            Tailor Resume Bullet
          </Button>
        </div>
      </div>
    </div>
  )
}

