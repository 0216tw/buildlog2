import { Navigate, Route, Routes } from 'react-router-dom'
import { ProtectedRoute } from '../components/ProtectedRoute'
import { DashboardPage } from '../pages/DashboardPage'
import { HealthPage } from '../pages/HealthPage'
import { LoginPage } from '../pages/LoginPage'

type AppRoutesProps = {
  isAuthenticated?: boolean
}

export function AppRoutes({ isAuthenticated = false }: AppRoutesProps) {
  return (
    <Routes>
      <Route path="/" element={<HealthPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
        <Route path="/app" element={<DashboardPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
