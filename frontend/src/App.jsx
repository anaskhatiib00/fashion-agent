import { useEffect, useState } from "react"
import { createItem, getItems, getExportUrl } from "./services/api"

function App() {
  const [title, setTitle] = useState("")
  const [price, setPrice] = useState("")
  const [quantity, setQuantity] = useState("")
  const [size, setSize] = useState("")
  const [color, setColor] = useState("")
  const [notes, setNotes] = useState("")
  const [frontImage, setFrontImage] = useState(null)
  const [backImage, setBackImage] = useState(null)
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)
  const [items, setItems] = useState([])

  const loadItems = async () => {
    try {
      const data = await getItems()
      setItems(data.items)
    } catch (error) {
      console.error("Failed to load items", error)
    }
  }

  useEffect(() => {
    loadItems()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage("")
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append("title", title)
      formData.append("price", price)
      formData.append("quantity", quantity)
      formData.append("size", size)
      formData.append("color", color)
      formData.append("notes", notes)
      formData.append("front_image", frontImage)
      formData.append("back_image", backImage)

      const data = await createItem(formData)
      setMessage(data.message)

      setTitle("")
      setPrice("")
      setQuantity("")
      setSize("")
      setColor("")
      setNotes("")
      setFrontImage(null)
      setBackImage(null)

      e.target.reset()
      loadItems()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "40px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Fashion Agent</h1>
      <p>Add a clothing item</p>

      <form
        onSubmit={handleSubmit}
        style={{ display: "grid", gap: "12px", marginBottom: "30px" }}
      >
        <input
          type="text"
          placeholder="Item title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Size"
          value={size}
          onChange={(e) => setSize(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          required
        />

        <textarea
          placeholder="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <label>Front Image</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFrontImage(e.target.files[0])}
          required
        />

        <label>Back Image</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setBackImage(e.target.files[0])}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Item"}
        </button>
      </form>

      {message && <p style={{ marginBottom: "20px" }}>{message}</p>}

      <a
        href={getExportUrl()}
        target="_blank"
        rel="noreferrer"
        style={{
          display: "inline-block",
          marginBottom: "20px",
          padding: "10px 16px",
          background: "#111",
          color: "#fff",
          textDecoration: "none",
          borderRadius: "6px",
        }}
      >
        Export Excel
      </a>

      <h2>Saved Items</h2>

      {items.length === 0 ? (
        <p>No items yet.</p>
      ) : (
        <div style={{ display: "grid", gap: "16px" }}>
          {items.map((item) => (
            <div
              key={item.id}
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "16px",
              }}
            >
              <h3>{item.title}</h3>
              <p><strong>Price:</strong> {item.price}</p>
              <p><strong>Quantity:</strong> {item.quantity}</p>
              <p><strong>Size:</strong> {item.size}</p>
              <p><strong>Color:</strong> {item.color}</p>
              <p><strong>Notes:</strong> {item.notes || "No notes"}</p>

              <div
                style={{
                  marginTop: "12px",
                  padding: "12px",
                  background: "#f7f7f7",
                  borderRadius: "6px",
                }}
              >
                <strong>AI Output:</strong>
                <pre style={{ whiteSpace: "pre-wrap", marginTop: "8px" }}>
                  {item.ai_output || "No AI output yet"}
                </pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App