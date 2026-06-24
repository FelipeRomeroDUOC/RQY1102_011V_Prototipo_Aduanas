import { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';

export default function ActualizarDeclaracion() {
  const { token } = useContext(AuthContext);
  const [decId, setDecId] = useState('');
  const [declaracion, setDeclaracion] = useState(null);
  const [resultado, setResultado] = useState('');
  const [observaciones, setObservaciones] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setDeclaracion(null);
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/sag/declaraciones/${decId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Declaración no encontrada');
      }

      const data = await response.json();
      setDeclaracion(data);
      setResultado(data.resultado);
      setObservaciones('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/sag/declaraciones/${declaracion.id}/resultado`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          resultado,
          observaciones
        })
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Error al actualizar declaración');
      }

      setSuccess('Declaración actualizada exitosamente');
      setDeclaracion({ ...declaracion, resultado, observaciones: declaracion.observaciones ? `${declaracion.observaciones}\n${observaciones}` : observaciones });
      setObservaciones('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg border-t-4 border-aduana-green">
        <h2 className="text-xl font-bold text-white mb-4">Buscar Declaración</h2>
        <form onSubmit={handleSearch} className="flex gap-4">
          <input
            type="number"
            required
            className="flex-1 bg-gray-700 text-white border border-gray-600 rounded px-4 py-2 focus:outline-none focus:border-aduana-green focus:ring-1 focus:ring-aduana-green"
            placeholder="ID de la Declaración (ej. 1)"
            value={decId}
            onChange={(e) => setDecId(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-aduana-green text-white px-6 py-2 rounded hover:bg-opacity-90 disabled:opacity-50"
          >
            Buscar
          </button>
        </form>
      </div>

      {error && (
        <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-900 border border-green-700 text-green-200 px-4 py-3 rounded">
          {success}
        </div>
      )}

      {declaracion && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Detalles de la Declaración #{declaracion.id}</h3>
          
          <div className="grid grid-cols-2 gap-4 mb-6 text-sm text-gray-300">
            <div>
              <span className="block text-gray-500">Viajero (RUT)</span>
              {declaracion.viajero}
            </div>
            <div>
              <span className="block text-gray-500">Fecha</span>
              {declaracion.fecha}
            </div>
            <div className="col-span-2">
              <span className="block text-gray-500">Productos Declarados</span>
              {declaracion.productos_declarados.join(', ') || 'Ninguno'}
            </div>
            <div>
              <span className="block text-gray-500">Incluye Mascotas</span>
              {declaracion.incluye_mascotas ? 'Sí' : 'No'}
            </div>
            <div className="col-span-2">
              <span className="block text-gray-500">Observaciones Actuales</span>
              <p className="whitespace-pre-wrap">{declaracion.observaciones || 'Ninguna'}</p>
            </div>
          </div>

          <form onSubmit={handleUpdate} className="space-y-4 border-t border-gray-700 pt-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Nuevo Resultado
              </label>
              <select
                className="w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:border-aduana-green focus:ring-1 focus:ring-aduana-green"
                value={resultado}
                onChange={(e) => setResultado(e.target.value)}
                disabled={isLoading}
              >
                <option value="PENDIENTE">PENDIENTE DE REVISIÓN</option>
                <option value="APROBADO">APROBADO</option>
                <option value="RETENIDO">RETENIDO (Inspección / Cuarentena)</option>
                <option value="DECOMISADO">DECOMISADO (Destrucción)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Añadir Observación
              </label>
              <textarea
                className="w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:border-aduana-green focus:ring-1 focus:ring-aduana-green"
                rows="3"
                value={observaciones}
                onChange={(e) => setObservaciones(e.target.value)}
                disabled={isLoading}
                placeholder="Motivo de retención, estado del animal, etc."
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-aduana-green text-white font-semibold py-2 rounded hover:bg-opacity-90 disabled:opacity-50"
            >
              Actualizar Declaración
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
