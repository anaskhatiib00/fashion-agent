const API_URL = "http://127.0.0.1:8000"

export async function createItem(formData) {
  const response = await fetch(`${API_URL}/api/items`, {
    method: "POST",
    body: formData,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || data.message || "Failed to create item")
  }

  return data
}

export async function getItems() {
  const response = await fetch(`${API_URL}/api/items`)

  if (!response.ok) {
    throw new Error("Failed to fetch items")
  }

  return response.json()
}

export function getExportUrl() {
  return `${API_URL}/api/items/export`
}