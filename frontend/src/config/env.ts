const defaultApiBaseUrl = 'http://127.0.0.1:8000/api'

export const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL || defaultApiBaseUrl
).replace(/\/+$/, '')
