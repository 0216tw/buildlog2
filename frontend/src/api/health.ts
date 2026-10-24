import { apiBaseUrl } from '../config/env'

export type HealthResponse = {
  status: 'ok'
}

function isHealthResponse(value: unknown): value is HealthResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    value.status === 'ok'
  )
}

export async function fetchHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const response = await fetch(`${apiBaseUrl}/health`, {
    headers: { Accept: 'application/json' },
    signal,
  })

  if (!response.ok) {
    throw new Error(`상태 확인 요청 실패: ${response.status}`)
  }

  const data: unknown = await response.json()
  if (!isHealthResponse(data)) {
    throw new Error('상태 확인 응답 형식이 올바르지 않습니다.')
  }

  return data
}
