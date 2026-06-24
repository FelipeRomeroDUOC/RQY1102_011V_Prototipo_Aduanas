import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import { useContext } from 'react';

import RegistrarCruce from './pages/pdi/RegistrarCruce';
import VerificarViajero from './pages/pdi/VerificarViajero';

import RegistrarDeclaracion from './pages/sag/RegistrarDeclaracion';
import RegistrarSalidaTemporal from './pages/vehiculos/RegistrarSalidaTemporal';
import VerificarVehiculo from './pages/vehiculos/VerificarVehiculo';

const RootRedirect = () => {
  const { user } = useContext(AuthContext);
  if (!user) return <Navigate to="/login" replace />;
  if (user.rol === 'FUNCIONARIO_PDI') return <Navigate to="/pdi/registrar" replace />;
  if (user.rol === 'FUNCIONARIO_SAG') return <Navigate to="/sag/declaracion" replace />;
  if (user.rol === 'FUNCIONARIO_ADUANAS') return <Navigate to="/vehiculos/salida" replace />;
  return <Navigate to="/pdi/registrar" replace />; // Admin o default
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route path="/" element={<Layout />}>
            <Route index element={<RootRedirect />} />
            
            <Route path="pdi/registrar" element={
              <ProtectedRoute allowedRoles={['FUNCIONARIO_PDI']}><RegistrarCruce /></ProtectedRoute>
            } />
            <Route path="pdi/viajero" element={
              <ProtectedRoute allowedRoles={['FUNCIONARIO_PDI']}><VerificarViajero /></ProtectedRoute>
            } />
            
            <Route path="sag/declaracion" element={
              <ProtectedRoute allowedRoles={['FUNCIONARIO_SAG']}><RegistrarDeclaracion /></ProtectedRoute>
            } />
            
            <Route path="vehiculos/salida" element={
              <ProtectedRoute allowedRoles={['FUNCIONARIO_ADUANAS']}><RegistrarSalidaTemporal /></ProtectedRoute>
            } />
            <Route path="vehiculos/verificar" element={
              <ProtectedRoute allowedRoles={['FUNCIONARIO_ADUANAS']}><VerificarVehiculo /></ProtectedRoute>
            } />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
