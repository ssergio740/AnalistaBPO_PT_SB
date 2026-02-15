def solicitud(solicitud):
    
    return {
        "compania": solicitud['compania'],
        "solicitud_id": solicitud['solicitud_id'],
        "solicitud_descripcion": solicitud['solicitud_descripcion']
    }

def respuesta(respuesta):
    return {
        "compania": respuesta['respuesta'],
        "solicitud_id": respuesta['solicitud_id'],
        "solicitud_fecha": respuesta['solicitud_fecha'],
        "solicitud_tipo": respuesta['solicitud_tipo'],
        "solicitud_prioridad": respuesta['solicitud_prioridad'],
        "solicitud_id_cliente": respuesta['solicitud_id_cliente'],
        "solicitud_tipo_id_cliente": respuesta['solicitud_tipo_id_cliente'],
        "solicitud_id_plataforma_externa": respuesta['solicitud_id_plataforma_externa'],
        "proximo_paso": respuesta['proximo_paso'],
        "justificacion": respuesta['justificacion'],
        "estado": respuesta['estado']
    }