// config.js
// Exporta la URL base de la API. En desarrollo usa localhost, en producción usa la variable de entorno configurada en Render.
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
