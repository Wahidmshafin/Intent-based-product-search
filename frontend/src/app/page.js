import Layout from '@/components/Layout'
import ProductGrid from '@/components/ProductGrid'

async function getProducts() {
  try {
    const res = await fetch('https://fakestoreapi.com/products')
    if (!res.ok) {
      throw new Error('Failed to fetch products')
    }
    return res.json()
  } catch (error) {
    console.error('Error fetching products:', error)
    return []
  }
}

export default async function Home() {
  const products = await getProducts()

  return (
    <Layout>
      {/* <h1 className="text-2xl font-bold mb-6">Featured Products</h1> */}
      <ProductGrid products={products} />
    </Layout>
  )
}