from dataclasses import dataclass


@dataclass
class ScopeDTO:
    """
    Representa un nodo de la jerarquía de scopes de un proveedor cloud, normalizado
    para ser independiente del proveedor (Azure, AWS, GCP).

    En Azure la jerarquía es: Tenant -> Subscription -> ResourceGroup.
    Cada nivel se mapea a una fila en la tabla AmbitoNodo.

    Atributos:
        tipo_nodo:        Tipo del nodo en la jerarquía. Ej: "subscription", "resource_group".
        proveedor_ref_id: ID nativo del proveedor para este nodo. E sla clave que usamos
                          para construir el mapa ref→UUID durante la ingesta.
                          Ej Azure: "/subscriptions/abc-123"
                                    "/subscriptions/abc-123/resourceGroups/rg-prod"
        nombre:           Nombre legible del nodo. Ej: "rg-produccion".
        padre_ref_id:     proveedor_ref_id del nodo padre en la jerarquía del proveedor.
                          Es None para el nodo raíz (subscription).
                          La ingesta necesita dos pasadas para resolver este ID nativo
                          al UUID interno de AmbitoNodo (padre_id en la BD).
    """
    tipo_nodo: str
    proveedor_ref_id: str
    nombre: str
    padre_ref_id: str | None


@dataclass
class ResourceDTO:
    """
    Representa un recurso cloud concreto (VM, base de datos, almacenamiento, etc.),
    normalizado para ser independiente del proveedor.

    Cada instancia se mapea a una fila en la tabla Recurso.

    Atributos:
        recurso_ref_id: ID nativo del proveedor para este recurso. Se usa para
                        resolver la FK recurso.id durante la ingesta de costes y
                        para el upsert idempotente (ON CONFLICT).
                        Ej Azure: "/subscriptions/abc/resourceGroups/rg-prod/providers/Microsoft.Compute/virtualMachines/vm-01"
        ambito_ref_id:  proveedor_ref_id del scope (resource group) al que pertenece
                        este recurso. La ingesta lo resuelve al UUID interno de
                        AmbitoNodo (id_ambito_nodo en la BD) usando el mapa
                        construido al ingestar los scopes.
                        Ej Azure: "/subscriptions/abc-123/resourceGroups/rg-prod"
        nombre:         Nombre legible del recurso. Ej: "vm-produccion-01".
        tipo:           Tipo de recurso del proveedor. Ej: "Microsoft.Compute/virtualMachines".
        ubicacion:      Región donde está desplegado. Ej: "westeurope".
        estado:         Estado normalizado al enum de la BD: "activo", "detenido" o "eliminado".
        propiedades:    Metadatos adicionales específicos del proveedor en formato libre (JSONB).
    """
    recurso_ref_id: str
    ambito_ref_id: str
    nombre: str
    tipo: str
    ubicacion: str
    estado: str
    propiedades: dict
