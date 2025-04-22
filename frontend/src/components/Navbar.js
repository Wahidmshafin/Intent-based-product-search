import SearchBar from './SearchBar'
import Link from 'next/link'

export default function Navbar({ onHistoryClick }) {
  return (
    <nav className="bg-white shadow-md py-4 px-6">
      <div className="flex items-center justify-between max-w-5xl mx-auto">
        {/* Logo and Hamburger (mobile) */}
        <div className="flex items-center space-x-4">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/">
              <span className="text-xl font-bold text-indigo-600 cursor-pointer">ShopNow</span>
            </Link>
          </div>
        </div>

        {/* Search Bar - Hidden on small screens */}
        <div className="hidden md:flex flex-1 mx-8 max-w-md">
          <SearchBar />
        </div>

        {/* Account and History */}
        <div className="flex text-gray-700 items-center space-x-4">
          {/* History button - visible on all screens */}
          <button 
            onClick={onHistoryClick}
            className="p-2 rounded-full hover:bg-gray-100"
          >
            {/* Clock icon for medium+ screens, Hamburger for small screens */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path className="hidden md:block" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path className="md:hidden" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Account */}
          <button className="p-2 rounded-full hover:bg-gray-100">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Search Bar - Visible only on small screens */}
      <div className="mt-4 md:hidden max-w-md mx-auto">
        <SearchBar />
      </div>
    </nav>
  )
}