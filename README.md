# Proyecto Bot Cosmo

## 🌱 Idea del Proyecto

> Un bot cuyo propósito es animar a los usuarios a competir entre ellos para ver quién sabe más sobre el medio ambiente.  
> Esto también incentivará a que los usuarios investiguen y aprendan más sobre temas ecológicos.

---

## ⚙️ ¿Qué hace el bot?

- Primero, los usuarios deben registrarse para que el bot acepte sus comandos.  
- Luego, el bot les dará preguntas ecológicas (cada pregunta tiene una ganancia y una pérdida, ¡tengan cuidado!).  
- Contará con un sistema de ranking para ver quién tiene más *eco-coins*.  
- Permitirá ver la información del usuario.  
- Y también el historial completo de participación.

---

## 📜 Comandos

1. **`$register`**  
   Registra automáticamente al usuario en la base de datos de Discord (***ID de Discord y nombre de usuario***), y confirma que ya estás registrado.  
   Si el usuario ya existe, el bot lo notificará.

2. **`$question`**  
   El bot enviará una pregunta ecológica. Deberás responder correctamente (***palabras clave***).  
   Si aciertas, ganarás *eco-coins*; si fallas, se te restarán monedas de tu billetera virtual.

3. **`$ranking`**  
   El bot consultará la base de datos y mostrará la lista de usuarios registrados, ordenados de mayor a menor cantidad de *eco-coins*.

4. **`$info`**  
   Muestra tu información personal:  
   - ***Nombre de usuario***  
   - ***Cantidad actual de eco-coins***

5. **`$history`**  
   Muestra tu historial completo, incluyendo:  
   - Preguntas resueltas  
   - Respuestas dadas  
   - Monedas ganadas o perdidas  
   - Fechas correspondientes

---

## 💻 Requisitos

- Python 3.12

---

## 📦 Librerías

- `discord.py==2.3.2`  
- `python-dotenv==1.0.0`

---

## 🚀 Futuras Mejoras

- Sitio web oficial del bot  
- Reproducción de música en canales de voz  
- sistema anti-spam 
- Nuevos comandos:  
  - **`$clean`**: Borra todos los mensajes del canal.  
  - **`$shop`**: Una tienda donde se podrán comprar roles temporales o permanentes.
  - **`$eco-tip`**: Dar datos reales sobre el cambio climático o consejos diarios
