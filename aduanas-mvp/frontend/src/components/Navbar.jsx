import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  if (!user) return null;

  return (
    <nav className="bg-aduana-blue text-white w-64 min-h-screen flex flex-col fixed left-0 top-0">
      <div className="p-4 bg-aduana-light font-bold text-lg text-center">
        Aduanas Chile
      </div>
      
      <div className="flex-1 p-4 flex flex-col gap-2">
        {(user.rol === 'FUNCIONARIO_PDI' || user.rol === 'ADMINISTRADOR') && (
          <>
            <div className="text-xs uppercase text-gray-300 font-semibold mt-4 mb-2">PDI Migraciones</div>
            <Link to="/pdi/registrar" className="hover:bg-aduana-light p-2 rounded">Registrar Cruce</Link>
            <Link to="/pdi/viajero" className="hover:bg-aduana-light p-2 rounded">Verificar Viajero</Link>
          </>
        )}
        
        {(user.rol === 'FUNCIONARIO_SAG' || user.rol === 'ADMINISTRADOR') && (
          <>
            <div className="text-xs uppercase text-gray-300 font-semibold mt-4 mb-2">SAG Fitosanitario</div>
            <Link to="/sag/declaracion" className="hover:bg-aduana-light p-2 rounded">Nueva Declaración</Link>
            <Link to="/sag/actualizar" className="hover:bg-aduana-light p-2 rounded">Actualizar Declaración</Link>
          </>
        )}
        
        {(user.rol === 'FUNCIONARIO_ADUANAS' || user.rol === 'ADMINISTRADOR') && (
          <>
            <div className="text-xs uppercase text-gray-300 font-semibold mt-4 mb-2">Aduanas Vehículos</div>
            <Link to="/vehiculos/salida" className="hover:bg-aduana-light p-2 rounded">Salida Temporal</Link>
            <Link to="/vehiculos/verificar" className="hover:bg-aduana-light p-2 rounded">Verificar Vehículo</Link>
          </>
        )}
      </div>

      <div className="p-4 border-t border-aduana-light">
        <div className="text-sm mb-2 font-semibold">{user.nombre} {user.apellido}</div>
        <div className="text-xs text-gray-300 mb-4">{user.rol}</div>
        <button 
          onClick={() => logout()}
          className="w-full bg-red-600 hover:bg-red-700 text-white py-1 rounded text-sm transition-colors"
        >
          Cerrar Sesión
        </button>
      </div>
    </nav>
  );
}
