"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Loader2 } from "lucide-react"

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
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setInputText(selectedText)
  }, [selectedText])

  const handleSubmit = async () => {
    if (!inputText || isLoading) return

    const newMessage: Message = { text: inputText, type: "input" }
    setMessages((prev) => [...prev, newMessage])
    setIsLoading(true)

    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 60000) // 60 second timeout

      const response = await fetch("http://localhost:8000/tailor-resume", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Origin: window.location.origin, // Add this line
        },
        body: JSON.stringify({
          job_description: jobDescription,
          resume_bullet: inputText,
        }),
        mode: "cors", // Add this line
        credentials: "same-origin", // Add this line
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      const responseMessage: Message = {
        text: data.tailored_bullet,
        type: "response",
      }

      setMessages((prev) => [...prev, responseMessage])
    } catch (error) {
      console.error("Error:", error)
      const errorMessage: Message = {
        text:
          error instanceof Error && error.name === "AbortError"
            ? "The request took too long. The AI might be busy. Please try again."
            : "An error occurred while tailoring the resume bullet. Please try again.",
        type: "response",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setInputText("")
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b p-4 flex items-center justify-center">
        <Image src="/ratemyresume.svg" alt="RatemyResume Logo" width={200} height={50} priority />
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
          {isLoading && (
            <div className="flex items-center justify-center">
              <Loader2 className="h-6 w-6 animate-spin" />
              <span className="ml-2">Tailoring resume bullet...</span>
            </div>
          )}
        </div>
      </div>
      <div className="border-t p-4">
        <div className="space-y-4">
          <Textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Paste your resume bullet point here..."
            className="min-h-[100px]"
          />
          <Button onClick={handleSubmit} className="w-full" disabled={isLoading}>
            {isLoading ? "Tailoring..." : "Tailor Resume Bullet"}
          </Button>
        </div>
      </div>
    </div>
  )
}

