'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState, useEffect, useRef } from 'react'

export default function ProductCard({ product }) {
  const [isHovered, setIsHovered] = useState(false)
  const [showTooltip, setShowTooltip] = useState(false)
  const [position, setPosition] = useState({ x: 0, y: 0 })
  const hoverTimer = useRef(null)

  const handleMouseEnter = () => {
    setIsHovered(true)
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
    setShowTooltip(false)
    clearTimeout(hoverTimer.current)
  }

  const handleMouseMove = (e) => {
    // Update position immediately
    setPosition({
      x: e.clientX + 15,
      y: e.clientY + 15
    })

    // Hide tooltip when mouse moves
    setShowTooltip(false)
    
    // Clear any existing timer
    clearTimeout(hoverTimer.current)
    
    // Start new timer to show tooltip after 1 second of no movement
    hoverTimer.current = setTimeout(() => {
      if (isHovered) {
        setShowTooltip(true)
      }
    }, 500)
  }

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      clearTimeout(hoverTimer.current)
    }
  }, [])

  return (
    <div className="relative">
      <Link href={`/products/${product.id}`} passHref>
        <div 
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 cursor-pointer h-full flex flex-col"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onMouseMove={handleMouseMove}
        >
          {/* Product Image */}
          <div className="h-48 relative flex-shrink-0">
            <Image
              src={product.image}
              alt={product.title}
              fill
              className="object-contain transition-opacity duration-300 p-4"
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            />
          </div>
          
          {/* Product Info */}
          <div className="p-4 flex-grow flex flex-col">
            <h3 className="text-lg text-gray-800 font-semibold mb-1 line-clamp-1">{product.title}</h3>
            <p className="text-gray-600 text-sm mb-2 line-clamp-2">
              {product.description.substring(0, 60)}...
            </p>
            <p className="text-indigo-600 font-bold mt-auto">${product.price}</p>
          </div>
        </div>
      </Link>

      {/* OS-style hover tooltip with delayed appearance */}
      {isHovered && (
        <div 
          className={`fixed z-50 bg-white/40 backdrop-blur-sm shadow-xl rounded-md p-4 max-w-xs border border-gray-200 pointer-events-none transition-opacity duration-200 ${
            showTooltip ? 'opacity-100' : 'opacity-0'
          }`}
          style={{
            left: `${position.x}px`,
            top: `${position.y}px`,
          }}
        >
          <p className="text-gray-700 text-xs mb-2">{product.description}</p>
        </div>
      )}
    </div>
  )
}