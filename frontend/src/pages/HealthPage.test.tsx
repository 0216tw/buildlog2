import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { HealthPage } from './HealthPage'

describe('HealthPage', () => {
  it('연결 중 상태를 먼저 보여준다', () => {
    vi.stubGlobal('fetch', vi.fn(() => new Promise(() => undefined)))

    render(<HealthPage />)

    expect(screen.getByText('서버에 연결하는 중입니다.')).toBeTruthy()
  })

  it('상태 확인 API가 성공하면 연결 성공을 보여준다', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ status: 'ok' }),
      }),
    )

    render(<HealthPage />)

    expect(
      await screen.findByText('백엔드 연결에 성공했습니다.'),
    ).toBeTruthy()
  })

  it('상태 확인 API가 실패하면 실패 안내를 보여준다', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('network error')))

    render(<HealthPage />)

    expect(
      await screen.findByText('백엔드에 연결할 수 없습니다.'),
    ).toBeTruthy()
    expect(screen.getByRole('button', { name: '다시 확인' })).toBeTruthy()
  })
})
