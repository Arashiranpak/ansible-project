# Ansible Playbook for Nginx Web Server Deployment with Monitoring and Recovery

## Overview
This project automates the deployment and management of Nginx web servers on three cloud servers provided by **Abr Arvan**. The infrastructure is fully containerized using Docker, and monitoring is implemented using **Prometheus**, **Alertmanager**, and **Pushgateway**.

### Project Components
The project is divided into three main sections:
1. **Webserver**:
   - Deploys Nginx web servers across three nodes using containerized environments.
2. **Monitoring**:
   - Includes Prometheus, Pushgateway, and Alertmanager to monitor the health of the web servers and trigger alerts.
3. **Recovery**:
   - Implements automated container recovery when a web server becomes unavailable.

### Key Features
- **Nginx Deployment**:
  - Fully containerized deployment of Nginx web servers across three nodes.
- **Health Check Automation**:
  - A custom script runs every minute to check the health of the Nginx containers.
  - Pushes `1` (healthy) or `0` (down) to the Pushgateway.
- **Alerting & Auto-Recovery**:
  - Prometheus continuously monitors the Pushgateway metrics.
  - Alertmanager triggers when `web_health_check == 0` and automatically deploys a new Nginx container on a healthy node.

## Architecture Overview

1. **Nginx Web Servers**:
   - Deployed on three nodes defined in the `inventory.yml` file.
   - Fully containerized for flexibility and reliability.

2. **Monitoring Stack**:
   - **Pushgateway**: Receives health metrics from the health check script.
   - **Prometheus**: Monitors the `web_health_check` metric and triggers alerts based on conditions.
   - **Alertmanager**: Handles alert notifications and invokes a webhook for recovery actions.

3. **Health Check Script**:
   - Periodically checks the status of Nginx containers every minute.
   - Reports the health status (`1` or `0`) to the Pushgateway.

4. **Auto-Recovery**:
   - Alertmanager triggers a webhook when `web_health_check` equals `0`.
   - The webhook executes a recovery script to deploy a replacement Nginx container on a healthy node.

## Prerequisites
- **Cloud Environment**: Three servers provisioned in Abr Arvan.
- **Ansible Version**: Requires Ansible 2.9 or later.
- **Container Engine**: Docker installed on all target nodes.
