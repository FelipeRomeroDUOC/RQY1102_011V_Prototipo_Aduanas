import { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { API_URL } from '../../config';

export default function RegistrarCruce() {
  const [rutPasaporte, setRutPasaporte] = useState('');
  const [tipo, setTipo] = useState('INGRESO');
  const [estadoDocumentos, setEstadoDocumentos] = useState('VALIDO');
  const [observaciones, setObservaciones] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/v1/pdi/cruces`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          rut_pasaporte: rutPasaporte,
          tipo,
          estado_documentos: estadoDocumentos,
          observaciones
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al registrar cruce');
      }

      setSuccess(`Cruce registrado exitosamente para ${data.viajero.nombre} ${data.viajero.apellido}`);
      setRutPasaporte('');
      setObservaciones('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-sm border-t-4 border-aduana-blue">
      <h2 className="text-xl font-bold text-aduana-blue mb-6">Registrar Control Migratorio</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4 text-sm">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">RUT o Pasaporte del Viajero</label>
          <input
            type="text"
            required
            className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
            value={rutPasaporte}
            onChange={(e) => setRutPasaporte(e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Cruce</label>
            <select
              className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
              value={tipo}
              onChange={(e) => setTipo(e.target.value)}
              disabled={isLoading}
            >
              <option value="INGRESO">Ingreso a Chile</option>
              <option value="EGRESO">Egreso de Chile</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Estado de Documentos</label>
            <select
              className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
              value={estadoDocumentos}
              onChange={(e) => setEstadoDocumentos(e.target.value)}
              disabled={isLoading}
            >
              <option value="VALIDO">Válido</option>
              <option value="OBSERVADO">Observado</option>
              <option value="RECHAZADO">Rechazado</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Observaciones (Opcional)</label>
          <textarea
            className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
            rows="3"
            value={observaciones}
            onChange={(e) => setObservaciones(e.target.value)}
            disabled={isLoading}
          ></textarea>
        </div>

        <div className="pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full bg-aduana-blue text-white font-semibold py-2 rounded transition-colors ${isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-aduana-light'}`}
          >
            {isLoading ? 'Registrando...' : 'Registrar Cruce'}
          </button>
        </div>
      </form>
    </div>
  );
}
