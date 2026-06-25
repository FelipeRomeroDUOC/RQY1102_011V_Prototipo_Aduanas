import { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { API_URL } from '../../config';

export default function RegistrarDeclaracion() {
  const [rutPasaporte, setRutPasaporte] = useState('');
  const [cruceId, setCruceId] = useState('');
  const [incluyeMascotas, setIncluyeMascotas] = useState(false);
  const [productosDeclarados, setProductosDeclarados] = useState('');
  const [resultado, setResultado] = useState('PENDIENTE');
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
      const prodArray = productosDeclarados.split(',').map(p => p.trim()).filter(p => p);
      
      const response = await fetch(`${API_URL}/api/v1/sag/declaraciones`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          rut_pasaporte: rutPasaporte,
          cruce_id: cruceId ? parseInt(cruceId) : null,
          productos_declarados: prodArray,
          incluye_mascotas: incluyeMascotas,
          observaciones
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al registrar declaración');
      }

      setSuccess(`Declaración #${data.id} registrada exitosamente para ${data.viajero}`);
      
      if (resultado !== 'PENDIENTE') {
        const updateResponse = await fetch(`${API_URL}/api/v1/sag/declaraciones/${data.id}/resultado`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            resultado,
            observaciones: 'Resultado actualizado en registro'
          })
        });
        
        if (!updateResponse.ok) {
          throw new Error('Declaración registrada, pero falló la actualización del resultado');
        }
        setSuccess(`Declaración #${data.id} registrada y actualizada a ${resultado}`);
      }

      setProductosDeclarados('');
      setIncluyeMascotas(false);
      setObservaciones('');

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-sm border-t-4 border-aduana-blue">
      <h2 className="text-xl font-bold text-aduana-blue mb-6">Declaración Jurada SAG</h2>
      
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
        <div className="grid grid-cols-2 gap-4">
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
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">ID Cruce (Opcional)</label>
            <input
              type="number"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
              value={cruceId}
              onChange={(e) => setCruceId(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Productos Declarados (separados por coma)</label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
            placeholder="Ej: manzanas, queso, embutidos"
            value={productosDeclarados}
            onChange={(e) => setProductosDeclarados(e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            id="mascotas"
            className="h-4 w-4 text-aduana-blue border-gray-300 rounded focus:ring-aduana-blue"
            checked={incluyeMascotas}
            onChange={(e) => setIncluyeMascotas(e.target.checked)}
            disabled={isLoading}
          />
          <label htmlFor="mascotas" className="ml-2 block text-sm text-gray-700">
            ¿Incluye animales o mascotas vivas?
          </label>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Resultado del Control</label>
          <select
            className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
            value={resultado}
            onChange={(e) => setResultado(e.target.value)}
            disabled={isLoading}
          >
            <option value="PENDIENTE">PENDIENTE DE REVISIÓN</option>
            <option value="APROBADO">APROBADO</option>
            <option value="RETENIDO">RETENIDO</option>
            <option value="DECOMISADO">DECOMISADO</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Observaciones</label>
          <textarea
            className="w-full border border-gray-300 rounded px-3 py-2 focus:ring-aduana-blue focus:border-aduana-blue"
            rows="2"
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
            {isLoading ? 'Registrando...' : 'Confirmar Declaración'}
          </button>
        </div>
      </form>
    </div>
  );
}
