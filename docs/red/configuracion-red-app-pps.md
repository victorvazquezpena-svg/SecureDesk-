# Configuración de red de APP-PPS

## 1. Descripción

La máquina virtual **APP-PPS** será utilizada como servidor para el desarrollo y despliegue del proyecto SecureDesk.

La máquina se ejecuta sobre **VirtualBox** y utiliza **Ubuntu Server** como sistema operativo.

Para facilitar la administración remota, las conexiones SSH y el acceso a los servicios desplegados, se ha planteado asignarle una dirección IP estática mediante **Netplan**.

---

## 2. Datos de la máquina

| Parámetro | Configuración |
|---|---|
| Sistema operativo | Ubuntu Server |
| Nombre del equipo | APP-PPS |
| Hipervisor | VirtualBox |
| Interfaz de red | `enp0s3` |
| IP anterior mediante DHCP | `10.5.255.48/16` |
| IP estática propuesta | `172.31.176.40` |
| Máscara propuesta | `255.255.255.0 (/24)` |
| Gateway propuesto | `172.31.176.1` |
| DNS | `8.8.8.8`, `1.1.1.1` |
| Herramienta de configuración | Netplan |

> **Nota:** La máscara `/24` y la puerta de enlace `172.31.176.1` están pendientes de comprobar con la configuración real de la red utilizada en VirtualBox.

---

## 3. Configuración de Netplan

El archivo de configuración se encuentra dentro de:

```text
/etc/netplan/
```

Se ha planteado utilizar una configuración similar a la siguiente:

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 172.31.176.40/24
      routes:
        - to: default
          via: 172.31.176.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

Antes de aplicar definitivamente esta configuración se deben comprobar la máscara de red y el gateway reales.

---

## 4. Comandos utilizados

Para consultar el estado actual de las interfaces:

```bash
ip -br a
```

Para consultar la tabla de rutas:

```bash
ip route
```

Para revisar la configuración actual de Netplan:

```bash
cat /etc/netplan/*.yaml
```

Para editar la configuración:

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Antes de aplicar definitivamente los cambios:

```bash
sudo netplan try
```

Si la configuración es correcta:

```bash
sudo netplan apply
```

---

## 5. Comprobaciones posteriores

Una vez aplicada la configuración se deben realizar las siguientes comprobaciones.

### Comprobar la dirección IP

```bash
ip -br a
```

La interfaz `enp0s3` deberá mostrar la dirección:

```text
172.31.176.40/24
```

### Comprobar la ruta por defecto

```bash
ip route
```

Deberá aparecer una ruta similar a:

```text
default via 172.31.176.1 dev enp0s3
```

### Comprobar conectividad con el gateway

```bash
ping -c 4 172.31.176.1
```

### Comprobar conectividad exterior

```bash
ping -c 4 8.8.8.8
```

### Comprobar resolución DNS

```bash
ping -c 4 google.com
```

---

## 6. Objetivo dentro de SecureDesk

La utilización de una dirección IP fija permitirá mantener una dirección conocida para acceder a los servicios desplegados en APP-PPS.

La arquitectura prevista será:

```text
Cliente / navegador / móvil
            |
            |
            v
   172.31.176.40:8080
            |
            v
+---------------------------+
| APP-PPS                   |
| Ubuntu Server             |
|                           |
| Docker / Docker Compose   |
|                           |
| - Aplicación SecureDesk   |
| - API Python / Flask      |
| - Base de datos           |
+---------------------------+
```

Esto permitirá posteriormente realizar:

- conexiones mediante SSH;
- administración remota del servidor;
- acceso a SecureDesk desde otros equipos;
- despliegue mediante Docker;
- pruebas de la aplicación desde otros dispositivos;
- auditorías mediante herramientas como OWASP ZAP o Burp Suite.

---

## 7. Estado actual

**Estado: pendiente de validación.**

La dirección `172.31.176.40` está definida como dirección objetivo para APP-PPS.

Antes de considerar finalizada la configuración se debe verificar:

- la máscara real de la red de VirtualBox;
- la puerta de enlace correspondiente;
- que la dirección `172.31.176.40` no esté siendo utilizada por otro equipo;
- conectividad con el gateway;
- conectividad exterior;
- resolución DNS.

Cuando estas comprobaciones sean correctas, se podrá considerar finalizada la configuración de red estática de APP-PPS.