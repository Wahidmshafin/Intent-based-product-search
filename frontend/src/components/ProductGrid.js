'use client'

import { useState, useEffect } from 'react'
import ProductCard from './ProductCard'

export default function ProductGrid({ products }) {
  const [visibleProducts, setVisibleProducts] = useState([])
  const [page, setPage] = useState(1)
  const productsPerPage = 9

  useEffect(() => {
    // Initial load
    setVisibleProducts(products.slice(0, productsPerPage))
  }, [products])

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
        document.documentElement.offsetHeight - 200
      ) {
        loadMoreProducts()
      }
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [page, products])

  const loadMoreProducts = () => {
    const nextPage = page + 1
    const startIndex = (nextPage - 1) * productsPerPage
    const endIndex = startIndex + productsPerPage

    if (startIndex < products.length) {
      setVisibleProducts(prev => [...prev, ...products.slice(startIndex, endIndex)])
      setPage(nextPage)
    }
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {visibleProducts.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
