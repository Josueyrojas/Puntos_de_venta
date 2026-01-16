import re

with open('metodos.py', 'r') as f:
    content = f.read()

# Find and replace the agregar_cliente method
pattern = r'    def agregar_cliente\(self, codigo: str, nombre: str, telefono: str, email: str = "", direccion: str = "", rfc: str = ""\):\s*"""Agrega un nuevo cliente"""\s*self\.clientes\[codigo\] = \{\s*"nombre": nombre,\s*"telefono": telefono,\s*"email": email,\s*"direccion": direccion,\s*"rfc": rfc\s*\}\s*self\.guardar_clientes\(\)'

replacement = '''    def agregar_cliente(self, codigo: str, nombre: str, telefono: str, email: str, direccion: str, rfc: str) -> Tuple[bool, str]:
        """Agrega un nuevo cliente con validaciones"""
        # Validar campos requeridos
        if not codigo.strip():
            return False, "El código del cliente es requerido"
        if not nombre.strip():
            return False, "El nombre del cliente es requerido"
        if not telefono.strip():
            return False, "El teléfono del cliente es requerido"
        if not email.strip():
            return False, "El email del cliente es requerido"
        if not direccion.strip():
            return False, "La dirección del cliente es requerida"
        if not rfc.strip():
            return False, "El RFC del cliente es requerido"
        
        # Validar formato de email
        if not validar_email(email):
            return False, "El formato del email no es válido"
        
        # Validar formato de RFC
        if not validar_rfc(rfc):
            return False, "El formato del RFC no es válido (debe ser 12-13 caracteres alfanuméricos)"
        
        # Verificar que el código no exista
        if codigo in self.clientes:
            return False, "Ya existe un cliente con este código"
        
        self.clientes[codigo] = {
            "nombre": nombre.strip(),
            "telefono": telefono.strip(),
            "email": email.strip(),
            "direccion": direccion.strip(),
            "rfc": rfc.upper().strip()
        }
        self.guardar_clientes()
        return True, "Cliente agregado exitosamente"'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('metodos.py', 'w') as f:
    f.write(new_content)

print('Replacement done')