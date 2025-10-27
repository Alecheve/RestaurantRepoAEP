from flask import Flask, request

app = Flask(__name__)

# Diccionario "quemado" con 5 restaurantes
restaurantes = [
    {
        "id": 1,
        "nombre": "La Trattorina",
        "tipo": "italiana",
        "ubicacion": "centro",
        "calificacion": 4.5,
        "precio_promedio": 45000
    },
    {
        "id": 2,
        "nombre": "Sushi Master",
        "tipo": "japonesa",
        "ubicacion": "Sur",
        "calificacion": 4.8,
        "precio_promedio": 65000
    },
    {
        "id": 3,
        "nombre": "Tacos & tacos",
        "tipo": "mexicana",
        "ubicacion": "Norte",
        "calificacion": 4.2,
        "precio_promedio": 28000
    },
    {
        "id": 4,
        "nombre": "Burger Paradise",
        "tipo": "americana",
        "ubicacion": "Centro",
        "calificacion": 4.0,
        "precio_promedio": 35000
    },
    {
        "id": 5,
        "nombre": "Charruas",
        "tipo": "uruguaya",
        "ubicacion": "Sur",
        "calificacion": 4.7,
        "precio_promedio": 72000
    }
]


# Obtener un restaurante por path parameter ID
@app.route('/restaurantes/<int:restaurante_id>', methods=['GET'])
def get_restaurante_por_id(restaurante_id):
    resultado = list(filter(lambda r: r["id"] == restaurante_id, restaurantes))
    
    if resultado:
        return resultado[0], 200
    
    return {"error": "Restaurante no existe"}, 404


# Obtener todos los restaurantes o filtrar por query parameters
@app.route('/restaurantes', methods=['GET'])
def get_todos_restaurantes():    
    
    # Obtener query parameters
    tipo_param = request.args.get('tipo')
    calificacion_param = request.args.get('calificacion')
    ubicacion_param = request.args.get('ubicacion')
    
    print(f"Query params recibidos - tipo: {tipo_param}, calificacion: {calificacion_param}, ubicacion: {ubicacion_param}")
    
    # Comenzar con todos los restaurantes
    resultado = restaurantes.copy()
    
    # Filtrar por tipo de cocina (case insensitive)
    if tipo_param:
        resultado = list(filter(
            lambda r: r["tipo"].lower() == tipo_param.lower(), 
            resultado
        ))
    
    # Filtrar por calificación mínima
    if calificacion_param:
        try:
            calificacion_min = float(calificacion_param)
            resultado = list(filter(
                lambda r: r["calificacion"] >= calificacion_min, 
                resultado
            ))
        except ValueError:
            return {"error": "Calificación debe ser un número válido"}, 400
    
    # Filtrar por ubicación (case insensitive)
    if ubicacion_param:
        resultado = list(filter(
            lambda r: r["ubicacion"].lower() == ubicacion_param.lower(), 
            resultado
        ))
    
    if not resultado:
        return {"mensaje": "No se encontraron restaurantes con los filtros especificados", "restaurantes": []}, 200
    
    return {"total": len(resultado), "restaurantes": resultado}, 200


# ENDPOINT 3: POST crear un nuevo restaurante
@app.route('/restaurantes', methods=['POST'])
def crear_restaurante():
    global restaurantes
    data = request.get_json()
    
    # Validar que se envió data
    if not data:
        return {"error": "No se envió información"}, 400
    
    # Validar campos requeridos
    campos_requeridos = ["nombre", "tipo", "ubicacion", "calificacion", "precio_promedio"]
    for campo in campos_requeridos:
        if campo not in data:
            return {"error": f"El campo '{campo}' es requerido"}, 400
    

    id = len(restaurantes) + 1
    # Crear nuevo restaurante
    nuevo_restaurante = {
        "id": id,
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "ubicacion": data["ubicacion"],
        "calificacion": data["calificacion"],
        "precio_promedio": data["precio_promedio"]
    }
    
    # Agregar al diccionario
    restaurantes.append(nuevo_restaurante)
    
    print(f"Nuevo restaurante creado: {nuevo_restaurante}")
    
    return {
        "mensaje": "Restaurante creado exitosamente",
        "restaurante": nuevo_restaurante
    }, 201


# ENDPOINT 4: DELETE eliminar un restaurante por ID
@app.route('/restaurantes/<int:restaurante_id>', methods=['DELETE'])
def eliminar_restaurante(restaurante_id):
    
    # Buscar el restaurante
    restaurante_encontrado = None
    for r in restaurantes:
        if r["id"] == restaurante_id:
            restaurante_encontrado = r
            break
    
    if not restaurante_encontrado:
        return {"error": "Restaurante no encontrado"}, 404
    
    # Eliminar el restaurante
    restaurantes = [r for r in restaurantes if r["id"] != restaurante_id]
    
    print(f"Restaurante eliminado: {restaurante_encontrado}")
    
    return {
        "mensaje": "Restaurante eliminado exitosamente",
        "restaurante_eliminado": restaurante_encontrado
    }, 200


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8003,
        debug=True
    )