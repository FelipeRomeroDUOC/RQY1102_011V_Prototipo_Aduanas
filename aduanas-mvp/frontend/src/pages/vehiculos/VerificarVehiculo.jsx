import { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';

export default function VerificarVehiculo() {
  const [patente, setPatente] = useState('');
  const [vehiculo, setVehiculo] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useContext(AuthContext);

  const handleSearch = async (e) => {
    e.preventDefault();
    setError('');
    setVehiculo(null);
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/vehiculos/${patente.toUpperCase()}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Error al buscar vehículo');
      }
      
      setVehiculo(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadge = (estado) => {
    switch(estado) {
      case 'VALIDO': return <span className="bg-estado-valido text-white text-xs px-2 py-1 rounded">VÁLIDO</span>;
      case 'OBSERVADO': return <span className="bg-estado-observado text-white text-xs px-2 py-1 rounded">OBSERVADO</span>;
      case 'RECHAZADO': return <span className="bg-estado-rechazado text-white text-xs px-2 py-1 rounded">RECHAZADO</span>;
      default: return null;
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="bg-white p-6 rounded-lg shadow-sm border-t-4 border-aduana-blue">
        <h2 className="text-xl font-bold text-aduana-blue mb-4">Verificar Vehículo</h2>
        
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              required
              className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue uppercase"
              placeholder="Ingrese Patente"
              value={patente}
              onChange={(e) => setPatente(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className={`bg-aduana-blue text-white font-semibold py-2 px-6 rounded transition-colors ${isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-aduana-light'}`}
          >
            Buscar
          </button>
        </form>
        
        {error && (
          <div className="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
            {error}
          </div>
        )}
      </div>

      {vehiculo && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-semibold text-lg mb-4 border-b pb-2">Datos del Vehículo</h3>
            <div className="space-y-3 text-sm">
              <div className="grid grid-cols-2">
                <span className="text-gray-500">Patente:</span>
                <span className="font-bold">{vehiculo.patente}</span>
              </div>
              <div className="grid grid-cols-2">
                <span className="text-gray-500">Tipo:</span>
                <span>{vehiculo.tipo}</span>
              </div>
              <div className="grid grid-cols-2">
                <span className="text-gray-500">Marca / Modelo:</span>
                <span>{vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})</span>
              </div>
              <div className="grid grid-cols-2">
                <span className="text-gray-500">Placa:</span>
                <span className={vehiculo.tipo_placa === 'DIPLOMATICA' ? 'text-aduana-blue font-bold' : ''}>
                  {vehiculo.tipo_placa}
                </span>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-semibold text-lg mb-4 border-b pb-2">Última Salida Temporal</h3>
            
            {!vehiculo.ultima_salida_temporal ? (
              <p className="text-sm text-gray-500">No hay salidas temporales registradas.</p>
            ) : (
              <div className="space-y-3 text-sm">
                <div className="grid grid-cols-2">
                  <span className="text-gray-500">Estado de Trámite:</span>
                  <span>{getStatusBadge(vehiculo.ultima_salida_temporal.estado_documentos)}</span>
                </div>
                <div className="grid grid-cols-2">
                  <span className="text-gray-500">Fecha de Salida:</span>
                  <span>{vehiculo.ultima_salida_temporal.fecha_salida}</span>
                </div>
                <div className="grid grid-cols-2">
                  <span className="text-gray-500">Retorno Estimado:</span>
                  <span className="font-medium text-aduana-blue">{vehiculo.ultima_salida_temporal.fecha_retorno_estimada}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
