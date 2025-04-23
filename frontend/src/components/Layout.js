'use client'

import Navbar from './Navbar'
import HistorySidebar from './HistorySidebar'
import { useState } from 'react'

export default function Layout({ children }) {
  const [isHistoryOpen, setIsHistoryOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar onHistoryClick={() => setIsHistoryOpen(!isHistoryOpen)} />
      <HistorySidebar 
        isOpen={isHistoryOpen} 
        onClose={() => setIsHistoryOpen(false)}
      />
      <main className="container mx-auto px-4 py-6 max-w-5xl relative">
        {children}
      </main>
    </div>
  )
}