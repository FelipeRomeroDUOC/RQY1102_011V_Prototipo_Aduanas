import { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { API_URL } from '../../config';

export default function VerificarViajero() {
  const [rutPasaporte, setRutPasaporte] = useState('');
  const [viajero, setViajero] = useState(null);
  const [historial, setHistorial] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useContext(AuthContext);

  const handleSearch = async (e) => {
    e.preventDefault();
    setError('');
    setViajero(null);
    setHistorial([]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/v1/pdi/viajeros/${rutPasaporte}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Error al buscar viajero');
      }
      
      setViajero(data);
      
      // Fetch historial
      const histResponse = await fetch(`${API_URL}/api/v1/pdi/cruces/${rutPasaporte}/historial?limite=5`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (histResponse.ok) {
        const histData = await histResponse.json();
        setHistorial(histData.cruces || []);
      }
      
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
        <h2 className="text-xl font-bold text-aduana-blue mb-4">Verificar Viajero</h2>
        
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              required
              className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
              placeholder="Ingrese RUT o Pasaporte"
              value={rutPasaporte}
              onChange={(e) => setRutPasaporte(e.target.value)}
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

      {viajero && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-semibold text-lg mb-4 border-b pb-2">Datos del Viajero</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-gray-500">Nombre Completo</div>
                <div className="font-medium">{viajero.nombre} {viajero.apellido}</div>
              </div>
              <div>
                <div className="text-gray-500">Documento ({viajero.tipo_documento})</div>
                <div className="font-medium">{viajero.rut_pasaporte}</div>
              </div>
              <div>
                <div className="text-gray-500">Nacionalidad</div>
                <div className="font-medium">{viajero.nacionalidad}</div>
              </div>
              <div>
                <div className="text-gray-500">Fecha de Nacimiento</div>
                <div className="font-medium">{viajero.fecha_nacimiento}</div>
              </div>
            </div>
          </div>
          
          <div className="md:col-span-2 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-semibold text-lg mb-4 border-b pb-2">Últimos Cruces Registrados</h3>
            
            {historial.length === 0 ? (
              <p className="text-sm text-gray-500">No hay cruces registrados para este viajero.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left table-auto">
                  <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                      <th className="px-4 py-2">Fecha/Hora</th>
                      <th className="px-4 py-2">Tipo</th>
                      <th className="px-4 py-2">Estado</th>
                      <th className="px-4 py-2">Funcionario</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historial.map((cruce) => (
                      <tr key={cruce.id} className="border-b">
                        <td className="px-4 py-3 font-medium text-gray-900">{cruce.fecha_hora}</td>
                        <td className="px-4 py-3">{cruce.tipo}</td>
                        <td className="px-4 py-3">{getStatusBadge(cruce.estado_documentos)}</td>
                        <td className="px-4 py-3">{cruce.funcionario}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
