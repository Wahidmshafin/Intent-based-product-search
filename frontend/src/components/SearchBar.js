'use client'

export default function SearchBar() {
  function handleSubmit(event) {
    event.preventDefault()
    const query = event.target.elements.query.value
    console.log('Search query:', query)
    // You would typically add your search logic here
  }

  return (
    <form onSubmit={handleSubmit} className="relative w-full text-gray-700">
      <input
        type="text"
        name="query" // Added name attribute for form access
        placeholder="Search products..."
        className="w-full py-2 text-gray-700 px-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
      />
      <button type="submit" className="absolute right-3 top-1/2 transform -translate-y-1/2">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
    </form>
  )
}