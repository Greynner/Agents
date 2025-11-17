import { NextRequest, NextResponse } from 'next/server';

const MODAL_BASE_URL = process.env.MODAL_BASE_URL || '';
const MODAL_API_KEY = process.env.MODAL_API_KEY;
const PROXY_TIMEOUT = parseInt(process.env.MODAL_PROXY_TIMEOUT || '60', 10) * 1000; // Convertir a ms

export async function POST(request: NextRequest) {
  // Manejar CORS
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Manejar preflight
  if (request.method === 'OPTIONS') {
    return NextResponse.json({}, { status: 204, headers: corsHeaders });
  }

  try {
    // Validar que MODAL_BASE_URL esté configurada
    if (!MODAL_BASE_URL) {
      console.error('❌ MODAL_BASE_URL no está configurada');
      return NextResponse.json(
        {
          error: 'MODAL_BASE_URL no está configurada en las variables de entorno de Vercel',
          detail: 'Configura MODAL_BASE_URL en Vercel',
        },
        {
          status: 500,
          headers: corsHeaders,
        }
      );
    }

    // Construir la URL del endpoint de Modal
    const modalEndpoint = `${MODAL_BASE_URL.replace(/\/$/, '')}/analizar-requerimiento`;
    
    // Obtener el body de la petición
    const body = await request.json();

    // Preparar headers
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (MODAL_API_KEY) {
      headers['Authorization'] = `Bearer ${MODAL_API_KEY}`;
    }

    console.log(`🔄 Proxying POST to ${modalEndpoint}`);

    // Hacer la petición a Modal
    const response = await fetch(modalEndpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(PROXY_TIMEOUT),
    });

    // Obtener la respuesta
    const data = await response.json();

    // Retornar la respuesta con CORS
    return NextResponse.json(data, {
      status: response.status,
      headers: corsHeaders,
    });
  } catch (error: any) {
    console.error('❌ Error en proxy:', error);

    // Manejar timeout
    if (error.name === 'AbortError' || error.name === 'TimeoutError') {
      return NextResponse.json(
        {
          error: `Timeout al conectar con Modal (>${PROXY_TIMEOUT / 1000}s)`,
        },
        {
          status: 504,
          headers: corsHeaders,
        }
      );
    }

    // Otros errores
    return NextResponse.json(
      {
        error: error.message || 'Error inesperado en el proxy',
        detail: 'Revisa los logs del servidor',
      },
      {
        status: 500,
        headers: corsHeaders,
      }
    );
  }
}

// También manejar OPTIONS para CORS
export async function OPTIONS() {
  return NextResponse.json(
    {},
    {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    }
  );
}

