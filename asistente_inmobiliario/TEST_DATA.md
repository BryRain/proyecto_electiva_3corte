# 🧪 DATOS DE PRUEBA - VALORES EXACTOS

**Documento de Datos para Testing Asistente Inmobiliario**  
**Copiar y pegar estos valores en los tests**

---

## 👤 USUARIOS DE PRUEBA

### Usuario 1: Principal

```
Email:         test.user@example.com
Username:      testuser123
Nombre:        Juan Pérez
Contraseña:    Password123
```

### Usuario 2: Alternativo

```
Email:         developer.test@email.com
Username:      devtester
Nombre:        María García
Contraseña:    TestPass456
```

### Usuario 3: Mínimo (Validar límites)

```
Email:         a@b.com
Username:      u
Nombre:        X
Contraseña:    123456
```

---

## 🏠 PROMPTS DE BÚSQUEDA IA

### Búsqueda 1: Estándar (Medellín)

```
Busco apartamento de 2 habitaciones en Medellín, máximo $300,000
```

**Respuesta Esperada Contiene:**
- SearchAgent: "He identificado X propiedades"
- PropertyEvaluator: Score de ubicación
- FinancialAdvisor: Cuota mensual
- Coordinator: Recomendación final

---

### Búsqueda 2: Luxury/Premium

```
Necesito casa de lujo en Medellín zona Sabaneta, 4+ habitaciones, piscina, jacuzzi, presupuesto $1,000,000
```

**Respuesta Esperada:**
- Enfoque en ubicación premium
- Amenidades especiales
- Análisis de inversión a largo plazo

---

### Búsqueda 3: Económica

```
Busco apto pequeño y económico en Bogotá, máximo $100,000, zona norte, cerca de transporte
```

**Respuesta Esperada:**
- Opciones bajo presupuesto
- Ubicaciones accesibles
- Buena relación precio/ubicación

---

### Búsqueda 4: Comercial

```
Oficina comercial en Cali para empresa de 50 personas, cerca de zona financiera, presupuesto $500,000
```

**Respuesta Esperada:**
- Análisis comercial
- Ubicación estratégica
- ROI potencial

---

### Búsqueda 5: Inversión

```
¿Cuál es la mejor propiedad para invertir en Colombia en 2024? Quiero rentabilidad del 10%+ anual
```

**Respuesta Esperada:**
- Análisis de rentabilidad
- Proyecciones
- Ciudades recomendadas

---

### Búsqueda 6: Específica

```
Apto en Medellín Poblado, 3 habitaciones, piso alto, vista a la ciudad, $450,000-$550,000
```

---

### Búsqueda 7: Múltiples Criterios

```
Casa en Bogotá zona Usaquén, mínimo 4 habitaciones, jardín, parqueadero, escuelas cercanas, $800,000
```

---

## 🏘️ FILTROS DE PROPIEDADES

### Filtro Set 1: Medellín - Rango Bajo

```
Ciudad:           Medellín
Precio Mínimo:    150000
Precio Máximo:    300000
Tipo:             (Todos)
Habitaciones:     (Todos)
```

**Resultados Esperados:** 8-15 propiedades

---

### Filtro Set 2: Bogotá - Rango Medio

```
Ciudad:           Bogotá
Precio Mínimo:    300000
Precio Máximo:    600000
Tipo:             Apartamento
Habitaciones:     2
```

**Resultados Esperados:** 3-8 propiedades

---

### Filtro Set 3: Premium - Todos

```
Ciudad:           (Todos)
Precio Mínimo:    800000
Precio Máximo:    2000000
Tipo:             Casa
Habitaciones:     4
```

**Resultados Esperados:** 2-5 propiedades

---

### Filtro Set 4: Económico - Apartamentos

```
Ciudad:           Cali
Precio Mínimo:    80000
Precio Máximo:    200000
Tipo:             Apartamento
Habitaciones:     1
```

**Resultados Esperados:** 5-10 propiedades

---

### Filtro Set 5: Multicriterio Complejo

```
Ciudad:           Medellín
Precio Mínimo:    250000
Precio Máximo:    450000
Tipo:             Apartamento
Habitaciones:     3
```

**Resultados Esperados:** 4-8 propiedades

---

## 💰 PROMPTS PARA AGENTES

### SearchAgent - Prompt 1

```
Busca aptos en Bogotá, máximo $250,000, 2 habitaciones, zona norte
```

**Respuesta Debe Incluir:**
- Número de propiedades encontradas
- Ubicaciones específicas
- Precios en rango

---

### SearchAgent - Prompt 2

```
¿Hay casas disponibles en Medellín Sabaneta entre $600k-$1M?
```

---

### PropertyEvaluator - Prompt 1

```
Evalúa estas propiedades: 
- Apto Poblado $300k, 80m², 2 hab
- Casa Laureles $400k, 120m², 3 hab
- Apto Envigado $250k, 75m², 2 hab
```

**Respuesta Debe Incluir:**
- Scoring de cada propiedad
- Recomendación de inversión
- Análisis de ubicación

---

### PropertyEvaluator - Prompt 2

```
¿Cuál es la mejor relación precio-m² entre estas opciones?
Opción A: $400k, 150m²
Opción B: $350k, 120m²
Opción C: $500k, 180m²
```

---

### FinancialAdvisor - Prompt 1

```
Calcula hipoteca para apto de $300,000:
- Inicial: 20% ($60,000)
- Plazo: 30 años
- Tasa: 7% anual
¿Cuál es la cuota mensual?
```

**Respuesta Debe Incluir:**
- Monto inicial
- Monto a financiar
- Cuota mensual exacta
- Tasa aplicable

---

### FinancialAdvisor - Prompt 2

```
Compara financiamiento:
Opción A: 20 años al 6.5%
Opción B: 30 años al 7%
Opción C: 15 años al 6%
Para propiedad de $500,000
```

---

### LegalAdvisor - Prompt 1

```
¿Qué documentos necesito como comprador para adquirir propiedad en Medellín?
```

**Respuesta Debe Incluir:**
- Documentación personal
- Documentación de la propiedad
- Proceso notarial

---

### LegalAdvisor - Prompt 2

```
Checklist legal para inversión inmobiliaria en Colombia
```

---

### Coordinator - Prompt 1

```
Sintetiza análisis completo de compra:
- Ubicación: Medellín Poblado
- Precio: $300,000
- Habitaciones: 2
- Área: 80m²
- Considera: búsqueda, evaluación, finanzas, legal
```

**Respuesta Debe Incluir:**
- Recomendación clara
- Próximos pasos en orden
- Ventajas y desventajas
- Timeline

---

### Coordinator - Prompt 2

```
Plan de acción para compra de propiedad en 6 semanas
```

---

## 📄 BÚSQUEDAS EN DOCUMENTOS

### Búsqueda 1: Requisitos

```
Búsqueda: "Documentos requeridos para compra"
Documento esperado: legal_requirements.pdf
```

---

### Búsqueda 2: Financiamiento

```
Búsqueda: "Hipoteca y financiamiento"
Documento esperado: financial_guide.pdf
```

---

### Búsqueda 3: Proceso

```
Búsqueda: "Proceso de compra paso a paso"
Documento esperado: purchase_process.pdf
```

---

### Búsqueda 4: Impuestos

```
Búsqueda: "Impuestos inmobiliarios en Colombia"
Documento esperado: tax_guide.pdf
```

---

### Búsqueda 5: Inversión

```
Búsqueda: "Estrategias de inversión inmobiliaria"
Documento esperado: investment_strategies.pdf
```

---

### Búsqueda 6: Verificación

```
Búsqueda: "Verificación de antecedentes de propiedad"
Documento esperado: verification_checklist.pdf
```

---

## 🔐 VALIDACIONES

### Contraseñas Válidas

```
✓ Password123
✓ SecurePass456
✓ MyProperty2024
✓ InversionIA789
✓ TestingPass01
```

### Contraseñas Inválidas

```
✗ 12345        (< 6 caracteres)
✗ pass         (< 6 caracteres)
✗ a            (1 carácter)
✗ (vacío)      (sin valor)
```

### Emails Válidos

```
✓ test@example.com
✓ user.name@domain.co
✓ property.test@email.com
✓ investor+123@gmail.com
```

### Emails Inválidos

```
✗ test.example.com    (sin @)
✗ @example.com        (sin usuario)
✗ test@.com          (sin dominio)
✗ test@@example.com   (@ duplicada)
```

---

## 💻 DATOS TÉCNICOS PARA DEBUGGING

### URLs de Endpoints

```
Login:             POST http://localhost:5000/api/auth/login
Register:          POST http://localhost:5000/api/auth/register
Búsqueda IA:       POST http://localhost:5000/api/ai/analyze
Propiedades:       GET  http://localhost:5000/api/properties
Favoritos:         GET  http://localhost:5000/api/favorites
Agentes Info:      GET  http://localhost:5000/api/agents
Ejecutar Agent:    POST http://localhost:5000/api/agents/execute
Subir Documento:   POST http://localhost:5000/api/documents/upload
Buscar Documentos: POST http://localhost:5000/api/documents/search
```

---

### Headers para Requests

```
Authorization: Bearer {token}
Content-Type: application/json
```

---

### Estructura JSON - Login Request

```json
{
  "email": "test.user@example.com",
  "password": "Password123"
}
```

---

### Estructura JSON - Register Request

```json
{
  "email": "test.user@example.com",
  "username": "testuser123",
  "full_name": "Juan Pérez",
  "password": "Password123"
}
```

---

### Estructura JSON - AI Search Request

```json
{
  "query": "Busco apartamento de 2 habitaciones en Medellín, máximo $300,000",
  "context": {
    "budget": 300000,
    "bedrooms": 2,
    "city": "Medellín"
  }
}
```

---

### Estructura JSON - Execute Agent Request

```json
{
  "agent_name": "search",
  "task": "Busca aptos en Bogotá máximo $250,000",
  "context": {
    "city": "Bogotá",
    "budget": 250000
  }
}
```

---

### Estructura JSON - Properties Filter Request

```json
{
  "city": "Medellín",
  "min_price": 200000,
  "max_price": 500000,
  "bedrooms": 2,
  "type": "apartment",
  "page": 1,
  "per_page": 12
}
```

---

## 📊 RESPUESTAS ESPERADAS (Ejemplos)

### Respuesta SearchAgent

```
"He identificado 8 propiedades que coinciden con tus criterios 
en Medellín con precios entre $245,000 y $299,000. 

Las opciones más relevantes son:
1. Apto Poblado - $299,000 - 2 hab - 80m²
2. Apto Laureles - $245,000 - 2 hab - 75m²
3. Apto Envigado - $280,000 - 2 hab - 85m²

Recomiendo revisar primero Poblado por su ubicación estratégica."
```

---

### Respuesta PropertyEvaluator

```
"ANÁLISIS DE VALUACIÓN:

Poblado ($299k):
- Ubicación: 8.5/10 (excelente)
- Precio/m²: $3,737 (justo para zona)
- Potencial revalorización: Alto
- Score: 8.5/10

Laureles ($245k):
- Ubicación: 8.0/10 (muy buena)
- Precio/m²: $3,266 (muy bueno)
- Potencial revalorización: Medio-alto
- Score: 8.0/10

RECOMENDACIÓN: Poblado mejor inversión, Laureles mejor relación precio."
```

---

### Respuesta FinancialAdvisor

```
"ANÁLISIS FINANCIERO - Propiedad $299,000

Simulación de Hipoteca:
- Valor total: $299,000
- Inicial (20%): $59,800
- Monto a financiar: $239,200

Opción 1 (30 años, 7% anual):
- Cuota mensual: $1,273
- Total pagado: $458,280
- Interés: $159,280

Opción 2 (20 años, 7% anual):
- Cuota mensual: $1,598
- Total pagado: $383,520
- Interés: $84,320

RECOMENDACIÓN: Cuota de $1,273/mes es más accesible."
```

---

### Respuesta LegalAdvisor

```
"DOCUMENTACIÓN REQUERIDA:

Del Vendedor:
✓ Título de propiedad original
✓ Cédula de ciudadanía
✓ Certificado de libertad y tradición
✓ Declaración de Renta (2 años)
✓ Certificado de servicios públicos

Del Comprador:
✓ Cédula de ciudadanía
✓ RUT actualizado
✓ Certificado bancario
✓ Declaración de Renta

Proceso Notarial: 30-45 días
Costo aprox: 3-4% del valor"
```

---

### Respuesta Coordinator

```
"🏆 RECOMENDACIÓN INTEGRAL FINAL:

✅ OPCIÓN ELEGIDA: Apto Poblado - $299,000

VENTAJAS:
• Ubicación estratégica: Poblado 8.5/10
• Precio competitivo: $3,737/m²
• Financiamiento accesible: $1,273/mes
• Documentación completa
• Alto potencial de revalorización

📋 PRÓXIMOS PASOS (6-8 semanas):

Semana 1:
1. Contactar vendedor
2. Agendar inspección
3. Revisar documentación

Semana 2-3:
4. Hacer oferta formal
5. Recopilar documentos

Semana 4-8:
6. Proceso notarial
7. Pago e inscripción
8. Entrega de llaves

💡 ACCIÓN INMEDIATA: Llamar vendedor hoy
⏰ TIEMPO TOTAL: 6-8 semanas"
```

---

## 🔍 VERIFICACIÓN RÁPIDA

### Checklist Mínimo

```
[ ] Registro funciona
[ ] Login funciona
[ ] Búsqueda IA retorna 5 agentes
[ ] Propiedades se cargan
[ ] Favoritos se guardan
[ ] Agentes responden
[ ] Documentos se suben
[ ] Búsqueda RAG funciona
```

---

## 🐛 ERRORES COMUNES

### Error 1: "OPENROUTER_API_KEY not configured"

```
Solución: En .env, verificar:
OPENROUTER_API_KEY=sk_live_...
```

---

### Error 2: "Database connection failed"

```
Solución:
1. Backend/database/init_db.py
2. Crear tables primero
3. Luego cargar datos
```

---

### Error 3: "Token expired"

```
Solución: Re-login
Frontend borrará token automáticamente
```

---

### Error 4: "No results from RAG"

```
Solución: Subir documentos primero
Luego esperar indexing (10-15s)
```

---

## 📈 PERFORMANCE TARGETS

```
Búsqueda IA:        < 15 segundos
Carga Propiedades:  < 3 segundos
Búsqueda Documentos: < 5 segundos
Subir PDF:          < 20 segundos
Carga Inicial:      < 5 segundos
```

---

**ÚLTIMA ACTUALIZACIÓN:** 27 de Mayo 2026  
**VERSIÓN:** 1.0 - Test Data

