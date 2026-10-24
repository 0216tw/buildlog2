import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { AppRoutes } from './AppRoutes'

describe('AppRoutes', () => {
  it('로그인하지 않은 사용자를 로그인 준비 화면으로 보낸다', () => {
    render(
      <MemoryRouter initialEntries={['/app']}>
        <AppRoutes />
      </MemoryRouter>,
    )

    expect(screen.getByText('로그인 준비 화면')).toBeTruthy()
  })

  it('로그인한 사용자는 보호된 화면을 볼 수 있다', () => {
    render(
      <MemoryRouter initialEntries={['/app']}>
        <AppRoutes isAuthenticated />
      </MemoryRouter>,
    )

    expect(screen.getByText('내 기록 홈 준비 화면')).toBeTruthy()
  })
})
