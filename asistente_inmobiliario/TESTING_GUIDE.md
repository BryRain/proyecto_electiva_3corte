# 📋 GUÍA COMPLETA DE PRUEBAS - FRONTEND

**Documento de Testing para Asistente Inmobiliario IA**  
**Fecha:** Mayo 27, 2026  
**Propósito:** Validar todas las funcionalidades del frontend

---

## 🚀 INICIO RÁPIDO

### 1. Iniciar la Aplicación

```bash
# Terminal 1: Backend
cd c:\Users\Bryan\Documents\proyecto_electiva_3Corte\asistente_inmobiliario
python backend/app.py

# Terminal 2: Ir a localhost
http://localhost:5000
```

### 2. Verificar que esté funcionando
```
✓ Página muestra "Asistente Inmobiliario IA"
✓ Formulario de login visible
✓ No hay errores en consola (F12)
```

---

## 📍 FUNCIONALIDAD 1: AUTENTICACIÓN (LOGIN/REGISTRO)

### Test 1.1: Registro de Usuario Nuevo

**Objetivo:** Crear una nueva cuenta

**Pasos:**
```
1. En pantalla de login, hacer clic "¿No tienes cuenta? Registrarse"
2. Completar formulario:
   - Email:    test.user@example.com
   - Usuario:  testuser123
   - Nombre:   Juan Pérez
   - Contraseña: Password123
   - Confirmar: Password123
3. Hacer clic "Registrarse"
```

**Datos de Prueba:**
```json
{
  "email": "test.user@example.com",
  "username": "testuser123",
  "full_name": "Juan Pérez",
  "password": "Password123"
}
```

**Resultado Esperado:**
```
✓ Mensaje: "Registro exitoso. Por favor inicia sesión."
✓ Email se carga en campo de login
✓ Formulario de login se muestra automáticamente
```

**Validaciones:**
- ✓ Email debe ser válido (contener @)
- ✓ Contraseñas deben coincidir
- ✓ Contraseña mínimo 6 caracteres
- ✓ Usuario único (no permitir duplicados)

---

### Test 1.2: Login Exitoso

**Objetivo:** Iniciar sesión con credenciales correctas

**Pasos:**
```
1. En pantalla de login
2. Email:     test.user@example.com
3. Contraseña: Password123
4. Hacer clic "Ingresar"
```

**Resultado Esperado:**
```
✓ Redirecciona al dashboard
✓ Mostrar "Hola, testuser123" en esquina superior
✓ Tabs visibles: Búsqueda IA, Propiedades, Favoritos, Agentes, Documentos
✓ Token guardado en localStorage
```

**Verificar en Consola (F12):**
```javascript
// Abrir Console y ejecutar:
localStorage.getItem('user')
// Debe retornar: {"id": 1, "username": "testuser123", "email": "..."}
```

---

### Test 1.3: Login Fallido (Contraseña Incorrecta)

**Objetivo:** Validar mensaje de error

**Pasos:**
```
1. Email:     test.user@example.com
2. Contraseña: ContraseñaIncorrecta
3. Hacer clic "Ingresar"
```

**Resultado Esperado:**
```
✓ Mensaje de error: "Email o contraseña incorrectos"
✓ Permanecer en pantalla de login
✓ NO redireccionar al dashboard
```

---

### Test 1.4: Logout

**Objetivo:** Cerrar sesión

**Pasos:**
```
1. Estar logueado (después del Test 1.2)
2. Hacer clic botón "Salir" (esquina superior derecha)
3. Confirmar "¿Seguro que deseas cerrar sesión?"
```

**Resultado Esperado:**
```
✓ Token se borra de localStorage
✓ Redirecciona a pantalla de login
✓ Todos los campos limpios
```

---

## 🔍 FUNCIONALIDAD 2: BÚSQUEDA INTELIGENTE CON IA

### Test 2.1: Búsqueda Simple

**Objetivo:** Ejecutar búsqueda con IA y ver resultados de agentes

**Pasos:**
```
1. Estar logueado
2. Ir a tab "🔍 Búsqueda IA"
3. En buscador, escribir exactamente:
   "Busco apartamento de 2 habitaciones en Medellín, máximo $300,000"
4. Presionar Enter o hacer clic "Buscar con IA"
5. Esperar 5-10 segundos
```

**Prompt Exacto para Copiar/Pegar:**
```
Busco apartamento de 2 habitaciones en Medellín, máximo $300,000
```

**Resultado Esperado:**
```
✓ Se muestra "Analizando con IA..." mientras procesa
✓ Aparece sección "Análisis IA" con respuesta del Coordinator
✓ Sección "Análisis por Especialista" muestra:
  - SearchAgent: Propiedades encontradas
  - PropertyEvaluator: Evaluación
✓ Sección "Documentos Relevantes" muestra resultados RAG (si hay)
✓ Búsqueda aparece en "Historial de Búsquedas" abajo
```

**Respuestas Ejemplo que Verás:**
```
SearchAgent:
"He identificado 8 propiedades que coinciden con tus criterios
en Medellín con precios entre $245,000 y $299,000..."

PropertyEvaluator:
"Análisis de ubicación: Poblado 8.5/10, Laureles 8.0/10..."

Coordinator (Síntesis Final):
"🏆 RECOMENDACIÓN: Apto Poblado - $299,000..."
```

---

### Test 2.2: Búsqueda con Diferentes Criterios

**Objetivo:** Probar flexibilidad del sistema con criterios variados

**Pasos:** Repetir búsqueda con estos prompts alternos:

**Opción A - Búsqueda Luxury:**
```
Necesito casa de lujo en Medellín zona Sabaneta, 4+ habitaciones, piscina, presupuesto $1,000,000
```

**Opción B - Búsqueda Económica:**
```
Apto pequeño en Bogotá, máximo $150,000, área de parqueo
```

**Opción C - Búsqueda Específica:**
```
Oficina comercial en Cali, cerca de zona financiera, $500,000
```

**Opción D - Búsqueda Abierta:**
```
¿Cuáles son las mejores propiedades para invertir en Colombia ahora?
```

**Resultado Esperado (Todas):**
```
✓ Respuesta IA diferente según criterios
✓ Cada búsqueda se agrega al historial
✓ Sistema mantiene coherencia en análisis
✓ Agentes responden según el contexto
```

---

### Test 2.3: Búsqueda sin Criterios

**Objetivo:** Validar manejo de búsquedas vacías

**Pasos:**
```
1. Campo de búsqueda vacío
2. Hacer clic "Buscar con IA"
```

**Resultado Esperado:**
```
✓ Alert: "Por favor escribe una búsqueda"
✓ No se ejecuta búsqueda
✓ Permanece en mismo tab
```

---

### Test 2.4: Historial de Búsquedas

**Objetivo:** Verificar que se guarda el historial

**Pasos:**
```
1. Realizar 3 búsquedas diferentes (Tests 2.1, 2.2)
2. Bajar al final de "🔍 Búsqueda IA"
3. Ver sección "Historial de Búsquedas"
4. Hacer clic en una búsqueda anterior
```

**Resultado Esperado:**
```
✓ Se muestran todas las búsquedas realizadas
✓ Cada entrada muestra:
  - Query exacto
  - Timestamp
  - Número de resultados
✓ Al hacer clic, se recarga respuesta anterior
✓ No hay duplicados
```

---

## 🏘️ FUNCIONALIDAD 3: EXPLORAR PROPIEDADES

### Test 3.1: Cargar Propiedades sin Filtros

**Objetivo:** Ver todas las propiedades disponibles

**Pasos:**
```
1. Estar logueado
2. Ir a tab "🏘️ Propiedades"
3. Esperar que carguen propiedades
```

**Resultado Esperado:**
```
✓ Grilla muestra 12 propiedades por página
✓ Cada propiedad muestra:
  - Imagen/Ícono
  - Título/Dirección
  - Precio
  - Habitaciones
  - Baños
  - Área (m²)
  - Botón ❤️ (favoritos)
✓ Paginación en el fondo (números de página)
✓ Si no hay propiedades: "Cargando propiedades..."
```

---

### Test 3.2: Filtrar por Ciudad

**Objetivo:** Buscar propiedades en ubicación específica

**Pasos:**
```
1. En tab "Propiedades"
2. Campo "Ciudad": Medellín
3. Hacer clic "Aplicar Filtros"
4. Esperar resultados
```

**Datos para Probar:**
```
- Medellín
- Bogotá
- Cali
- Barranquilla
```

**Resultado Esperado:**
```
✓ Grilla actualiza mostrando solo propiedades en Medellín
✓ Contador: "Mostrando X propiedades"
✓ Si no hay: "No se encontraron propiedades"
```

---

### Test 3.3: Filtrar por Precio

**Objetivo:** Buscar en rango de precio

**Pasos:**
```
1. En tab "Propiedades"
2. "Precio mínimo": 200000
3. "Precio máximo": 400000
4. Hacer clic "Aplicar Filtros"
```

**Rangos para Probar:**
```
Rango 1:
- Mínimo: 150000
- Máximo: 300000

Rango 2:
- Mínimo: 500000
- Máximo: 1000000

Rango 3:
- Mínimo: 100000
- Máximo: 50000 (INVÁLIDO - prueba error)
```

**Resultado Esperado:**
```
✓ Muestra propiedades dentro del rango
✓ Filtra correctamente precios
✓ Si rango inválido: mostrar error
```

---

### Test 3.4: Filtrar por Tipo de Propiedad

**Objetivo:** Buscar por tipo (apartamento, casa, oficina)

**Pasos:**
```
1. En tab "Propiedades"
2. Seleccionar "Tipo de propiedad"
3. Elegir: "Apartamento"
4. Hacer clic "Aplicar Filtros"
```

**Tipos Disponibles:**
```
- Apartamento
- Casa
- Oficina
- Comercial
```

**Resultado Esperado:**
```
✓ Filtra por tipo seleccionado
✓ Actualiza grilla
✓ Permite combinar con otros filtros
```

---

### Test 3.5: Filtros Combinados

**Objetivo:** Usar múltiples filtros simultáneamente

**Pasos:**
```
1. Ciudad:           Medellín
2. Precio mínimo:    200000
3. Precio máximo:    500000
4. Tipo:             Apartamento
5. Habitaciones:     2
6. Hacer clic "Aplicar Filtros"
```

**Resultado Esperado:**
```
✓ Aplica todos los filtros
✓ Resultado: Apartamentos de 2 hab en Medellín, $200k-$500k
✓ Grilla actualiza correctamente
✓ Permite combinación compleja
```

---

### Test 3.6: Limpiar Filtros

**Objetivo:** Resetear filtros y ver todas las propiedades

**Pasos:**
```
1. Aplicar filtros (Test 3.5)
2. Hacer clic "Limpiar"
3. Esperar recarga
```

**Resultado Esperado:**
```
✓ Todos los campos se vacían
✓ Grilla muestra propiedades sin filtros
✓ Vuelve a página 1
✓ Cuenta de propiedades se reinicia
```

---

### Test 3.7: Paginación

**Objetivo:** Navegar entre páginas de resultados

**Pasos:**
```
1. En tab "Propiedades"
2. Al fondo, ver paginación
3. Hacer clic página "2"
4. Hacer clic "→ Siguiente" (si existe)
5. Hacer clic "← Anterior"
```

**Resultado Esperado:**
```
✓ Página 2 muestra propiedades 13-24
✓ Página anterior desactiva botón "← Anterior"
✓ Última página desactiva "→ Siguiente"
✓ Números actuales resaltados
✓ Número de propiedades se mantiene en 12 por página
```

---

## ❤️ FUNCIONALIDAD 4: FAVORITOS

### Test 4.1: Agregar a Favoritos

**Objetivo:** Marcar una propiedad como favorita

**Pasos:**
```
1. En tab "Propiedades"
2. En cualquier tarjeta de propiedad
3. Hacer clic en el botón ❤️ (corazón)
```

**Resultado Esperado:**
```
✓ Corazón cambia de color (se llena)
✓ Toast/mensaje: "Agregado a favoritos"
✓ Propiedad se guarda en BD
✓ Contador de favoritos aumenta
```

---

### Test 4.2: Ver Favoritos

**Objetivo:** Ver lista de propiedades favoritas

**Pasos:**
```
1. Agregar 2-3 propiedades a favoritos (Test 4.1)
2. Ir a tab "❤️ Favoritos"
3. Esperar que carguen
```

**Resultado Esperado:**
```
✓ Tab muestra solo propiedades favoritas
✓ Aparecen las 2-3 agregadas
✓ Corazones están llenos ❤️
✓ Orden: más recientes primero
✓ Si no hay: "No hay favoritos aún"
```

---

### Test 4.3: Quitar de Favoritos

**Objetivo:** Desmarcar una propiedad como favorita

**Pasos:**
```
1. En tab "Favoritos"
2. En una propiedad favorita
3. Hacer clic en ❤️ (corazón lleno)
```

**Resultado Esperado:**
```
✓ Corazón se vacía ❤️ → 🤍
✓ Desaparece de tab "Favoritos"
✓ Mensaje: "Removido de favoritos"
✓ En "Propiedades" ya no aparece como favorito
```

---

### Test 4.4: Sincronización de Favoritos

**Objetivo:** Verificar que favoritos se actualizan en ambos tabs

**Pasos:**
```
1. En tab "Propiedades": ❤️ una propiedad
2. Ir a tab "Favoritos" 
3. Volver a tab "Propiedades"
4. ❤️ otra propiedad
5. Ir a tab "Favoritos"
```

**Resultado Esperado:**
```
✓ Las 2 propiedades aparecen en "Favoritos"
✓ Corazones sincronizados en ambos tabs
✓ Sin lag ni retrasos
```

---

## 🤖 FUNCIONALIDAD 5: AGENTES ESPECIALIZADOS

### Test 5.1: Ver Lista de Agentes

**Objetivo:** Mostrar información de los 5 agentes

**Pasos:**
```
1. Ir a tab "🤖 Agentes"
2. Observar sección "Consultar Agentes Especializados"
```

**Resultado Esperado:**
```
✓ Se muestran 5 agentes:
  1. 🔍 SearchAgent - Real Estate Property Search Specialist
  2. 📊 PropertyEvaluator - Real Estate Valuation Expert
  3. 💰 FinancialAdvisor - Mortgage and Financial Planning Expert
  4. ⚖️ LegalAdvisor - Real Estate Legal Expert
  5. 🎯 Coordinator - Real Estate Transaction Coordinator

✓ Cada uno muestra nombre y rol
✓ Descripción visible
```

---

### Test 5.2: Ejecutar SearchAgent

**Objetivo:** Llamar agente específico y ver resultado

**Pasos:**
```
1. En tab "Agentes"
2. En "Ejecutar Agente Específico"
3. Seleccionar: "SearchAgent"
4. Descripción: "Busca aptos en Bogotá, máximo $250,000"
5. Hacer clic "Ejecutar"
6. Esperar respuesta (5-10 segundos)
```

**Datos para Probar:**
```
Agent: SearchAgent
Task:  Busca aptos en Bogotá, máximo $250,000
```

**Resultado Esperado:**
```
✓ Se muestra "Procesando..."
✓ Aparece respuesta en "Resultado:"
✓ Respuesta debe contener sugerencias de búsqueda
✓ Formato JSON/texto legible
✓ Sin errores en consola
```

---

### Test 5.3: Ejecutar PropertyEvaluator

**Objetivo:** Evaluar propiedades específicas

**Pasos:**
```
1. Seleccionar: "PropertyEvaluator"
2. Descripción: "Evalúa estas propiedades: Apto $300k Poblado, 
                 Casa $400k Laureles, Apto $250k Envigado"
3. Hacer clic "Ejecutar"
```

**Resultado Esperado:**
```
✓ Retorna análisis de valuación
✓ Ranking de propiedades
✓ Puntuación por ubicación
✓ Recomendación de inversión
```

---

### Test 5.4: Ejecutar FinancialAdvisor

**Objetivo:** Obtener análisis financiero

**Pasos:**
```
1. Seleccionar: "FinancialAdvisor"
2. Descripción: "Calcula hipoteca para apto de $300,000 
                 con 20% inicial"
3. Hacer clic "Ejecutar"
```

**Resultado Esperado:**
```
✓ Retorna cálculos de hipoteca
✓ Cuota mensual
✓ Monto inicial
✓ Período de financiamiento
✓ Tasas estimadas
```

---

### Test 5.5: Ejecutar LegalAdvisor

**Objetivo:** Obtener asesoría legal

**Pasos:**
```
1. Seleccionar: "LegalAdvisor"
2. Descripción: "¿Qué documentos necesito para comprar 
                 propiedad en Medellín?"
3. Hacer clic "Ejecutar"
```

**Resultado Esperado:**
```
✓ Retorna checklist legal
✓ Documentos requeridos
✓ Pasos del proceso
✓ Tiempo estimado
✓ Advertencias legales
```

---

### Test 5.6: Ejecutar Coordinator

**Objetivo:** Síntesis integral de todos los análisis

**Pasos:**
```
1. Seleccionar: "Coordinator"
2. Descripción: "Sintetiza el análisis completo de apto 
                 en Medellín a $300k: búsqueda, evaluación, 
                 finanzas y aspectos legales"
3. Hacer clic "Ejecutar"
```

**Resultado Esperado:**
```
✓ Retorna recomendación integral
✓ Resume todas las perspectivas
✓ Define próximos pasos
✓ Prioriza acciones
✓ Respuesta estructurada y clara
```

---

### Test 5.7: Error - Agente no seleccionado

**Objetivo:** Validar error cuando no hay agente

**Pasos:**
```
1. Dejar "Seleccionar agente..." por defecto
2. Escribir descripción
3. Hacer clic "Ejecutar"
```

**Resultado Esperado:**
```
✓ Error: "Selecciona un agente primero"
✓ No se ejecuta request
✓ Permanece en mismo tab
```

---

## 📄 FUNCIONALIDAD 6: GESTIÓN DE DOCUMENTOS (RAG)

### Test 6.1: Subir Documento PDF

**Objetivo:** Cargar un documento para búsqueda RAG

**Preparación Previa:**
```
1. Crear archivo PDF de prueba con contenido sobre:
   "Requisitos para compra de propiedad en Colombia"

O usar documento existente en: documents/
```

**Pasos:**
```
1. Ir a tab "📄 Documentos"
2. Sección "Subir Documentos"
3. Hacer clic en área de carga (o arrastra archivo)
4. Seleccionar PDF
5. Hacer clic "Subir Documentos"
6. Esperar confirmación (10-15 segundos)
```

**Resultado Esperado:**
```
✓ Se muestra "Procesando documento..."
✓ Mensaje: "✓ Documento procesado exitosamente"
✓ Número de chunks procesados
✓ Documento disponible para búsqueda
✓ Sin errores en consola
```

---

### Test 6.2: Búsqueda en Documentos

**Objetivo:** Buscar información dentro de documentos subidos

**Pasos:**
```
1. En tab "Documentos"
2. Sección "Buscar en Documentos"
3. Campo de búsqueda: "Documentos requeridos para compra"
4. Hacer clic "Buscar"
5. Esperar resultados
```

**Queries para Probar:**
```
Query 1: "Documentos requeridos"
Query 2: "Requisitos legales"
Query 3: "Proceso de compra"
Query 4: "Impuestos inmobiliarios"
Query 5: "Financiamiento"
```

**Resultado Esperado:**
```
✓ Se muestran documentos relevantes
✓ Cada resultado muestra:
  - Fragmento de texto
  - Fuente (archivo)
  - Score de similitud (0-1)
  - Resaltado: palabras clave
✓ Resultados ordenados por relevancia
✓ Si no hay: "No se encontraron documentos"
```

---

### Test 6.3: Múltiples Documentos

**Objetivo:** Probar búsqueda en múltiples PDFs

**Pasos:**
```
1. Subir 3 documentos diferentes:
   - legal_requirements.pdf
   - financial_guide.pdf
   - property_checklist.pdf
   (Test 6.1 x 3)

2. Buscar: "Financiamiento de propiedad"
```

**Resultado Esperado:**
```
✓ Resultado 1: financial_guide.pdf (alta relevancia)
✓ Resultado 2: property_checklist.pdf (media)
✓ Resultado 3: legal_requirements.pdf (baja)
✓ Ordenados por score de similitud
✓ Búsqueda abarca TODOS los documentos
```

---

### Test 6.4: Búsqueda RAG desde Búsqueda IA

**Objetivo:** Verificar integración de RAG con búsqueda principal

**Pasos:**
```
1. Haber subido documentos (Test 6.1)
2. Ir a tab "🔍 Búsqueda IA"
3. Hacer búsqueda: 
   "¿Qué documentos necesito para comprar?"
4. Ver sección "Documentos Relevantes (RAG)"
```

**Resultado Esperado:**
```
✓ Bajo la síntesis del Coordinator
✓ Sección muestra fragmentos de documentos
✓ Relacionados con la búsqueda
✓ Si no hay docs subidos: "No se encontraron..."
✓ Scores de similitud visibles
```

---

### Test 6.5: Búsqueda Vacía en Documentos

**Objetivo:** Validar campo de búsqueda vacío

**Pasos:**
```
1. Campo de búsqueda vacío
2. Hacer clic "Buscar"
```

**Resultado Esperado:**
```
✓ Alert: "Por favor escribe una búsqueda"
✓ No se ejecuta request
✓ Permanece en mismo tab
```

---

## 🔐 FUNCIONALIDAD 7: SEGURIDAD Y VALIDACIONES

### Test 7.1: Token JWT Expira

**Objetivo:** Validar comportamiento cuando expira token

**Pasos:**
```
1. Estar logueado (Test 1.2)
2. Abrir DevTools (F12)
3. Application → Cookies/Local Storage
4. Borrar manualmente el token
5. Intentar hacer búsqueda
```

**Resultado Esperado:**
```
✓ Error: "No autorizado" o similar
✓ Redirecciona a login
✓ Requiere re-autenticación
```

---

### Test 7.2: Datos Sensibles no Visibles

**Objetivo:** Verificar que credenciales no se exponen

**Pasos:**
```
1. Abrir DevTools (F12)
2. Network Tab
3. Hacer login
4. Revisar request de login
```

**Resultado Esperado:**
```
✓ Contraseña NO visible en Network
✓ Enviado vía HTTPS (en producción)
✓ Headers incluyen Content-Type: application/json
✓ Token retornado como Bearer
```

---

### Test 7.3: XSS Prevention (Script Injection)

**Objetivo:** Validar que no se ejecutan scripts maliciosos

**Pasos:**
```
1. En búsqueda, intentar:
   "<script>alert('XSS')</script>"
2. Observar resultado
```

**Resultado Esperado:**
```
✓ Script se muestra como texto, NO se ejecuta
✓ Si hay alert, es que hay vulnerabilidad
✓ Texto se escapa correctamente
```

---

## 📊 MATRIZ DE PRUEBAS RÁPIDA

| # | Funcionalidad | Test | Status | Notas |
|---|---|---|---|---|
| 1 | Registro | 1.1 | ⬜ | |
| 2 | Login | 1.2 | ⬜ | |
| 3 | Login Fallido | 1.3 | ⬜ | |
| 4 | Logout | 1.4 | ⬜ | |
| 5 | Búsqueda IA | 2.1 | ⬜ | |
| 6 | Búsqueda Variada | 2.2 | ⬜ | |
| 7 | Búsqueda Vacía | 2.3 | ⬜ | |
| 8 | Historial | 2.4 | ⬜ | |
| 9 | Propiedades | 3.1 | ⬜ | |
| 10 | Filtro Ciudad | 3.2 | ⬜ | |
| 11 | Filtro Precio | 3.3 | ⬜ | |
| 12 | Filtro Tipo | 3.4 | ⬜ | |
| 13 | Filtros Combinados | 3.5 | ⬜ | |
| 14 | Limpiar Filtros | 3.6 | ⬜ | |
| 15 | Paginación | 3.7 | ⬜ | |
| 16 | Agregar Favoritos | 4.1 | ⬜ | |
| 17 | Ver Favoritos | 4.2 | ⬜ | |
| 18 | Quitar Favoritos | 4.3 | ⬜ | |
| 19 | Sincronización | 4.4 | ⬜ | |
| 20 | Lista Agentes | 5.1 | ⬜ | |
| 21 | SearchAgent | 5.2 | ⬜ | |
| 22 | PropertyEvaluator | 5.3 | ⬜ | |
| 23 | FinancialAdvisor | 5.4 | ⬜ | |
| 24 | LegalAdvisor | 5.5 | ⬜ | |
| 25 | Coordinator | 5.6 | ⬜ | |
| 26 | Error Agente | 5.7 | ⬜ | |
| 27 | Subir PDF | 6.1 | ⬜ | |
| 28 | Buscar Docs | 6.2 | ⬜ | |
| 29 | Múltiples Docs | 6.3 | ⬜ | |
| 30 | RAG Integrado | 6.4 | ⬜ | |
| 31 | Búsqueda Vacía | 6.5 | ⬜ | |
| 32 | Token Expira | 7.1 | ⬜ | |
| 33 | Seguridad | 7.2 | ⬜ | |
| 34 | XSS Prevention | 7.3 | ⬜ | |

---

## 🎬 ESCENARIO DE PRUEBA INTEGRAL (End-to-End)

**Objetivo:** Ejecutar flujo completo del usuario

**Duración:** ~30 minutos

### Paso 1: Onboarding (5 min)
```
1. Ir a http://localhost:5000
2. Registrarse con email: e2e.test@example.com
3. Login exitoso
4. Ver dashboard
```

### Paso 2: Búsqueda IA (8 min)
```
1. Tab "Búsqueda IA"
2. Ejecutar búsqueda compleja:
   "Busco invertir en propiedad en Medellín, 
    presupuesto $500,000-$800,000, 
    preferiblemente Poblado o Laureles,
    3+ habitaciones, buena rentabilidad"
3. Revisar análisis de los 5 agentes
4. Ver documentos relacionados (RAG)
```

### Paso 3: Exploración (8 min)
```
1. Tab "Propiedades"
2. Filtros: 
   - Ciudad: Medellín
   - Rango: $500k-$800k
   - Tipo: Apartamento/Casa
3. Navegar entre páginas
4. Favoritar 3 propiedades
```

### Paso 4: Análisis Específico (5 min)
```
1. Tab "Agentes"
2. Ejecutar FinancialAdvisor:
   "Analiza financiamiento de $700,000 
    con 30% inicial"
3. Ejecutar Coordinator:
   "Sintetiza análisis completo"
```

### Paso 5: Documentación (4 min)
```
1. Tab "Documentos"
2. Subir PDF de requisitos legales
3. Buscar: "Documentos requeridos para compra"
4. Revisar resultados
```

### Resultado Final:
```
✓ Usuario tiene:
  - Búsqueda IA completa
  - 3 propiedades favoritas
  - Análisis financiero
  - Documentación legal
  - Recomendación del Coordinator
```

---

## 🐛 BUGS COMUNES Y CÓMO REPORTARLOS

### Formato de Reporte

```
TÍTULO: [Funcionalidad] - [Descripción breve del bug]

PASOS PARA REPRODUCIR:
1. ...
2. ...
3. ...

RESULTADO ESPERADO:
...

RESULTADO ACTUAL:
...

PANTALLA/STACK TRACE:
[Pega imagen o error]

NAVEGADOR: Chrome 120.0
SO: Windows 11
```

### Ejemplo Real

```
TÍTULO: Búsqueda IA - No muestra resultados RAG

PASOS PARA REPRODUCIR:
1. Ir a tab "Documentos"
2. Subir PDF
3. Ir a "Búsqueda IA"
4. Hacer búsqueda
5. Ver sección "Documentos Relevantes"

RESULTADO ESPERADO:
Debe mostrar fragmentos del PDF subido

RESULTADO ACTUAL:
Sección vacía, dice "No se encontraron documentos"

ERROR EN CONSOLA:
GET /api/rag/search - 500 Internal Server Error
```

---

## ✅ CHECKLIST FINAL

Antes de marcar proyecto como "Completo":

```
AUTENTICACIÓN:
☐ Registro funciona
☐ Login funciona
☐ Logout funciona
☐ Token persiste
☐ Sesión protegida

BÚSQUEDA IA:
☐ Busca texto libre
☐ Muestra respuestas de agentes
☐ Integra RAG
☐ Historial funciona
☐ Sin timeouts

PROPIEDADES:
☐ Carga sin filtros
☐ Filtro ciudad funciona
☐ Filtro precio funciona
☐ Filtros combinados
☐ Paginación correcta

FAVORITOS:
☐ Agregar funciona
☐ Tab favoritos actualiza
☐ Quitar funciona
☐ Sincronización correcta

AGENTES:
☐ 5 agentes visibles
☐ SearchAgent responde
☐ PropertyEvaluator responde
☐ FinancialAdvisor responde
☐ LegalAdvisor responde
☐ Coordinator responde

DOCUMENTOS:
☐ Subir PDF funciona
☐ Búsqueda en docs funciona
☐ RAG integrado funciona
☐ Múltiples docs funciona

SEGURIDAD:
☐ Token expira correctamente
☐ XSS prevention
☐ CORS funciona
☐ No hay datos sensibles expuestos

PERFORMANCE:
☐ Búsqueda IA <15s
☐ Carga propiedades <3s
☐ No hay memory leaks
☐ UI responsivo
```

---

**ÚLTIMA ACTUALIZACIÓN:** 27 de Mayo de 2026  
**VERSIÓN:** 1.0 - Testing Guide

---
