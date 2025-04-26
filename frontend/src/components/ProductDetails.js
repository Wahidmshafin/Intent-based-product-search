'use client'

import Image from 'next/image'
import { useState } from 'react'

export default function ProductDetails({ product }) {
  const [quantity, setQuantity] = useState(1)

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="md:flex">
        {/* Product Image */}
        <div className="md:w-1/2 p-8">
          <div className="h-96 relative">
            <Image
              src={product.image}
              alt={product.title}
              fill
              className="object-contain"
              priority
            />
          </div>
        </div>
        
        {/* Product Info */}
        <div className="p-8 md:w-1/2">
          <h1 className="text-2xl text-gray-700 font-bold mb-2">{product.title}</h1>
          <div className="flex items-center mb-4">
            <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded">
              {product.category}
            </span>
            <div className="ml-2 flex items-center">
              {[...Array(5)].map((_, i) => (
                <svg
                  key={i}
                  className={`w-4 h-4 ${i < Math.round(product.rating.rate) ? 'text-yellow-300' : 'text-gray-300'}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
              <span className="text-gray-600 text-sm ml-1">
                ({product.rating.count})
              </span>
            </div>
          </div>
          <p className="text-indigo-600 text-2xl font-bold mb-6">${product.price}</p>
          <p className="text-gray-700 mb-6">{product.description}</p>
          
          <div className="flex text-gray-500 items-center mb-6">
            <button 
              onClick={() => setQuantity(q => Math.max(1, q - 1))}
              className="px-3 py-1 border border-gray-300 rounded-l-md"
            >
              -
            </button>
            <span className="px-4 py-1 border-t border-b border-gray-300">
              {quantity}
            </span>
            <button 
              onClick={() => setQuantity(q => q + 1)}
              className="px-3 py-1 border border-gray-300 rounded-r-md"
            >
              +
            </button>
          </div>
          
          <div className="flex space-x-4">
            <button className="bg-indigo-600 text-white px-6 py-2 rounded-full hover:bg-indigo-700 transition-colors">
              Add to Cart ({quantity})
            </button>
            <button className="border border-indigo-600 text-indigo-600 px-6 py-2 rounded-full hover:bg-indigo-50 transition-colors">
              Save for Later
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}