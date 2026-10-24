import { useEffect, useState } from 'react'
import { fetchHealth } from '../api/health'

type ConnectionState = 'loading' | 'success' | 'error'

export function HealthPage() {
  const [connectionState, setConnectionState] =
    useState<ConnectionState>('loading')
  const [requestCount, setRequestCount] = useState(0)

  useEffect(() => {
    const controller = new AbortController()

    fetchHealth(controller.signal)
      .then(() => setConnectionState('success'))
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') {
          return
        }
        setConnectionState('error')
      })

    return () => controller.abort()
  }, [requestCount])

  const retryConnection = () => {
    setConnectionState('loading')
    setRequestCount((count) => count + 1)
  }

  const messages = {
    loading: {
      title: '서버에 연결하는 중입니다.',
      detail: '잠시만 기다려 주세요.',
    },
    success: {
      title: '백엔드 연결에 성공했습니다.',
      detail: 'BuildLog 개발 준비가 정상적으로 동작합니다.',
    },
    error: {
      title: '백엔드에 연결할 수 없습니다.',
      detail: 'FastAPI 서버가 실행 중인지 확인해 주세요.',
    },
  } satisfies Record<ConnectionState, { title: string; detail: string }>

  const message = messages[connectionState]

  return (
    <main className="app-shell">
      <p className="brand">BUILDLOG</p>
      <section className="status-card">
        <h1>개발 연결 확인</h1>
        <p className="description">
          React 화면에서 FastAPI 상태 확인 API를 호출합니다.
        </p>
        <div
          className="status-box"
          data-state={connectionState}
          aria-live="polite"
        >
          <span className="status-dot" aria-hidden="true" />
          <div className="status-copy">
            <strong>{message.title}</strong>
            <span>{message.detail}</span>
          </div>
        </div>
        {connectionState === 'error' && (
          <button
            className="retry-button"
            type="button"
            onClick={retryConnection}
          >
            다시 확인
          </button>
        )}
      </section>
    </main>
  )
}
