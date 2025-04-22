export default function HistorySidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Overlay - only for mobile/tablet */}
      {(isOpen) && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        ></div>
      )}

      {/* Sidebar */}
      <div className={`
        fixed top-0 h-full w-64 bg-white shadow-lg z-50 transition-all duration-300 ease-in-out
        lg:right-0 lg:translate-x-0
        ${isOpen ? 'right-0' : '-right-full'}
      `}>
        <div className="p-4 flex justify-between items-center border-b">
          <h2 className="text-lg text-gray-800 font-semibold">Recent History</h2>
          <button 
            onClick={onClose} 
            className="lg:hidden p-1 rounded-full hover:bg-gray-100"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="p-4">
          <p className="text-gray-500">Your viewed products will appear here</p>
        </div>
      </div>
    </>
  )
}