Operaciones con Conjuntos – App didáctica con Streamlit

Descripción
Aplicación para practicar operaciones entre conjuntos con una UI simple. Se ingresan tres conjuntos de enteros no negativos: Universo U, A y B. La app valida entradas, muestra resultados formateados y dibuja un diagrama de Venn.

Requisitos
- Python 3.12+
- Dependencias listadas en `requeriments.txt`

Instalación y ejecución
1) (Opcional) Crear y activar entorno virtual en Windows PowerShell:
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
2) Instalar dependencias:
   pip install -r requeriments.txt
3) Ejecutar:
   python -m streamlit run main.py

Uso básico
1) Ingresar U, A y B como números enteros >= 0 separados por comas (p. ej. U: 0, 1, 2, 3, 4, 5). La app:
   - Rechaza caracteres no numéricos y negativos.
   - Rechaza comas dobles o finales (tokens vacíos).
   - Muestra advertencias por duplicados en U, A o B.
   - Exige que A y B sean subconjuntos de U.
   Los mensajes aparecen en un banner superior “intrusivo” para mayor visibilidad.
2) Elegir una operación en las pestañas: Básicas (∪, ∩), Diferencias (A−B, B−A, A△B) o Complementos (A′, B′).
3) Ver el resultado en “Conjunto solución” y el diagrama de Venn debajo. El diagrama se genera apenas hay datos válidos en U, A y B; al seleccionar una operación, se resalta la región correspondiente.
4) Botón “🧹 Limpiar” (arriba a la derecha) para reiniciar U, A, B y la solución. Muestra confirmación en verde.

Detalles de validación
- Solo enteros no negativos (>= 0).
- Se permiten espacios alrededor de comas; se ignoran.
- No se permiten comas duplicadas ni coma final.
- Duplicados detectados por texto antes de convertir a `set`.
- Pertenencia: A ⊆ U y B ⊆ U. Si hay elementos de A o B fuera de U, se informa en el banner.

Cómo se calculan las operaciones
- Parsing: `modules/operations.py::parse_set` convierte el CSV a `set[int]` con validaciones.
- Lógica “por universo” (equivalente al ejemplo Java):
  - `operate_binary_by_universe(universe, a, b, op)` recorre U ordenado y para cada elemento x calcula p = x∈A y q = x∈B. Según `op` aplica:
    - union: p ∨ q
    - inter: p ∧ q
    - diff_a_b: p ∧ ¬q
    - diff_b_a: q ∧ ¬p
    - sym: p ⊕ q
  - `operate_unary_by_universe(universe, a, op)` para complemento: ¬p
  Esto asegura coherencia con ejercicios de aula que operan “sobre U”.
- Formato de salida: `modules/utils.py::format_set` ordena y presenta como cadena o “Ø” si vacío.

Interfaz y estado
- Los botones disparan el cálculo; el resultado se escribe en `st.session_state["s"]` y se refleja en el input de solución (`key="s_widget"`). Se evita escribir en la misma clave del widget para no generar errores de Streamlit.
- Las alertas se agregan con `add_alert(mensaje, nivel)` y se renderizan al inicio en un contenedor “sticky”. Niveles usados: error (rojo), warning (ámbar), success (verde).
- Universo efectivo: si el U ingresado no contiene A o B, se ajusta automáticamente a U′ = U ∪ A ∪ B y se muestra una advertencia. El diagrama etiqueta el Universo mostrando solo U − (A ∪ B).

Estructura del proyecto
- `main.py`: UI de Streamlit, validaciones visuales, disparo de operaciones, banner de alertas y sincronización del resultado.
- `modules/operations.py`: `parse_set`, `operate_binary_by_universe`, `operate_unary_by_universe`.
- `modules/utils.py`: `format_set`, `find_duplicates_in_csv`, `elements_not_in_universe`.
- `modules/diagram.py`: `draw_venn(a, b, universe)` y `draw_venn_with_highlight(a, b, op, universe)` para el diagrama de Venn. Las etiquetas de las regiones muestran elementos (A−B, B−A y A∩B) en lugar de conteos. El rectángulo del Universo se etiqueta con U − (A ∪ B). En complementos, el tono del Universo coincide con el resaltado de la operación.

Resolver problemas comunes
- No se ve el resultado: verifica que A y B ⊆ U y que el formato sea correcto (sin comas dobles, sin letras, sin negativos).
- Import de Streamlit no resuelto: activa el entorno y reinstala dependencias (`pip install -r requeriments.txt`).
- `matplotlib-venn` no encontrado: reinstala dependencias.
- Alertas tardías: el banner se renderiza en un contenedor superior reservado; si persiste, recarga la página del navegador.