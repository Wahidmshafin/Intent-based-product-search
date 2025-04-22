import Layout from '@/components/Layout'
import ProductDetails from '@/components/ProductDetails'

async function getProduct(id) {
  try {
    const res = await fetch(`https://fakestoreapi.com/products/${id}`)
    if (!res.ok) {
      throw new Error('Failed to fetch product')
    }
    return res.json()
  } catch (error) {
    console.error('Error fetching product:', error)
    return null
  }
}

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)

  if (!product) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold">Product not found</h1>
          <p className="mt-4">The product you're looking for doesn't exist.</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto py-8">
        <ProductDetails product={product} />
      </div>
    </Layout>
  )
}