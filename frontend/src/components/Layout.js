'use client'

import Navbar from './Navbar'
import HistorySidebar from './HistorySidebar'
import { useState, useEffect } from 'react'

export default function Layout({ children }) {
  const [isHistoryOpen, setIsHistoryOpen] = useState(false)
  const [isLargeScreen, setIsLargeScreen] = useState(false)

  useEffect(() => {
    // Only run on client side
    if (typeof window !== 'undefined') {
      const checkScreenSize = () => {
        const isLarge = window.innerWidth >= 1440
        setIsLargeScreen(isLarge)
        setIsHistoryOpen(isLarge) // Auto-open on large screens
      }

      // Initial check
      checkScreenSize()
      
      // Add event listener
      window.addEventListener('resize', checkScreenSize)
      
      // Clean up
      return () => window.removeEventListener('resize', checkScreenSize)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar onHistoryClick={() => setIsHistoryOpen(!isHistoryOpen)} />
      <HistorySidebar 
        isOpen={isLargeScreen || isHistoryOpen} 
        onClose={() => setIsHistoryOpen(false)}
      />
      <main className="container mx-auto px-4 py-6 max-w-5xl relative">
        {children}
      </main>
    </div>
  )
}